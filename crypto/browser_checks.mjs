const {chromium}=await import(process.env.PROOFPICK_PLAYWRIGHT_MODULE || new URL('../.tools/browser-runtime/node_modules/playwright/index.mjs',import.meta.url));
const BASE=process.env.PROOFPICK_TEST_URL||'http://127.0.0.1:8765/';
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
const contexts=await Promise.all([0,1,2,3,4].map(()=>browser.newContext({viewport:{width:1200,height:1000}})));
const [seller,owner,...buyers]=await Promise.all(contexts.map(c=>c.newPage()));
const checks=[],errors=[];const pass=name=>{checks.push({name,passed:true});console.log(name);};
for(const p of [seller,owner,...buyers])p.on('pageerror',e=>errors.push(e.message));
async function click(p,id){await p.locator('#'+id).click();await p.waitForFunction(id=>!document.getElementById(id).disabled,id,{timeout:240000});}
try{
 await seller.goto(BASE);await click(seller,'create');await seller.locator('#access').waitFor({state:'visible'});
 const join=await seller.locator('#joinLink').inputValue();await owner.goto(await seller.locator('#ownerLink').inputValue());
 for(let i=0;i<3;i++){
  const p=buyers[i];await p.goto(join);await p.locator('#buyer').waitFor({state:'visible'});await p.locator('#quantity').fill(String(i+2));await p.locator('#budget').fill('10000');
  const req=p.waitForRequest(r=>r.url().endsWith('/api/order'));await click(p,'submitOrder');const body=(await req).postDataJSON();
  assert.deepEqual(Object.keys(body).sort(),['campaign','ciphertext','id','mpc','version']);assert.equal(body.mpc.encrypted.length,3);
  assert.match(await p.locator('#buyerState').innerText(),/注文受付済み/);
  if(i===2)await p.locator('#buyer').screenshot({path:'submission/groupbuy-order.png'});
 }
 pass('3ブラウザで数量2・3・4を端末で秘密分散し暗号化送信');
 await click(seller,'decrypt');assert.match(await seller.locator('#notice').innerText(),/先に/);pass('証明前の個別注文の復号を拒否');
 await click(owner,'close');await click(seller,'aggregate');
 console.log(await seller.locator('#notice').innerText());
 assert.match(await seller.locator('#proofState').innerText(),/合計 9個 \/ 1620円/);
 pass('実際のREP3共同計算・Groth16共同証明・snarkjs検証が成功');
 const info=await seller.evaluate(async()=>{const h=new URLSearchParams(location.hash.slice(1));return (await fetch('/api/view',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+h.get('token')},body:JSON.stringify({campaign:h.get('campaign')})})).json();});
 assert.equal(new Set(info.proof.pids).size,6);assert.equal(info.proof.public_inputs.length,32);
 await fs.writeFile('tests/reports/groupbuy-mpc-proof-example.json',JSON.stringify(info.proof,null,2));
 pass('6個のネイティブプロセスと32公開入力の証跡を保存');
 await seller.locator('#proofState').screenshot({path:'submission/groupbuy-mpc-proof.png'});
 await click(seller,'decrypt');assert.match(await seller.locator('#decrypted').innerText(),/合計 9個 \/ 1620円/);pass('開示した個別注文を登録commitmentと照合');
 await seller.locator('#seller').screenshot({path:'submission/groupbuy-demo.png'});
 await click(seller,'place');assert.match(await seller.locator('#state').innerText(),/発注済み/);pass('発注時にも実証明を再検証');
 await click(seller,'ready');for(const p of buyers){await click(p,'refresh');await click(p,'receive');}
 await click(seller,'refresh');assert.match(await seller.locator('#state').innerText(),/全員の受け取り/);pass('ZK検証済み発注から3件の受け取りまで完了');
 await seller.goto(BASE);await seller.locator('#minimum').fill('10');await click(seller,'create');await seller.locator('#access').waitFor({state:'visible'});
 const nextJoin=await seller.locator('#joinLink').inputValue(),nextId=new URLSearchParams(new URL(nextJoin).hash.slice(1)).get('campaign');await owner.goto(await seller.locator('#ownerLink').inputValue());await owner.waitForFunction(cid=>document.getElementById('campaignInput').value===cid,nextId);
 for(let i=0;i<3;i++){await buyers[i].goto(nextJoin);await buyers[i].waitForFunction(cid=>document.getElementById('campaignInput').value===cid,nextId);await buyers[i].locator('#buyer').waitFor({state:'visible'});await buyers[i].locator('#quantity').fill(String(i+2));await buyers[i].locator('#budget').fill('10000');await click(buyers[i],'submitOrder');assert.match(await buyers[i].locator('#buyerState').innerText(),/注文受付済み/);}
 await click(owner,'close');await click(seller,'aggregate');assert.match(await seller.locator('#proofState').innerText(),/成立数量に届いていません/);pass('成立数量に届かないことも実際に共同証明');
 const blocked=await seller.evaluate(async()=>{const h=new URLSearchParams(location.hash.slice(1)),headers={'Content-Type':'application/json',Authorization:'Bearer '+h.get('token')},campaign=h.get('campaign');const v=await (await fetch('/api/view',{method:'POST',headers,body:JSON.stringify({campaign})})).json();const response=await fetch('/api/place',{method:'POST',headers,body:JSON.stringify({campaign,orders:v.orders.map(o=>o.id),snapshot:v.snapshot})});return {status:response.status,hidden:v.orders.every(o=>!('ciphertext' in o))};});
 assert.equal(blocked.status,409);assert.equal(blocked.hidden,true);pass('不成立の証明では発注を拒否し個別注文も開示しない');
 assert.deepEqual(errors,[]);pass('ブラウザ実行エラーなし');
 await fs.writeFile('tests/reports/groupbuy-mpc-browser-report.json',JSON.stringify({date:'2026-11-05',scope:'3 buyer browser contexts; 3 native REP3 witness processes and 3 Groth16 proving processes on one trusted PC; development CRS; synthetic orders; no real payment/delivery.',checks,elapsed_ms:info.proof.elapsed_ms},null,2));
}finally{await browser.close();}
