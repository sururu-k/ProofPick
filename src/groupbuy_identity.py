"""Local PASTA access-token and DPoP verification for the ProofPick demo."""
import base64
import hashlib
import json
import threading
import time
import urllib.request
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


def b64(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()


def decode(value):
    return base64.urlsafe_b64decode(value + '=' * (-len(value) % 4))


def jwt(value):
    parts = value.split('.')
    if len(parts) != 3 or len(value) > 12000:
        raise ValueError('invalid JWT')
    return json.loads(decode(parts[0])), json.loads(decode(parts[1])), (parts[0]+'.'+parts[1]).encode(), decode(parts[2])


class IdentityVerifier:
    def __init__(self, issuer='http://localhost:3000', client_id='proofpick'):
        if issuer != 'http://localhost:3000':
            raise ValueError('This demo only trusts the local IdP')
        self.issuer, self.client_id = issuer, client_id
        self.used = {}
        self.lock = threading.Lock()

    def verify(self, token, proof, url):
        try:
            h, claims, message, signature = jwt(token)
            if h.get('typ') != 'at+jwt' or h.get('alg') != 'EdDSA' or not isinstance(h.get('kid'), str):
                raise ValueError('invalid token header')
            with urllib.request.urlopen(self.issuer + '/jwks.json', timeout=3) as response:
                keys = json.load(response)['keys']
            keys = [k for k in keys if k.get('kid') == h['kid'] and k.get('kty') == 'OKP' and k.get('crv') == 'Ed25519']
            if len(keys) != 1:
                raise ValueError('unknown key')
            Ed25519PublicKey.from_public_bytes(decode(keys[0]['x'])).verify(signature, message)
            now = time.time()
            aud = claims.get('aud')
            if claims.get('iss') != self.issuer or not (aud == self.client_id or isinstance(aud, list) and self.client_id in aud) or type(claims.get('exp')) not in (int, float) or claims['exp'] <= now or not isinstance(claims.get('sub'), str) or not claims['sub']:
                raise ValueError('invalid claims')
            ph, pc, pm, ps = jwt(proof)
            jwk = ph.get('jwk', {})
            if ph.get('typ') != 'dpop+jwt' or ph.get('alg') != 'EdDSA' or set(jwk) != {'kty','crv','x'} or jwk['kty'] != 'OKP' or jwk['crv'] != 'Ed25519':
                raise ValueError('invalid proof header')
            Ed25519PublicKey.from_public_bytes(decode(jwk['x'])).verify(ps, pm)
            thumb = b64(hashlib.sha256(json.dumps({'crv':'Ed25519','kty':'OKP','x':jwk['x']}, separators=(',',':')).encode()).digest())
            if claims.get('cnf', {}).get('jkt') != thumb or pc.get('htm') != 'POST' or pc.get('htu') != url or pc.get('ath') != b64(hashlib.sha256(token.encode()).digest()) or type(pc.get('iat')) is not int or abs(now-pc['iat']) > 60 or not isinstance(pc.get('jti'), str) or not 16 <= len(pc['jti']) <= 128:
                raise ValueError('invalid proof')
            with self.lock:
                self.used = {k:v for k,v in self.used.items() if v > now}
                key = (thumb, pc['jti'])
                if key in self.used:
                    raise ValueError('replayed proof')
                self.used[key] = now + 121
            return claims['sub']
        except Exception as exc:
            raise ValueError('分散IDの検証に失敗しました。再ログインしてください。') from exc
