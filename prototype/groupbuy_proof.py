"""Actual 3-process co-circom REP3 calculation and Groth16 proof for Web orders.

The broker holds encrypted shares only. Each trustee decrypts its two REP3
shares into its own directory. This same-PC experiment trusts the OS/admin and
development CRS; it does not provide process-level protection against an admin.
"""
import base64
import datetime
import hashlib
import ipaddress
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from process_lock import exclusive_job

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'crypto-groupbuy'
EXE=ROOT/'.tools/co-snarks/target/release/co-circom.exe'
FIELD=21888242871839275222246405745257275088548364400416034343698204186575808495617

def field_hash(text):return str(int.from_bytes(hashlib.sha256(text.encode()).digest()[:16],'big'))
def run(command,**kwargs):
    p=subprocess.run(list(map(str,command)),capture_output=True,text=True,timeout=180,**kwargs)
    if p.returncode:raise ValueError('proof_process_failed: '+(p.stderr or p.stdout)[-500:])
    return p.stdout
def check_artifacts():
    manifest=json.loads((BASE/'artifacts/manifest.json').read_text())
    for name,expected in manifest.items():
        if hashlib.sha256((BASE/'artifacts'/name).read_bytes()).hexdigest()!=expected:
            raise ValueError('groupbuy_artifact_digest_mismatch')
    return manifest

class ProofEngine:
    def __init__(self,key_root):
        self.key_root=Path(key_root)
        with exclusive_job(ROOT/'.work/groupbuy-key-init.lock'):
            self.keys=[json.loads(run([sys.executable,BASE/'trustee.py',self.key_root/f'party{i}'])) for i in range(3)]
    def registry(self):return self.keys
    def prove(self,campaign,orders,snapshot):
        check_artifacts()
        if not EXE.is_file():raise ValueError('co_circom_not_built')
        if not 2<=len(orders)<=8:raise ValueError('MPC集計は2〜8件の有効な注文が必要です。')
        if json.loads(campaign['mpc_keys'])!=self.keys:raise ValueError('MPC鍵が変更されています。この募集は集計できません。')
        started=time.perf_counter()
        with exclusive_job(ROOT/'.work/groupbuy-proof.lock'), tempfile.TemporaryDirectory(prefix='groupbuy-proof-',dir=ROOT/'.work') as folder:
            directory=Path(folder)
            job={'campaign':campaign['id'],'context':campaign['mpc_context'],'batch':field_hash(snapshot),
                 'price':campaign['price'],'minimum':campaign['minimum'],'directory':folder,
                 'orders':[{'id':r['id'],'version':r['version'],'tag':field_hash(r['id']),'mpc':json.loads(r['mpc'])} for r in orders]}
            jobfile=directory/'job.json';jobfile.write_text(json.dumps(job),encoding='utf-8')
            run(['node',BASE/'public.mjs',jobfile]);job=json.loads(jobfile.read_text())
            self.configure(directory)
            for i in range(3):run([sys.executable,BASE/'trustee.py',self.key_root/f'party{i}','--job',jobfile,'--party',i])
            common=['--protocol','REP3','--curve','BN254']
            pids=[]
            for stage in ('witness','proof'):
                commands=[]
                for i in range(3):
                    part=directory/f'party{i}'
                    if stage=='witness':args=['generate-witness','--input',part/'input.json','--circuit',BASE/'purchase.circom','--out',part/'witness.shared']
                    else:args=['generate-proof','groth16','--witness',part/'witness.shared','--zkey',BASE/'artifacts/purchase.zkey','--out',part/'proof.json','--public-input',part/'public.json']
                    commands.append([EXE,*args,'--config',part/'config.toml',*common])
                processes=[]
                try:
                    for i,command in enumerate(commands):
                        log=open(directory/f'{stage}{i}.log','w',encoding='utf-8')
                        p=subprocess.Popen(list(map(str,command)),cwd=directory,stdout=log,stderr=log)
                        processes.append((p,log));pids.append(p.pid)
                    for p,_ in processes:
                        if p.wait(timeout=120):
                            (ROOT/'.work/groupbuy-last-error.log').write_text('\n'.join((directory/f'{stage}{j}.log').read_text(encoding='utf-8') for j in range(3)),encoding='utf-8')
                            raise ValueError('共同計算が失敗しました。分散入力または回路の条件が一致しません。')
                finally:
                    for p,log in processes:
                        if p.poll() is None:p.kill();p.wait()
                        log.close()
            report={'proof':json.loads((directory/'party0/proof.json').read_text()),
                    'public_inputs':json.loads((directory/'party0/public.json').read_text())}
            for i in (1,2):
                if json.loads((directory/f'party{i}/public.json').read_text())!=report['public_inputs']:raise ValueError('party_outputs_disagree')
            reportfile=directory/'proof.json';reportfile.write_text(json.dumps(report),encoding='utf-8')
            result=json.loads(run(['node',BASE/'verify.mjs',reportfile,jobfile]))
            report.update(result)
            report.update({'snapshot':snapshot,'expected':{k:job[k] for k in ('context','batch','price','minimum','expected_tail','expected_anchor')},
                           'order_count':len(orders),'pids':pids,'elapsed_ms':round((time.perf_counter()-started)*1000,2),
                           'scope':'Browser-created REP3 shares, 3 native witness processes and 3 native proving processes; independent snarkjs verifier. Same-PC OS/admin and development CRS trusted.'})
            return report
    def verify(self,report,campaign,orders,snapshot):
        # Rebuild expected public inputs from CURRENT stored orders, not proof-supplied claims.
        check_artifacts()
        with tempfile.TemporaryDirectory(prefix='groupbuy-verify-',dir=ROOT/'.work') as folder:
            folder=Path(folder);job={'context':campaign['mpc_context'],'batch':field_hash(snapshot),'price':campaign['price'],
                'minimum':campaign['minimum'],'orders':[{'tag':field_hash(r['id']),'mpc':json.loads(r['mpc'])} for r in orders]}
            jobfile=folder/'job.json';jobfile.write_text(json.dumps(job));run(['node',BASE/'public.mjs',jobfile])
            proof=folder/'proof.json';proof.write_text(json.dumps(report))
            return json.loads(run(['node',BASE/'verify.mjs',proof,jobfile]))
    def configure(self,directory):
        from cryptography import x509
        from cryptography.hazmat.primitives import hashes,serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        from cryptography.x509.oid import NameOID,ExtendedKeyUsageOID
        now=datetime.datetime.now(datetime.timezone.utc)
        for i in range(3):
            part=directory/f'party{i}';part.mkdir()
            key=ec.generate_private_key(ec.SECP256R1());name=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'localhost')])
            cert=x509.CertificateBuilder().subject_name(name).issuer_name(name).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(now-datetime.timedelta(minutes=5)).not_valid_after(now+datetime.timedelta(days=1)).add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost'),x509.IPAddress(ipaddress.ip_address('127.0.0.1'))]),False).add_extension(x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH,ExtendedKeyUsageOID.CLIENT_AUTH]),False).sign(key,hashes.SHA256())
            (part/'key.der').write_bytes(key.private_bytes(serialization.Encoding.DER,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
            (part/'cert.der').write_bytes(cert.public_bytes(serialization.Encoding.DER))
        for i in range(3):
            config='[compiler]\nlink_library = ['+json.dumps((ROOT/'.tools/fhe-runtime/node_modules/circomlib/circuits').as_posix())+']\n[network]\nmy_id = '+str(i)+f'\nbind_addr = "127.0.0.1:{18210+i}"\n'
            for j in range(3):config+=f'[[network.parties]]\nid = {j}\ndns_name = "127.0.0.1:{18210+j}"\n'
            config+='[network.tls]\nkey = '+json.dumps((directory/f'party{i}/key.der').as_posix())+'\ncerts = '+json.dumps([(directory/f'party{j}/cert.der').as_posix() for j in range(3)])+'\n'
            (directory/f'party{i}/config.toml').write_text(config)
