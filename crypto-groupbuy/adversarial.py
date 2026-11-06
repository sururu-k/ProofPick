"""Verify the actual saved proof and reject changed public inputs/proof/registry."""
import copy,json,sqlite3,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'prototype'))
from groupbuy_proof import ProofEngine
from groupbuy_server import Store

def main(db_path):
    engine=ProofEngine(str(db_path)+'.trustees')
    store=Store(db_path,engine=engine)
    with store.connect() as db:
        c=db.execute("SELECT * FROM campaigns WHERE state='COMPLETED' AND proof IS NOT NULL ORDER BY rowid DESC LIMIT 1").fetchone()
        if c is None:raise ValueError('Run the real browser workflow first')
        rows=[dict(r) for r in db.execute("SELECT * FROM orders WHERE campaign=? AND state!='CANCELLED' ORDER BY id",(c['id'],))]
        snap=store.snapshot(db,c['id'])
    c=dict(c);proof=json.loads(c['proof']);checks=[]
    def check(name,p=proof,campaign=c,orders=rows,snapshot=snap,reject=False):
        try:valid=engine.verify(p,campaign,orders,snapshot)['verified']
        except ValueError:valid=False
        passed=not valid if reject else valid
        checks.append({'case':name,'passed':passed});print(name,passed,flush=True)
        if not passed:raise AssertionError(name)
    check('original_real_proof')
    for index,name in [(0,'changed_total'),(1,'changed_amount'),(2,'changed_eligibility'),(3,'changed_batch_anchor'),(4,'changed_context'),(31,'changed_commitment')]:
        p=copy.deepcopy(proof);p['public_inputs'][index]=str(int(p['public_inputs'][index])+1);check(name,p=p,reject=True)
    p=copy.deepcopy(proof);p['proof']['pi_a'][0]='0';check('changed_curve_proof',p=p,reject=True)
    check('different_snapshot',snapshot='0'*64,reject=True)
    check('omitted_order',orders=rows[:-1],reject=True)
    changed=copy.deepcopy(rows);mpc=json.loads(changed[0]['mpc']);mpc['commitment']=str(int(mpc['commitment'])+1);changed[0]['mpc']=json.dumps(mpc)
    check('replaced_registered_order',orders=changed,reject=True)
    changed=copy.deepcopy(c);changed['price']+=1;check('changed_registered_price',campaign=changed,reject=True)
    output={'scope':'Actual Groth16 verification with independently rebuilt current-registry public inputs; no verifier mocks. Same-PC and development CRS.', 'checks':checks,'passed':all(x['passed'] for x in checks)}
    (ROOT/'prototype/groupbuy-mpc-adversarial-report.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
if __name__=='__main__':main(Path(sys.argv[1] if len(sys.argv)>1 else ROOT/'.work/groupbuy-mpc-test.sqlite3'))
