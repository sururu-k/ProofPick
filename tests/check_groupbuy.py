"""Run only the current group-purchase product checks, without legacy robot/crypto demos."""
import hashlib
import json
from pathlib import Path
import unittest
import sys

ROOT=Path(__file__).resolve().parents[1]
TESTS=ROOT/'tests'
sys.path.insert(0, str(ROOT/'src'))
if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(TESTS),pattern='test_groupbuy.py'))
    report={'scope':'Role/transaction tests with explicit FakeEngine; real REP3/Groth16 tested separately in groupbuy-mpc-browser-report.json. No real payment or delivery.',
            'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),
            'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in
                             ('src/groupbuy_server.py','src/groupbuy.js','src/groupbuy_mpc.js','src/groupbuy_proof.py','src/groupbuy.html','tests/test_groupbuy.py','tests/check_groupbuy.py')}}
    (TESTS/'reports/groupbuy-test-current.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
