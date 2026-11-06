import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {createHash,randomBytes} from 'node:crypto';
import {snarks} from './runtime.mjs';
const require=createRequire(import.meta.url), root=path.resolve(import.meta.dirname,'..');
process.chdir(root);
const {CircomRunner,bindings}=require('../.tools/fhe-runtime/node_modules/circom2');
const output='crypto-groupbuy/artifacts';fs.mkdirSync(output,{recursive:true});
fs.mkdirSync('.work',{recursive:true});
const dir=fs.mkdtempSync('.work/groupbuy-setup-');
const runner=new CircomRunner({args:['crypto-groupbuy/purchase.circom','--r1cs','--wasm','--sym','-l','.tools/fhe-runtime/node_modules/circomlib/circuits','-o',dir],env:process.env,preopens:{'.':'.'},bindings:{...bindings,fs}});
await runner.execute(fs.readFileSync(require.resolve('../.tools/fhe-runtime/node_modules/circom2/circom.wasm')));
const {zKey,powersOfTau}=await snarks();
let ptau='.work/crypto-next/local-final.ptau';
const sha=x=>createHash('sha256').update(x).digest('hex');
if(!fs.existsSync(ptau)){
 const {getCurveFromName}=require('../.tools/fhe-runtime/node_modules/ffjavascript');
 const curve=await getCurveFromName('bn128',true);
 await powersOfTau.newAccumulator(curve,13,dir+'/initial.ptau');
 await powersOfTau.contribute(dir+'/initial.ptau',dir+'/contributed.ptau','local-development-only',randomBytes(64).toString('hex'));
 ptau=dir+'/final.ptau';await powersOfTau.preparePhase2(dir+'/contributed.ptau',ptau);
}
// Development-only setup. No claim of an independent ceremony.
await zKey.newZKey(dir+'/purchase.r1cs',ptau,'.work/groupbuy-initial.zkey');
await zKey.contribute('.work/groupbuy-initial.zkey',dir+'/purchase.zkey','local-development-only',randomBytes(64).toString('hex'));
fs.writeFileSync(dir+'/verification_key.json',JSON.stringify(await zKey.exportVerificationKey(dir+'/purchase.zkey')));
// Reuse the exact Circomlib parameters in the browser, with attribution.
const constants=JSON.parse(fs.readFileSync('.tools/fhe-runtime/node_modules/circomlibjs/src/poseidon_constants.json'));
fs.mkdirSync('prototype/groupbuy-vendor',{recursive:true});
fs.writeFileSync('prototype/groupbuy-vendor/poseidon.json',JSON.stringify({C:constants.C[3],M:constants.M[3]}));
fs.copyFileSync('crypto-groupbuy/LICENSE-GPL','prototype/groupbuy-vendor/CIRCOMLIBJS-LICENSE');
const files=['purchase.zkey','verification_key.json','purchase_js/purchase.wasm'];
for(const n of [...files,'purchase.r1cs','purchase.sym']){fs.mkdirSync(path.dirname(output+'/'+n),{recursive:true});fs.copyFileSync(dir+'/'+n,output+'/'+n);}
const manifest=Object.fromEntries(files.map(n=>[n,sha(fs.readFileSync(output+'/'+n))]));
manifest['../purchase.circom']=sha(fs.readFileSync('crypto-groupbuy/purchase.circom'));
fs.writeFileSync(output+'/manifest.json',JSON.stringify(manifest,null,2));
console.log('Group-purchase circuit and development proving key ready');process.exit(0);
