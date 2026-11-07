"""One trustee's key and REP3 input adapter. Never reconstructs an order quantity."""
import argparse,base64,json
from pathlib import Path
from cryptography.hazmat.primitives import serialization,hashes
from cryptography.hazmat.primitives.asymmetric import rsa,padding

FIELD=21888242871839275222246405745257275088548364400416034343698204186575808495617
def main():
    parser=argparse.ArgumentParser();parser.add_argument('directory');parser.add_argument('--job');parser.add_argument('--party',type=int,default=0)
    args=parser.parse_args();directory=Path(args.directory);directory.mkdir(parents=True,exist_ok=True)
    path=directory/'key.pem'
    if not path.exists():
        key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
        path.write_bytes(key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
    key=serialization.load_pem_private_key(path.read_bytes(),password=None)
    pub=key.public_key().public_numbers()
    b64=lambda n:base64.urlsafe_b64encode(n.to_bytes((n.bit_length()+7)//8,'big')).decode().rstrip('=')
    if not args.job:
        print(json.dumps({'kty':'RSA','n':b64(pub.n),'e':b64(pub.e),'alg':'RSA-OAEP-256','ext':True,'key_ops':['encrypt']}));return
    job=json.loads(Path(args.job).read_text(encoding='utf-8'))
    inputs=job['public_input'].copy()
    for index in range(8):
        if index<len(job['orders']):
            row=job['orders'][index]
            label=f"gb1|{job['campaign']}|{row['id']}|{row['version']}".encode()
            raw=key.decrypt(base64.b64decode(row['mpc']['encrypted'][args.party],validate=True),
                padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=label))
            if len(raw)!=128 or any(int.from_bytes(raw[i:i+32],'little')>=FIELD for i in range(0,128,32)):
                raise ValueError('noncanonical_share')
        else:raw=bytes(128)
        inputs[f'quantities[{index}]']={'Shared':list(raw[:64])}
        inputs[f'salts[{index}]']={'Shared':list(raw[64:])}
    Path(job['directory'],f'party{args.party}','input.json').write_text(json.dumps(inputs),encoding='utf-8')

if __name__=='__main__':main()
