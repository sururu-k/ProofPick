// Only public campaign data and commitments are processed here.
import fs from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {buildPoseidon}=require('../.tools/fhe-runtime/node_modules/circomlibjs');
const poseidon=await buildPoseidon();
const file=process.argv[2],job=JSON.parse(fs.readFileSync(file,'utf8'));
const p=xs=>poseidon.F.toString(poseidon(xs));
const active=Array.from({length:8},(_,i)=>i<job.orders.length?'1':'0');
const tags=Array.from({length:8},(_,i)=>job.orders[i]?.tag||'0');
const commitments=Array.from({length:8},(_,i)=>job.orders[i]?.mpc.commitment||p([job.context,0,0,0]));
const scalar=x=>Array.from({length:32},(_,i)=>Number((BigInt(x)>>BigInt(i*8))&255n));
const input={};
for(const k of ['context','batch','price','minimum'])input[k]={Public:scalar(job[k])};
for(const [k,arr]of Object.entries({active,tags,commitments}))arr.forEach((v,i)=>input[`${k}[${i}]`]={Public:scalar(v)});
job.public_input=input;
job.expected_tail=[job.context,job.batch,String(job.price),String(job.minimum),...active,...tags,...commitments];
job.expected_anchor=p([job.context,job.batch]);
fs.writeFileSync(file,JSON.stringify(job));
