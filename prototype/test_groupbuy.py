import base64
import json
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path
from groupbuy_server import Store, Rejected, make_server


class FakeEngine:
    """Only for transaction/role unit tests. Real proofs tested separately."""
    def registry(self):return [{'test_public_key':i} for i in range(3)]
    def verify(self,report,campaign,orders,snapshot):
        if report.get('snapshot')!=snapshot or not report.get('verified'):raise ValueError('invalid_test_proof')
        return {'verified':True,'eligible':report.get('eligible',True),'total':4,'amount':720}


class GroupPurchaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'orders.db'
        self.s=Store(self.path,engine=FakeEngine())
        self.c=self.s.call('create',{'title':'共同購入','product':'紙ナプキン','price':180,'minimum':3,
            'deadline':int(time.time())+86400,'public_key':{'kty':'RSA','e':'AQAB','n':base64.urlsafe_b64encode(b'\x80'+b'x'*255).decode().rstrip('=')}})
        self.cid=self.c['id'];self.b='b'*48;self.oid='order-000000000001';self.sealed=base64.b64encode(b'x'*256).decode()
        self.mpc={'commitment':'1','encrypted':[self.sealed]*3}
    def tearDown(self): self.temp.cleanup()
    def call(self,action,role='',**data):
        token=self.c[role+'_token'] if role in ('owner','seller') else role
        return self.s.call(action,{'campaign':self.cid,**data},token)
    def order(self):return self.call('order',self.b,id=self.oid,ciphertext=self.sealed,version=0,mpc=self.mpc)
    def placed(self):
        self.order();self.call('close','owner')
        snapshot=self.call('view','seller')['snapshot']
        with self.s.connect() as db:db.execute('UPDATE campaigns SET proof=? WHERE id=?',(json.dumps({'verified':True,'snapshot':snapshot}),self.cid))
        return self.call('place','seller',orders=[self.oid],snapshot=snapshot)
    def test_full_lifecycle_persists_and_receipt_is_idempotent(self):
        self.placed();self.s=Store(self.path,engine=FakeEngine());self.call('ready','seller')
        self.assertFalse(self.call('receive',self.b,id=self.oid)['replayed'])
        self.assertTrue(self.call('receive',self.b,id=self.oid)['replayed'])
        self.assertEqual(self.call('view')['state'],'COMPLETED')
    def test_owner_cannot_read_ciphertexts_buyer_cannot_list_others(self):
        self.order()
        self.assertNotIn('ciphertext',self.call('view','owner')['orders'][0])
        self.assertEqual(self.call('view','outsider')['orders'],[])
        self.assertNotIn('owner_token',self.call('view','owner'))
    def test_retry_has_one_order_and_one_event(self):
        self.order();self.assertTrue(self.order()['replayed'])
        self.assertEqual(self.call('view')['order_count'],1)
        self.assertEqual(len(self.call('view','owner')['events']),2)
    def test_cancel_is_final_and_excluded_from_purchase(self):
        self.order();self.call('cancel',self.b,id=self.oid)
        self.assertEqual(self.call('view')['order_count'],0)
        with self.assertRaises(Rejected):self.order()
    def test_wrong_roles_cannot_mutate(self):
        self.order()
        for action,role,extra in [('close',self.b,{}),('ready','owner',{}),('cancel','seller',{'id':self.oid}),('receive','owner',{'id':self.oid})]:
            with self.assertRaises(Rejected):self.call(action,role,**extra)
    def test_receipt_before_ready_rejected(self):
        self.placed()
        with self.assertRaises(Rejected):self.call('receive',self.b,id=self.oid)
    def test_stale_snapshot_rejected(self):
        self.order();old=self.call('view','seller')['snapshot']
        self.call('order',self.b,id=self.oid,ciphertext=base64.b64encode(b'y'*256).decode(),version=1,mpc=self.mpc)
        self.call('close','owner')
        with self.assertRaises(Rejected):self.call('place','seller',orders=[self.oid],snapshot=old)
    def test_partial_or_duplicate_manifest_rejected(self):
        self.order();self.call('close','owner');snap=self.call('view','seller')['snapshot']
        for ids in ([],[self.oid,self.oid],['other']):
            with self.assertRaises(Rejected):self.call('place','seller',orders=ids,snapshot=snap)
    def test_deadline_rejects_new_orders(self):
        with self.s.connect() as db:db.execute('UPDATE campaigns SET deadline=?',(int(time.time())-1,))
        with self.assertRaises(Rejected):self.order()
    def test_plaintext_fields_are_rejected(self):
        with self.assertRaises(Rejected):self.call('order',self.b,id=self.oid,ciphertext=self.sealed,version=0,quantity=3,budget=1000)
    def test_concurrent_retries_only_write_once(self):
        results=[]
        threads=[threading.Thread(target=lambda:results.append(self.order())) for _ in range(8)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(len(results),8)
        self.assertEqual(sum(not r['replayed'] for r in results),1)
    def test_http_enforces_origin(self):
        server=make_server(self.s,0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            request=urllib.request.Request(f'http://127.0.0.1:{server.server_port}/api/view',
                data=json.dumps({'campaign':self.cid}).encode(),headers={'Content-Type':'application/json','Origin':'https://evil.invalid'})
            with self.assertRaises(urllib.error.HTTPError) as error:urllib.request.urlopen(request)
            self.assertEqual(error.exception.code,403)
        finally:server.shutdown();server.server_close();thread.join()

    def test_proof_required_before_placing(self):
        self.order();self.call('close','owner');snap=self.call('view','seller')['snapshot']
        with self.assertRaises(Rejected):self.call('place','seller',orders=[self.oid],snapshot=snap)

    def test_seller_ciphertext_withheld_before_proof(self):
        self.order()
        self.assertNotIn('ciphertext',self.call('view','seller')['orders'][0])

    def test_single_order_aggregation_is_rejected(self):
        self.order();self.call('close','owner')
        with self.assertRaises(Rejected):self.call('aggregate','seller')

    def test_failed_eligibility_blocks_purchase(self):
        self.order();self.call('close','owner');snap=self.call('view','seller')['snapshot']
        with self.s.connect() as db:db.execute('UPDATE campaigns SET proof=? WHERE id=?',(json.dumps({'verified':True,'eligible':False,'snapshot':snap}),self.cid))
        with self.assertRaises(Rejected):self.call('place','seller',orders=[self.oid],snapshot=snap)

    def test_invalid_cached_proof_is_not_trusted(self):
        self.order();self.call('close','owner');snap=self.call('view','seller')['snapshot']
        with self.s.connect() as db:db.execute('UPDATE campaigns SET proof=? WHERE id=?',(json.dumps({'verified':False,'snapshot':snap}),self.cid))
        with self.assertRaises(ValueError):self.call('place','seller',orders=[self.oid],snapshot=snap)


if __name__=='__main__':unittest.main()
