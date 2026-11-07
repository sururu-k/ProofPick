import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
import hashlib
import io
import json
import time
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from groupbuy_identity import IdentityVerifier, b64


def sign(key, header, claims):
    encode=lambda value:b64(json.dumps(value,separators=(',',':')).encode())
    data=(encode(header)+'.'+encode(claims)).encode()
    return data.decode()+'.'+b64(key.sign(data))


class IdentityTests(unittest.TestCase):
    def setUp(self):
        self.issuer_key=Ed25519PrivateKey.generate()
        self.client_key=Ed25519PrivateKey.generate()
        def jwk(key):
            return {'crv':'Ed25519','kty':'OKP','x':b64(key.public_key().public_bytes(serialization.Encoding.Raw,serialization.PublicFormat.Raw))}
        self.key=jwk(self.issuer_key);self.client=jwk(self.client_key)
        self.thumb=b64(hashlib.sha256(json.dumps(self.client,separators=(',',':')).encode()).digest())
        self.verifier=IdentityVerifier()
        self.url='http://127.0.0.1:8765/api/order'
        self.jwks=json.dumps({'keys':[dict(self.key,kid='key1')]}).encode()
    def token(self, **overrides):
        claims={'iss':'http://localhost:3000','aud':'proofpick','exp':int(time.time())+300,'sub':'alice','cnf':{'jkt':self.thumb}}
        claims.update(overrides)
        return sign(self.issuer_key,{'typ':'at+jwt','alg':'EdDSA','kid':'key1'},claims)
    def proof(self, token, **overrides):
        claims={'jti':'abcdefghijklmnop1234','htm':'POST','htu':self.url,'iat':int(time.time()),'ath':b64(hashlib.sha256(token.encode()).digest())}
        claims.update(overrides)
        return sign(self.client_key,{'typ':'dpop+jwt','alg':'EdDSA','jwk':self.client},claims)
    def verify(self, token, proof):
        with patch('urllib.request.urlopen',return_value=io.BytesIO(self.jwks)):
            return self.verifier.verify(token,proof,self.url)
    def test_valid_and_replayed(self):
        token=self.token();proof=self.proof(token)
        self.assertEqual(self.verify(token,proof),'alice')
        with self.assertRaises(ValueError):self.verify(token,proof)
    def test_invalid_claims_and_binding(self):
        for changes in ({'aud':'wrong'}, {'iss':'http://wrong'}, {'exp':int(time.time())-1}, {'cnf':{'jkt':'wrong'}}):
            token=self.token(**changes)
            with self.assertRaises(ValueError):self.verify(token,self.proof(token))
        token=self.token()
        for changes in ({'htu':'http://wrong'}, {'ath':'wrong'}, {'iat':int(time.time())-1000}):
            with self.assertRaises(ValueError):self.verify(token,self.proof(token,**changes))
        parts=token.split('.');parts[2]=('A' if parts[2][0]!='A' else 'B')+parts[2][1:]
        with self.assertRaises(ValueError):self.verify('.'.join(parts),self.proof(token))

if __name__=='__main__':unittest.main()
