"""Local encrypted group purchasing workflow. python src/groupbuy_server.py"""
import argparse
import base64
import hashlib
import json
import os
import secrets
import sqlite3
import subprocess
import time
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from groupbuy_proof import ProofEngine, FIELD, field_hash
from process_lock import ExperimentBusy


class Rejected(ValueError):
    pass


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def require(ok, message):
    if not ok:
        raise Rejected(message)


def integer(value, low, high):
    return type(value) is int and low <= value <= high


class Store:
    def __init__(self, path, engine=None):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.engine=engine or ProofEngine(str(path)+'.trustees')
        with self.connect() as db:
            db.executescript('''
            CREATE TABLE IF NOT EXISTS campaigns (
              id TEXT PRIMARY KEY, title TEXT, product TEXT, price INTEGER,
              minimum INTEGER, deadline INTEGER, public_key TEXT,
              owner_hash TEXT, seller_hash TEXT, state TEXT, manifest TEXT);
            CREATE TABLE IF NOT EXISTS orders (
              id TEXT PRIMARY KEY, campaign TEXT, buyer_hash TEXT, ciphertext TEXT,
              state TEXT, version INTEGER, created INTEGER);
            CREATE TABLE IF NOT EXISTS events (
              seq INTEGER PRIMARY KEY, campaign TEXT, order_id TEXT, action TEXT, at INTEGER);
            ''')
            for table,columns in {'campaigns':['mpc_keys','mpc_context','proof'],'orders':['mpc']}.items():
                existing={r[1] for r in db.execute('PRAGMA table_info('+table+')')}
                for column in columns:
                    if column not in existing:db.execute(f'ALTER TABLE {table} ADD COLUMN {column} TEXT')

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def call(self, action, data, token='', principal=None):
        require(isinstance(data, dict), '入力はオブジェクトにしてください。')
        if action=='aggregate':return self.aggregate(data,token)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            return self._call(db, action, data, token, principal)

    def event(self, db, cid, oid, action):
        db.execute('INSERT INTO events(campaign,order_id,action,at) VALUES(?,?,?,?)',
                   (cid, oid, action, int(time.time())))

    def _call(self, db, action, d, token, principal=None):
        buyer_hash = digest(token) if principal is None else digest(json.dumps([principal, token], ensure_ascii=False, separators=(',',':')))
        if action == 'create':
            require(set(d) == {'title','product','price','minimum','deadline','public_key'}, '募集項目が不正です。')
            for name in ('title', 'product'):
                require(isinstance(d[name], str) and 1 <= len(d[name].strip()) <= 70, '募集名・商品名は1〜70文字です。')
            require(integer(d['price'], 1, 1000000), '単価が不正です。')
            require(integer(d['minimum'], 1, 10000), '最小数量が不正です。')
            require(integer(d['deadline'], int(time.time())+1, int(time.time())+366*86400), '締切は未来の日付にしてください。')
            key = d['public_key']
            require(isinstance(key, dict) and set(key) <= {'kty','n','e','alg','ext','key_ops'} and
                    key.get('kty') == 'RSA' and key.get('e') == 'AQAB' and
                    isinstance(key.get('n'),str) and len(key['n']) == 342, 'RSA 2048公開鍵が必要です。')
            try:
                modulus = base64.urlsafe_b64decode(key['n']+'==')
                require(len(modulus)==256 and modulus[0] >= 128, '公開鍵が不正です。')
            except (ValueError, TypeError):
                raise Rejected('公開鍵が不正です。')
            cid, owner, seller = secrets.token_urlsafe(12), secrets.token_urlsafe(32), secrets.token_urlsafe(32)
            db.execute('INSERT INTO campaigns(id,title,product,price,minimum,deadline,public_key,owner_hash,seller_hash,state,manifest) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                       (cid, d['title'].strip(), d['product'].strip(), d['price'], d['minimum'],
                        d['deadline'], json.dumps(key), digest(owner), digest(seller), 'OPEN', None))
            context=field_hash(json.dumps([cid,d['product'],d['price'],d['minimum'],d['deadline'],key],sort_keys=True))
            db.execute('UPDATE campaigns SET mpc_keys=?,mpc_context=? WHERE id=?',(json.dumps(self.engine.registry()),context,cid))
            self.event(db,cid,None,'created')
            return {'id':cid,'owner_token':owner,'seller_token':seller}

        cid = d.get('campaign')
        require(isinstance(cid,str) and 1<=len(cid)<=64, '募集IDが不正です。')
        c = db.execute('SELECT * FROM campaigns WHERE id=?',(cid,)).fetchone()
        require(c is not None, '募集が見つかりません。')
        owner = secrets.compare_digest(digest(token), c['owner_hash'])
        seller = secrets.compare_digest(digest(token), c['seller_hash'])
        if action == 'view':
            result = {k:c[k] for k in ('id','title','product','price','minimum','deadline','state')}
            result['public_key'] = json.loads(c['public_key'])
            result['mpc_keys']=json.loads(c['mpc_keys']) if c['mpc_keys'] else None
            result['mpc_context']=c['mpc_context']
            result['proof']=json.loads(c['proof']) if c['proof'] else None
            result['role'] = 'owner' if owner else 'seller' if seller else 'buyer'
            rows = db.execute('SELECT * FROM orders WHERE campaign=? ORDER BY created,id',(cid,)).fetchall()
            result['order_count'] = sum(r['state'] != 'CANCELLED' for r in rows)
            result['orders'] = []
            for r in rows:
                own = secrets.compare_digest(buyer_hash, r['buyer_hash'])
                if owner or seller or own:
                    item = {k:r[k] for k in ('id','state','version')}
                    if own or seller and c['proof'] and json.loads(c['proof']).get('eligible'):
                        item['ciphertext'] = r['ciphertext']
                        item['commitment']=json.loads(r['mpc'])['commitment'] if r['mpc'] else None
                    result['orders'].append(item)
            if owner or seller:
                result['manifest'] = json.loads(c['manifest']) if c['manifest'] else None
                result['events'] = [dict(r) for r in db.execute('SELECT seq,order_id,action,at FROM events WHERE campaign=? ORDER BY seq',(cid,))]
            if seller:
                result['snapshot'] = self.snapshot(db,cid)
            return result
        if action == 'order':
            require(set(d) == {'campaign','id','ciphertext','version','mpc'}, '注文には暗号文・秘密分散データ・受付IDだけを送信してください。')
            require(c['mpc_context'] is not None,'旧版の募集です。新しい募集を作成してください。')
            mpc=d['mpc']
            require(isinstance(mpc,dict) and set(mpc)=={'commitment','encrypted'}, '分散入力が必要です。')
            require(isinstance(mpc['commitment'],str) and mpc['commitment'].isascii() and mpc['commitment'].isdigit() and len(mpc['commitment'])<=77 and 0<=int(mpc['commitment'])<FIELD,'注文commitmentが不正です。')
            require(isinstance(mpc['encrypted'],list) and len(mpc['encrypted'])==3,'3者への分散入力が必要です。')
            for share in mpc['encrypted']:
                require(isinstance(share,str) and len(share)==344 and len(base64.b64decode(share,validate=True))==256,'分散入力の暗号文が不正です。')
            mpc_json=json.dumps(mpc,sort_keys=True)
            require(isinstance(token,str) and 32 <= len(token) <= 128, '注文用の秘密コードが必要です。')
            oid, sealed, version = d['id'], d['ciphertext'], d['version']
            require(isinstance(oid,str) and 16 <= len(oid) <= 64 and all(ch.isalnum() or ch in '-_' for ch in oid), '受付IDが不正です。')
            require(isinstance(sealed,str) and len(sealed)==344, '暗号文が不正です。')
            try:
                require(len(base64.b64decode(sealed, validate=True))==256, '暗号文が不正です。')
            except ValueError:
                raise Rejected('暗号文が不正です。')
            require(integer(version,0,100000), '更新番号が不正です。')
            old = db.execute('SELECT * FROM orders WHERE id=?',(oid,)).fetchone()
            if old:
                require(old['campaign']==cid and secrets.compare_digest(old['buyer_hash'],buyer_hash), 'この注文の操作権限がありません。')
                if old['ciphertext']==sealed and old['mpc']==mpc_json and old['version']==version+1 and old['state']!='CANCELLED':
                    return {'id':oid,'version':old['version'],'replayed':True}
            require(c['state']=='OPEN' and time.time()<c['deadline'], '受付は終了しています。')
            require(old is None and version==0 or old is not None and old['state']=='SUBMITTED' and old['version']==version, '注文が更新済み、または取消済みです。再読込してください。')
            if old:
                db.execute('UPDATE orders SET ciphertext=?,mpc=?,version=version+1 WHERE id=?',(sealed,mpc_json,oid))
            else:
                count=db.execute("SELECT COUNT(*) FROM orders WHERE campaign=? AND state!='CANCELLED'",(cid,)).fetchone()[0]
                require(count<8,'この版では1募集あたり8件まで受け付けます。')
                db.execute('INSERT INTO orders(id,campaign,buyer_hash,ciphertext,state,version,created,mpc) VALUES(?,?,?,?,?,?,?,?)',(oid,cid,buyer_hash,sealed,'SUBMITTED',1,int(time.time()),mpc_json))
            self.event(db,cid,oid,'updated' if old else 'submitted')
            return {'id':oid,'version':version+1,'replayed':False}
        if action in ('cancel','receive'):
            r = db.execute('SELECT * FROM orders WHERE id=? AND campaign=?',(d.get('id'),cid)).fetchone()
            require(r is not None and secrets.compare_digest(r['buyer_hash'],buyer_hash), 'この注文の操作権限がありません。')
            target = 'CANCELLED' if action=='cancel' else 'RECEIVED'
            if r['state']==target:
                return {'state':target,'replayed':True}
            if action=='cancel':
                require(c['state']=='OPEN' and time.time()<c['deadline'] and r['state']=='SUBMITTED', '締切後の取消はできません。')
            else:
                require(c['state']=='READY' and r['state']=='ORDERED', '販売者の準備完了後に受け取れます。')
            db.execute('UPDATE orders SET state=? WHERE id=?',(target,r['id']))
            self.event(db,cid,r['id'],action)
            if action=='receive' and not db.execute("SELECT 1 FROM orders WHERE campaign=? AND state='ORDERED'",(cid,)).fetchone():
                db.execute("UPDATE campaigns SET state='COMPLETED' WHERE id=?",(cid,))
            return {'state':target,'replayed':False}
        if action == 'close':
            require(owner, '主催者の権限が必要です。')
            require(c['state'] in ('OPEN','CLOSED'), 'この募集は締め切れません。')
            if c['state']=='OPEN':
                db.execute("UPDATE campaigns SET state='CLOSED' WHERE id=?",(cid,))
                self.event(db,cid,None,'closed')
            return {'state':'CLOSED'}
        if action == 'place':
            require(seller, '販売者の権限が必要です。')
            ids = d.get('orders')
            require(isinstance(ids,list) and all(isinstance(x,str) for x in ids) and len(ids)==len(set(ids)), '発注一覧が不正です。')
            active = sorted(r[0] for r in db.execute("SELECT id FROM orders WHERE campaign=? AND state!='CANCELLED'",(cid,)))
            require(sorted(ids)==active and bool(active), '締切時点の全注文を確認してください。')
            require(isinstance(d.get('snapshot'),str), '注文スナップショットが必要です。')
            snapshot = self.snapshot(db,cid)
            require(d['snapshot']==snapshot, '注文が変わりました。再確認してください。')
            require(c['proof'] is not None,'先に秘密集計とZK検証を実行してください。')
            proof=json.loads(c['proof'])
            rows=db.execute("SELECT * FROM orders WHERE campaign=? AND state!='CANCELLED' ORDER BY id",(cid,)).fetchall()
            checked=self.engine.verify(proof,c,rows,snapshot)
            require(checked['verified'] and checked['eligible'],'ZK検証または成立条件の確認に失敗しました。')
            manifest = {'campaign':cid,'orders':active,'snapshot':snapshot,'asserted_by':'seller',
                        'verified_total':checked['total'],'verified_amount':checked['amount'],
                        'scope':'REP3 aggregate and Groth16 verification of registered commitments; seller checks fulfillment openings locally.'}
            if c['state'] in ('ORDERED','READY','COMPLETED'):
                require(json.loads(c['manifest'])==manifest, '既存の発注と一致しません。')
                return {'manifest':manifest,'replayed':True}
            require(c['state']=='CLOSED', '主催者が締め切ってから発注してください。')
            db.execute('UPDATE campaigns SET state=?,manifest=? WHERE id=?',('ORDERED',json.dumps(manifest),cid))
            db.execute("UPDATE orders SET state='ORDERED' WHERE campaign=? AND state='SUBMITTED'",(cid,))
            self.event(db,cid,None,'placed')
            return {'manifest':manifest,'replayed':False}
        if action == 'snapshot':
            require(seller, '販売者の権限が必要です。')
            return {'snapshot':self.snapshot(db,cid)}
        if action == 'ready':
            require(seller and c['state'] in ('ORDERED','READY'), '発注後、販売者が準備完了にできます。')
            if c['state']=='ORDERED':
                db.execute("UPDATE campaigns SET state='READY' WHERE id=?",(cid,))
                self.event(db,cid,None,'ready')
            return {'state':'READY'}
        if action == 'fail':
            require(seller and c['state']=='CLOSED', '締切後、販売者が不成立にできます。')
            db.execute("UPDATE campaigns SET state='FAILED' WHERE id=?",(cid,))
            self.event(db,cid,None,'failed')
            return {'state':'FAILED'}
        raise Rejected('操作が見つかりません。')

    def snapshot(self, db, cid):
        rows = [dict(r) for r in db.execute("SELECT id,version,ciphertext,mpc FROM orders WHERE campaign=? AND state!='CANCELLED' ORDER BY id",(cid,))]
        return digest(json.dumps(rows, sort_keys=True,separators=(',',':')))

    def aggregate(self,d,token):
        cid=d.get('campaign');require(isinstance(cid,str),'募集IDが不正です。')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            c=db.execute('SELECT * FROM campaigns WHERE id=?',(cid,)).fetchone()
            require(c is not None and secrets.compare_digest(digest(token),c['seller_hash']), '販売者の権限が必要です。')
            require(c['state']=='CLOSED','受付を締め切ってから秘密集計してください。')
            rows=db.execute("SELECT * FROM orders WHERE campaign=? AND state!='CANCELLED' ORDER BY id",(cid,)).fetchall()
            require(2<=len(rows)<=8,'個別数量を直接公開しないため、2〜8件の注文をまとめて集計します。')
            snapshot=self.snapshot(db,cid)
            if c['proof']:
                report=json.loads(c['proof']);self.engine.verify(report,c,rows,snapshot);return report
        report=self.engine.prove(c,rows,snapshot)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            current=db.execute('SELECT state FROM campaigns WHERE id=?',(cid,)).fetchone()
            require(current['state']=='CLOSED' and self.snapshot(db,cid)==snapshot,'証明中に募集の状態が変わりました。結果は採用しません。')
            db.execute('UPDATE campaigns SET proof=? WHERE id=?',(json.dumps(report),cid))
            self.event(db,cid,None,'zk_verified')
        return report


def make_server(store, port=8765, identity=None):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_): pass
        def send(self, status, value, mime='application/json; charset=utf-8'):
            raw = value if isinstance(value,bytes) else json.dumps(value,ensure_ascii=False).encode()
            self.send_response(status)
            for key,val in {'Content-Type':mime,'Content-Length':str(len(raw)), 'Cache-Control':'no-store',
                            'X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer',
                            'Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; connect-src 'self' http://localhost:3000; frame-ancestors 'none'; base-uri 'none'"}.items():
                self.send_header(key,val)
            self.end_headers(); self.wfile.write(raw)
        def valid(self):
            expected=f'127.0.0.1:{self.server.server_port}'
            return self.headers.get('Host')==expected and self.headers.get('Origin') in (None,'http://'+expected)
        def do_GET(self):
            if not self.valid(): return self.send(403,{'error':'local_only'})
            file={'/':('groupbuy.html','text/html; charset=utf-8'),'/groupbuy.js':('groupbuy.js','text/javascript; charset=utf-8'),
                  '/groupbuy_mpc.js':('groupbuy_mpc.js','text/javascript; charset=utf-8'),
                  '/groupbuy_identity.js':('groupbuy_identity.js','text/javascript; charset=utf-8'),
                  '/groupbuy-vendor/poseidon.json':('groupbuy-vendor/poseidon.json','application/json')}.get(urlsplit(self.path).path)
            if urlsplit(self.path).path == '/identity-config': return self.send(200, {'enabled': identity is not None})
            if not file: return self.send(404,{'error':'not_found'})
            return self.send(200,(Path(__file__).parent/file[0]).read_bytes(),file[1])
        def do_POST(self):
            if not self.valid() or self.headers.get('Content-Type')!='application/json': return self.send(403,{'error':'local_json_only'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                require(0<size<=16000,'リクエストが大きすぎます。')
                principal = None
                if identity:
                    auth = self.headers.get('X-Identity-Token', '')
                    principal = identity.verify(auth, self.headers.get('DPoP', ''), 'http://127.0.0.1:%s%s' % (self.server.server_port, urlsplit(self.path).path))
                data=json.loads(self.rfile.read(size))
                action=self.path.removeprefix('/api/') if self.path.startswith('/api/') else ''
                token=self.headers.get('Authorization','').removeprefix('Bearer ')
                return self.send(200,store.call(action,data,token,principal))
            except (ValueError,TypeError,KeyError) as exc:
                return self.send(409,{'error':str(exc)})
            except ExperimentBusy:
                return self.send(409,{'error':'ほかの共同証明を実行中です。少し待って再実行してください。'})
            except subprocess.TimeoutExpired:
                return self.send(503,{'error':'共同証明が時間内に終わりませんでした。発注は確定していません。'})
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8765)
    parser.add_argument('--db',default='.work/groupbuy-mpc.sqlite3')
    args=parser.parse_args()
    identity = None
    if os.environ.get('PROOFPICK_IDENTITY') == '1':
        from groupbuy_identity import IdentityVerifier
        identity = IdentityVerifier()
    server=make_server(Store(args.db),args.port,identity)
    print(f'Group purchase: http://127.0.0.1:{server.server_port}/',flush=True)
    server.serve_forever()
