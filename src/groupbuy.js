'use strict';
import {prepareMpc,poseidon4,tag} from './groupbuy_mpc.js';
import {identityEnabled,identitySubject,identityError,login,logout,authenticatedFetch} from './groupbuy_identity.js';
const $=id=>document.getElementById(id), enc=new TextEncoder(), dec=new TextDecoder();
const statuses={OPEN:'受付中',CLOSED:'締切・販売者の確認待ち',ORDERED:'発注済み',READY:'受け取り待ち',COMPLETED:'全員の受け取りを記録済み',FAILED:'不成立',SUBMITTED:'注文受付済み',CANCELLED:'取消済み',RECEIVED:'受け取り済み'};
let campaign='', token='', view=null, opened=null, verifiedSnapshot=null;
const random=()=>Array.from(crypto.getRandomValues(new Uint8Array(24)),b=>b.toString(16).padStart(2,'0')).join('');
const b64=b=>btoa(String.fromCharCode(...new Uint8Array(b)));
const unb64=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const read=key=>JSON.parse(localStorage.getItem('groupbuy:'+key)||'null');
const save=(key,v)=>localStorage.setItem('groupbuy:'+key,JSON.stringify(v));
function message(t){$('notice').textContent=t;}
async function api(action,data={},credential=token){const r=await authenticatedFetch('/api/'+action,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+credential},body:JSON.stringify({campaign,...data})});const v=await r.json();if(!r.ok)throw Error(v.error);return v;}
function link(cid,secret=''){return location.origin+'/#'+new URLSearchParams({campaign:cid,...(secret?{token:secret}:{})});}
function download(name,data){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);}
function buyerKey(cid){return 'buyer:'+cid+(identityEnabled?':'+identitySubject():'');}
function buyerAccess(){let b=read(buyerKey(campaign));if(!b){b={kind:'buyer',campaign,token:random(),id:random(),version:0};save(buyerKey(campaign),b);}return b;}
function cost(){if(!view)return;const n=Number($('quantity').value);$('cost').textContent='注文金額：'+(n*view.price).toLocaleString()+'円';}
async function refresh(){
 view=await api('view');opened=null;verifiedSnapshot=null;$('decrypted').textContent='';
 $('workspace').hidden=false;$('start').hidden=true;$('campaignInput').value=campaign;
 $('campaignTitle').textContent=view.title;$('terms').textContent=view.product+' / '+view.price+'円 / 合計'+view.minimum+'個から成立 / 締切 '+new Date(view.deadline*1000).toLocaleString();
 $('state').textContent=statuses[view.state];$('count').textContent='取消を除く注文：'+view.order_count+'件';$('joinLink').value=link(campaign);
 $('proofState').textContent=view.proof?'ZK検証済み：合計 '+view.proof.total+'個 / '+view.proof.amount+'円 / '+(view.proof.eligible?'成立数量に達しています':'成立数量に届いていません')+'\n3者で秘密集計・共同証明 → 別実装で検証（'+Math.round(view.proof.elapsed_ms)+' ms）':'秘密集計はまだ行っていません。締切後に2〜8件をまとめて計算します。';
 $('role').textContent={owner:'主催者：注文内容は見えません',seller:'販売者：端末で注文を復号します',buyer:'参加者：自分の注文を操作します'}[view.role];
 for(const role of ['owner','seller','buyer'])$(role).hidden=role!==view.role;
 $('history').textContent=view.events?view.events.map(e=>new Date(e.at*1000).toLocaleString()+' '+({created:'募集作成',submitted:'注文受付',updated:'注文変更',cancel:'取消',closed:'受付終了',placed:'発注確定',ready:'準備完了',receive:'受け取り',failed:'不成立'}[e.action]||e.action)+(e.order_id?' / '+e.order_id.slice(0,8):'')).join('\n'):'ほかの参加者の操作履歴は公開しません。';
 $('ownerState').textContent=JSON.stringify(view.orders.map(o=>({受付ID:o.id,状態:statuses[o.state]})),null,2);
 if(view.role==='buyer'){const b=buyerAccess();if(!token){token=b.token;view=await api('view');}const own=view.orders.find(o=>o.id===b.id);if(own){b.version=own.version;save(buyerKey(campaign),b);}$('buyerState').textContent=own?'受付ID：'+own.id+'\n状態：'+statuses[own.state]:'まだ注文していません。';}
 cost();
 const credentials=read('seller:'+campaign);$('access').hidden=!credentials || view.role!=='seller';
 if(credentials){$('ownerLink').value=link(campaign,credentials.owner_token);$('sellerLink').value=link(campaign,credentials.seller_token);}
}
async function go(cid,secret=''){campaign=cid;token=secret;const known=read(buyerKey(cid));if(!token&&known)token=known.token;history.replaceState(null,'',link(cid,secret));await refresh();}
async function create(){
 const keys=await crypto.subtle.generateKey({name:'RSA-OAEP',modulusLength:2048,publicExponent:new Uint8Array([1,0,1]),hash:'SHA-256'},true,['encrypt','decrypt']);
 const public_key=await crypto.subtle.exportKey('jwk',keys.publicKey),private_key=await crypto.subtle.exportKey('jwk',keys.privateKey);
 const d={title:$('title').value,product:$('product').value,price:Number($('price').value),minimum:Number($('minimum').value),deadline:Math.floor(new Date($('deadline').value).getTime()/1000),public_key};
 const r=await authenticatedFetch('/api/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});const v=await r.json();if(!r.ok)throw Error(v.error);
 save('seller:'+v.id,{kind:'seller',campaign:v.id,private_key,...v});await go(v.id,v.seller_token);message('募集を作成しました。販売者の鍵を保存し、主催者用リンクと参加者用リンクを渡してください。');
}
async function order(){
 const quantity=Number($('quantity').value),budget=Number($('budget').value);
 if(!Number.isSafeInteger(quantity)||quantity<1||quantity>9999||!Number.isSafeInteger(budget)||budget<quantity*view.price)throw Error('数量は1〜9999の整数にしてください。注文金額が予算を超える場合は送信しません。');
 const b=buyerAccess();if(token!==b.token)throw Error('この端末の注文アクセス情報と一致しません。保存ファイルから復元してください。');
 const payload={c:campaign,o:b.id,q:quantity,p:view.price};
 const key=await crypto.subtle.importKey('jwk',view.public_key,{name:'RSA-OAEP',hash:'SHA-256'},false,['encrypt']);
 // Reuse the same ciphertext/version after a network failure, preventing duplicate submission.
 let pending=read('pending:'+campaign);
 const plain=JSON.stringify(payload);
 if(!pending||pending.plain!==plain||pending.version!==b.version||!pending.mpc){
  if(!view.mpc_keys)throw Error('旧版の募集です。新しく募集を作成してください。');
  const shares=await prepareMpc(campaign,b.id,b.version+1,quantity,view.mpc_context,view.mpc_keys);
  pending={plain,version:b.version,mpc:{commitment:shares.commitment,encrypted:shares.encrypted},
   ciphertext:b64(await crypto.subtle.encrypt({name:'RSA-OAEP'},key,enc.encode(JSON.stringify({...payload,s:shares.salt}))))};
 }
 save('pending:'+campaign,pending);
 const result=await api('order',{id:b.id,ciphertext:pending.ciphertext,version:pending.version,mpc:pending.mpc},b.token);
 b.version=result.version;save(buyerKey(campaign),b);localStorage.removeItem('groupbuy:pending:'+campaign);
 await refresh();message('注文を保存しました。予算は送信していません。注文のアクセス情報を保存してください。');
}
async function decrypt(){
 await refresh();
 if(!view.proof?.verified)throw Error('先に「秘密のまま集計・ZK検証」を実行してください。');
 if(!view.proof.eligible)throw Error('成立数量に届いていません。個別注文は販売者に開示しません。');
 const credentials=read('seller:'+campaign);if(!credentials)throw Error('販売者の鍵ファイルを復元してください。');
 const key=await crypto.subtle.importKey('jwk',credentials.private_key,{name:'RSA-OAEP',hash:'SHA-256'},false,['decrypt']);
 const items=[];
 for(const o of view.orders.filter(o=>o.state!=='CANCELLED')){
  let p;try{p=JSON.parse(dec.decode(await crypto.subtle.decrypt({name:'RSA-OAEP'},key,unb64(o.ciphertext))));}catch{throw Error('注文 '+o.id.slice(0,8)+' を開けません。発注を止めました。');}
  if(p.c!==campaign||p.o!==o.id||p.p!==view.price||!Number.isInteger(p.q)||p.q<1||p.q>9999)throw Error('注文の内容または募集との対応が不正です。発注を止めました。');
  if(typeof p.s!=='string'||!/^\d{1,77}$/.test(p.s)||await poseidon4([view.mpc_context,await tag(o.id),p.q,p.s])!==o.commitment)throw Error('販売者向けの注文と秘密集計の入力が一致しません。発注を止めました。');
  items.push({order:o.id,quantity:p.q,amount:p.q*p.p});
 }
 const total=items.reduce((n,o)=>n+o.quantity,0);
 if(total!==view.proof.total||total*view.price!==view.proof.amount)throw Error('発注内容とZK検証済み合計が一致しません。');
 opened={campaign,product:view.product,unit_price:view.price,total_quantity:total,total_yen:total*view.price,orders:items,kind:'purchase-order',payment:'実決済は行っていません'};
 verifiedSnapshot=view.snapshot;
 $('decrypted').textContent=items.map(o=>'受付 '+o.order.slice(0,8)+'：'+o.quantity+'個 / '+o.amount+'円').join('\n')+'\n合計 '+total+'個 / '+total*view.price+'円\n'+(total>=view.minimum?'成立数量を満たしています。':'成立数量に届いていません。');
}
async function place(){if(!opened||!verifiedSnapshot)throw Error('先に注文を開いて確認してください。');if(opened.total_quantity<view.minimum)throw Error('成立数量に届いていません。');const po=opened;await api('place',{orders:po.orders.map(o=>o.order),snapshot:verifiedSnapshot});save('po:'+campaign,po);await refresh();message('発注を確定しました。発注書を保存できます。外部への送信や支払いは行っていません。');}
async function restore(file){if(!file)return;const d=JSON.parse(await file.text());if(typeof d.campaign!=='string')throw Error('保存ファイルが不正です。');if(d.kind==='seller'&&d.private_key&&d.seller_token){save('seller:'+d.campaign,d);await go(d.campaign,d.seller_token);}else if(d.kind==='buyer'&&d.id&&d.token){save(buyerKey(d.campaign),d);await go(d.campaign,d.token);}else throw Error('鍵または注文アクセス情報がありません。');message('アクセス情報を復元しました。');}
function bind(id,fn){$(id).addEventListener('click',async()=>{const button=$(id);button.disabled=true;message('処理しています…');try{await fn();if($('notice').textContent==='処理しています…')message('完了しました。');}catch(e){message(e.message);}finally{button.disabled=false;}});}
bind('create',create);bind('open',()=>go($('campaignInput').value.trim(),$('tokenInput').value.trim()));bind('refresh',refresh);bind('submitOrder',order);
bind('backup',()=>download('seller-key-'+campaign+'.json',read('seller:'+campaign)));bind('buyerBackup',()=>download('order-access-'+campaign+'.json',buyerAccess()));
bind('cancel',async()=>{await api('cancel',{id:buyerAccess().id});await refresh();});bind('receive',async()=>{await api('receive',{id:buyerAccess().id});await refresh();});
bind('close',async()=>{await api('close');await refresh();});bind('decrypt',decrypt);bind('place',place);
bind('aggregate',async()=>{message('3者で秘密集計と証明生成を実行しています。個別数量は復元しません。');await api('aggregate');await refresh();message('秘密集計の結果をZK検証しました。販売者は注文を開いて発注へ進めます。');});
bind('proofDownload',()=>{if(!view.proof)throw Error('先に秘密集計してください。');download('groupbuy-proof-'+campaign+'.json',view.proof);});
bind('export',()=>{const po=read('po:'+campaign);if(!po)throw Error('この端末で発注を確定してから保存してください。');download('purchase-order-'+campaign+'.json',po);});
bind('ready',async()=>{await api('ready');await refresh();});bind('fail',async()=>{await api('fail');await refresh();});
for(const id of ['restore','restoreAny'])$(id).addEventListener('change',async e=>{try{await restore(e.target.files[0]);}catch(err){message(err.message);}});
$('quantity').addEventListener('input',cost);
const tomorrow=new Date(Date.now()+86400000);$('deadline').value=new Date(tomorrow-tomorrow.getTimezoneOffset()*60000).toISOString().slice(0,16);
const h=new URLSearchParams(location.hash.slice(1));if(h.get('campaign'))go(h.get('campaign'),h.get('token')||'').catch(e=>message(e.message));
window.addEventListener('hashchange',()=>{const next=new URLSearchParams(location.hash.slice(1));if(next.get('campaign'))go(next.get('campaign'),next.get('token')||'').catch(e=>message(e.message));});

$('identityPanel').hidden=!identityEnabled;
if(identityError)message('分散ID: '+identityError);
if(identityEnabled){$('identityState').textContent=identitySubject()?'ログイン中：'+identitySubject():'ログインが必要です';$('identityLogin').addEventListener('click',()=>login().catch(e=>message(e.message)));$('identityLogout').addEventListener('click',logout);}
