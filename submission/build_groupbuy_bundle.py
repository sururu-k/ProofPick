"""Package only the current group-purchase application and its application materials."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
from urllib.parse import urlsplit, unquote
import zipfile

ROOT=Path(__file__).resolve().parents[1]
NAMES=['src/'+x for x in (
    'groupbuy_server.py','groupbuy.js','groupbuy_mpc.js','groupbuy_identity.js',
    'groupbuy_identity.py','groupbuy_proof.py','process_lock.py','groupbuy.html',
    'groupbuy-vendor/poseidon.json','groupbuy-vendor/CIRCOMLIBJS-LICENSE','groupbuy-vendor/NOTICE.txt')]
NAMES += ['tests/'+x for x in ('test_groupbuy.py','test_identity.py','check_groupbuy.py')]
NAMES += ['tests/reports/'+p.name for p in sorted((ROOT/'tests/reports').glob('*.json')) if p.name != 'groupbuy-test-current.json']
NAMES += ['submission/'+x for x in ('index.html','product.html','entry-copy-2026.json','groupbuy-issue-map.html','groupbuy-demo.png','groupbuy-order.png','groupbuy-mpc-proof.png','zenjyocon_entry_sheet_2026.pptx','build_groupbuy_bundle.py')]
NAMES += ['slides/index.html','integration/pasta-compose.yml']
NAMES += ['crypto/'+name for name in (
    'LICENSE-GPL','REPRODUCE.txt','adversarial.py','browser_checks.mjs',
    'build-native.ps1','circuit_tests.mjs','install.ps1','package-lock.json',
    'package.json','public.mjs','purchase.circom','runtime.mjs','setup.mjs',
    'trustee.py','upstream.json','verify.mjs','verify_export.mjs',
    'artifacts/manifest.json','artifacts/purchase.r1cs','artifacts/purchase.sym',
    'artifacts/purchase.zkey','artifacts/purchase_js/purchase.wasm',
    'artifacts/verification_key.json',
)]

def build():
    files={name:(ROOT/name).read_bytes() for name in NAMES}
    files['submission/index.html']=files['submission/index.html'].replace(b'groupbuy-source.zip',b'../README.txt')
    files['README.txt']=(ROOT/'crypto/REPRODUCE.txt').read_bytes()
    class Links(HTMLParser):
        def __init__(self,text):super().__init__();self.links=[];self.feed(text)
        def handle_starttag(self,tag,attrs):
            for key,val in attrs:
                if key in ('href','src'):self.links.append(val)
    for name,raw in files.items():
        if name.startswith('submission/') and name.endswith('.html'):
            for link in Links(raw.decode()).links:
                url=urlsplit(link)
                if url.scheme or url.netloc or not url.path or url.path.startswith('/'):continue
                target=posixpath.normpath(posixpath.join(posixpath.dirname(name),unquote(url.path)))
                assert target in files,(name,link)
    manifest={name:hashlib.sha256(raw).hexdigest() for name,raw in files.items()}
    files['source-manifest.json']=json.dumps(manifest,indent=2).encode()
    out=ROOT/'submission/groupbuy-source.zip'
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for name,raw in files.items():z.writestr(name,raw)
    with zipfile.ZipFile(out) as z:
        assert all(hashlib.sha256(z.read(name)).hexdigest()==sha for name,sha in manifest.items())
    print(json.dumps({'files':len(files),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))
if __name__=='__main__':build()
