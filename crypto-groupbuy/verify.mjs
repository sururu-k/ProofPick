import fs from 'node:fs';
import {createHash} from 'node:crypto';
import {snarks} from './runtime.mjs';
const manifest=JSON.parse(fs.readFileSync(new URL('artifacts/manifest.json',import.meta.url)));
const raw=fs.readFileSync(new URL('artifacts/verification_key.json',import.meta.url));
if(createHash('sha256').update(raw).digest('hex')!==manifest['verification_key.json'])throw Error('verification_key_digest_mismatch');
const report=JSON.parse(fs.readFileSync(process.argv[2])),expected=JSON.parse(fs.readFileSync(process.argv[3]));
const pub=report.public_inputs;
const total=Number(pub[0]);
if(pub.length!==32 || !Number.isSafeInteger(total)||total<expected.orders.length||total>expected.orders.length*9999 ||
 pub[1]!==String(total*expected.price)||pub[2]!==String(Number(total>=expected.minimum))||pub[3]!==expected.expected_anchor||
 JSON.stringify(pub.slice(4))!==JSON.stringify(expected.expected_tail))throw Error('public_input_binding_failed');
const {groth16}=await snarks();
if(!await groth16.verify(JSON.parse(raw),pub,report.proof))throw Error('groth16_verification_failed');
console.log(JSON.stringify({verified:true,total,amount:Number(pub[1]),eligible:pub[2]==='1'}));process.exit(0);
