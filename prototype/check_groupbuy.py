"""Run only the current group-purchase product checks, without legacy robot/crypto demos."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(ROOT),pattern='test_groupbuy.py'))
    report={'scope':'Role/transaction tests with explicit FakeEngine; real REP3/Groth16 tested separately in groupbuy-mpc-browser-report.json. No real payment or delivery.',
            'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
            'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                             ('groupbuy_server.py','groupbuy.js','groupbuy_mpc.js','groupbuy_proof.py','groupbuy.html','test_groupbuy.py','check_groupbuy.py')}}
    (ROOT/'groupbuy-test-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
