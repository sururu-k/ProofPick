// SPDX-License-Identifier: GPL-3.0-only
// Poseidon parameters from iden3/circomlibjs 0.1.7 (GPL-3.0).
// Browser field implementation and encrypted REP3 input adapter for ProofPick.
const FIELD=21888242871839275222246405745257275088548364400416034343698204186575808495617n;
let parameters;
const mod=x=>(x%FIELD+FIELD)%FIELD;
const bytes=n=>Array.from({length:32},(_,i)=>Number((n>>BigInt(i*8))&255n));
const uniform=()=>{for(;;){const b=crypto.getRandomValues(new Uint8Array(32));b[31]&=63;const n=b.reduceRight((v,x)=>(v<<8n)+BigInt(x),0n);if(n<FIELD)return n;}};
export async function poseidon4(values){
 if(!parameters){const response=await fetch('/groupbuy-vendor/poseidon.json');if(!response.ok)throw Error('Poseidon定数を読み込めません。');const p=await response.json();parameters={C:p.C.map(BigInt),M:p.M.map(r=>r.map(BigInt))};}
 let s=[0n,...values.map(BigInt)];if(s.length!==5)throw Error('poseidon_arity');
 const pow5=x=>{const a=x*x%FIELD;return a*a%FIELD*x%FIELD;};
 for(let r=0;r<68;r++){s=s.map((x,i)=>(x+parameters.C[r*5+i])%FIELD);s=s.map((x,i)=>(r<4||r>=64||i===0)?pow5(x):x);s=parameters.M.map(row=>row.reduce((a,x,i)=>(a+x*s[i])%FIELD,0n));}
 return s[0].toString();
}
export async function tag(order){const raw=new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(order)));return BigInt('0x'+Array.from(raw.slice(0,16),b=>b.toString(16).padStart(2,'0')).join('')).toString();}
export async function prepareMpc(campaign,order,version,quantity,context,keys){
 const salt=uniform(), shares=x=>{const a=uniform(),b=uniform();return [a,b,mod(x-a-b)];};
 const qs=shares(BigInt(quantity)),rs=shares(salt);
 const commitment=await poseidon4([context,await tag(order),quantity,salt]);
 const label=new TextEncoder().encode(`gb1|${campaign}|${order}|${version}`);
 const encrypted=[];
 for(let i=0;i<3;i++){
  const key=await crypto.subtle.importKey('jwk',keys[i],{name:'RSA-OAEP',hash:'SHA-256'},false,['encrypt']);
  const payload=new Uint8Array([...bytes(qs[i]),...bytes(qs[(i+2)%3]),...bytes(rs[i]),...bytes(rs[(i+2)%3])]);
  encrypted.push(btoa(String.fromCharCode(...new Uint8Array(await crypto.subtle.encrypt({name:'RSA-OAEP',label},key,payload)))));
 }
 return {commitment,encrypted,salt:salt.toString()};
}
