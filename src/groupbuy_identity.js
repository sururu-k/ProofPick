// ProofPick OAuth + DPoP client for the local PASTA demo.
const issuer='http://localhost:3000', client='proofpick', redirect=location.origin+'/';
const enc=new TextEncoder();
const b64=bytes=>btoa(String.fromCharCode(...new Uint8Array(bytes))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
const text64=s=>b64(enc.encode(s));
const random=()=>b64(crypto.getRandomValues(new Uint8Array(24)));
async function keypair(){
 const db=await new Promise((resolve,reject)=>{const r=indexedDB.open('proofpick-identity',1);r.onupgradeneeded=()=>r.result.createObjectStore('keys');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
 try{
  let pair=await new Promise((resolve,reject)=>{const r=db.transaction('keys').objectStore('keys').get('dpop');r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error)});
  if(!pair){pair=await crypto.subtle.generateKey('Ed25519',false,['sign','verify']);await new Promise((resolve,reject)=>{const t=db.transaction('keys','readwrite');t.objectStore('keys').put(pair,'dpop');t.oncomplete=resolve;t.onerror=()=>reject(t.error)})}
  const k=await crypto.subtle.exportKey('jwk',pair.publicKey), jwk={crv:k.crv,kty:k.kty,x:k.x};
  return {pair,jwk,jkt:b64(await crypto.subtle.digest('SHA-256',enc.encode(JSON.stringify(jwk))))};
 }finally{db.close()}
}
async function proof(material,htu,accessToken){
 const header={typ:'dpop+jwt',alg:'EdDSA',jwk:material.jwk};
 const payload={jti:random(),htm:'POST',htu,iat:Math.floor(Date.now()/1000)};
 if(accessToken)payload.ath=b64(await crypto.subtle.digest('SHA-256',enc.encode(accessToken)));
 const input=text64(JSON.stringify(header))+'.'+text64(JSON.stringify(payload));
 return input+'.'+b64(await crypto.subtle.sign('Ed25519',material.pair.privateKey,enc.encode(input)));
}
const config=await (await fetch('/identity-config')).json();
let token=sessionStorage.getItem('proofpick-id-token')||'';
let material;
export let identityError='';
try {
if(config.enabled){
 material=await keypair();
 const params=new URLSearchParams(location.search);
 if(params.has('code')||params.has('error')){
  const saved=sessionStorage.getItem('proofpick-id-state');sessionStorage.removeItem('proofpick-id-state');
  history.replaceState(null,'',location.pathname+location.hash);
  if(params.get('error')||!saved||params.get('state')!==saved)throw Error('認証が拒否されたか、state が一致しません。再ログインしてください。');
  const response=await fetch(issuer+'/token',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded','DPoP':await proof(material,issuer+'/token')},body:new URLSearchParams({grant_type:'authorization_code',code:params.get('code'),client_id:client,redirect_uri:redirect})});
  const result=await response.json();if(!response.ok||!result.access_token)throw Error('トークン取得に失敗しました。');
  token=result.access_token;sessionStorage.setItem('proofpick-id-token',token);
 }
}
} catch (error) { identityError=error.message; sessionStorage.removeItem('proofpick-id-token'); token=''; }
export const identityEnabled=config.enabled;
export function identitySubject(){try{const p=token.split('.')[1].replace(/-/g,'+').replace(/_/g,'/');return JSON.parse(new TextDecoder().decode(Uint8Array.from(atob(p),c=>c.charCodeAt(0)))).sub||''}catch{return ''}}
export async function login(){
 if(!material)material=await keypair();
 const state=random();sessionStorage.setItem('proofpick-id-state',state);
 sessionStorage.removeItem('proofpick-id-token');
 const url=new URL(issuer+'/authorize');url.search=new URLSearchParams({response_type:'code',client_id:client,redirect_uri:redirect,scope:'openid profile',state,dpop_jkt:material.jkt});location.assign(url);
}
export function logout(){sessionStorage.removeItem('proofpick-id-token');location.reload()}
export async function authenticatedFetch(url, options){
 if(!config.enabled)return fetch(url,options);
 if(!token)throw Error('先に分散IDでログインしてください。');
 const target=new URL(url,location.origin).href;
 return fetch(url,{...options,headers:{...options.headers,'X-Identity-Token':token,'DPoP':await proof(material,target,token)}});
}
