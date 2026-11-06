import fs from 'node:fs';
import {createRequire} from 'node:module';
import {snarks} from './runtime.mjs';
const require=createRequire(import.meta.url),{buildPoseidon}=require('../.tools/fhe-runtime/node_modules/circomlibjs');
const p=await buildPoseidon(),poseidon=xs=>p.F.toString(p(xs)),{groth16}=await snarks();
const dir=new URL('artifacts/',import.meta.url).pathname.replace(/^\/([A-Za-z]:)/,'$1');
function input(){const v={context:'123',batch:'456',price:180,minimum:3,active:[1,1,0,0,0,0,0,0],tags:[1,2,0,0,0,0,0,0],quantities:[2,3,0,0,0,0,0,0],salts:[42,43,0,0,0,0,0,0]};return v;}
const checks=[];
for(const [name,change]of [
 ['active_zero_quantity',v=>v.quantities[0]=0],
 ['quantity_above_9999',v=>v.quantities[0]=10000],
 ['negative_field_quantity',v=>v.quantities[0]='21888242871839275222246405745257275088548364400416034343698204186575808495616'],
 ['inactive_nonzero_quantity',v=>v.quantities[2]=1],
 ['inactive_nonzero_salt',v=>v.salts[2]=1],
 ['nonboolean_active',v=>v.active[0]=2],
]){
 const v=input();change(v);v.commitments=v.tags.map((tag,i)=>poseidon([v.context,tag,v.quantities[i],v.salts[i]]));
 let rejected=false;try{await groth16.fullProve(v,dir+'purchase_js/purchase.wasm',dir+'purchase.zkey');}catch{rejected=true;}
 checks.push({case:name,passed:rejected});if(!rejected)throw Error(name+' accepted');
}
fs.writeFileSync(new URL('../prototype/groupbuy-circuit-report.json',import.meta.url),JSON.stringify({scope:'Actual Circom WASM witness constraints; intentionally invalid inputs. Not a multi-party run.',checks,passed:true},null,2));
console.log(JSON.stringify({passed:true,checks:checks.length}));process.exit(0);
