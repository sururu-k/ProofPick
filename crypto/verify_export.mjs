// Verify the exported proof against its CLAIMED public registry. Registry
// authenticity must be checked against the application/participants separately.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
const file=path.resolve(process.argv[2]);
const report=JSON.parse(fs.readFileSync(file));
const temp=fs.mkdtempSync(path.join(os.tmpdir(),'groupbuy-verify-'));
try{
 const expected={...report.expected,orders:Array.from({length:report.order_count},()=>({}))};
 const target=path.join(temp,'expected.json');fs.writeFileSync(target,JSON.stringify(expected));
 const r=spawnSync(process.execPath,[path.join(import.meta.dirname,'verify.mjs'),file,target],{encoding:'utf8',timeout:60000});
 if(r.status!==0)throw Error(r.stderr||'verification_failed');
 console.log(r.stdout.trim());console.log('Verified against claimed public inputs. Independently authenticate the campaign/order registry before relying on this result.');
}finally{if(path.dirname(path.resolve(temp))!==path.resolve(os.tmpdir())||!path.basename(temp).startsWith('groupbuy-verify-'))throw Error('unexpected_temp_path');fs.rmSync(temp,{recursive:true,force:true});}
