import os from 'node:os';
const cpus=os.cpus.bind(os);os.cpus=()=>cpus().slice(0,2);
export async function snarks(){return import('../.tools/fhe-runtime/node_modules/snarkjs/main.js');}
