---
theme: seriph
title: ProofPick — 商品選択の根拠を証明する
info: |
  ## ProofPick
  理想は「誰でもAIロボを安心して走らせられる社会」。
  その核心「なぜその商品を選んだか」の証明を、まずデモに落とし込んだ。
class: text-center
highlighter: shiki
transition: slide-left
drawings:
  persist: false
---

# ProofPick

「なぜその商品を選んだか」を証明できると、
AIロボットはもっと安心して暮らしに入ってくる

<div class="pt-6 text-sm opacity-70">
理想は「誰でもロボを安心して走らせられる社会」— まずその核心をデモに落とし込みました<br>
第4回 全国情報教育コンテスト（全情コン2026）／愛知県大会 応募作品
</div>

---
layout: section
---

# 理想（ビジョン）

誰でもAIロボを安心して走らせられる社会へ

---

# 理想 — インフラ分離

<div class="grid grid-cols-2 gap-5 pt-4">

<div class="space-y-4">

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-bold text-emerald-300">店舗・倉庫（場の提供者）</div>
<div class="text-sm opacity-80 pt-1">
ロボットを所有しない。「走れる場」と「安全を検証する仕組み」だけを提供。
</div>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-bold text-emerald-300">外部AIロボット（稼働者）</div>
<div class="text-sm opacity-80 pt-1">
自分の技術（知財）は隠したまま稼働し、完了証明を出すたびに報酬を得る。
</div>
</div>

</div>

<div class="rounded-xl bg-slate-800/60 p-5 self-start">
<div class="font-bold mb-2">この理想のねらい</div>
<ul class="text-sm space-y-2 opacity-85">
<li>「店がロボットを買い取る」構造を壊す</li>
<li>同じ仕組みをデータ転用で<b>スーパー・物流・薬局・介護</b>へ横展開できる</li>
<li>AI企業も、店も、客も、損保も、みんな安心できる</li>
</ul>
</div>

</div>

---

# なぜこの理想か — 現場の3つの壁

<div class="grid grid-cols-3 gap-4 pt-4">

<div class="rounded-xl border border-slate-700 p-4">
<div class="text-2xl mb-2">💰</div>
<div class="font-bold mb-1">CAPEX の壁</div>
<div class="text-sm opacity-80">
スーパーや中小物流倉庫が自前でロボットを買い取り、維持管理（修理・AI更新）し続けるのは不可能。
</div>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="text-2xl mb-2">🛡️</div>
<div class="font-bold mb-1">責任の所在が検証できない</div>
<div class="text-sm opacity-80">
AIが商品を誤認したら事故になる。でも「AIのミスか、データの不備か」どこに責任があるのかを第三者が検証できない。
</div>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="text-2xl mb-2">🔒</div>
<div class="font-bold mb-1">監査済みか分からない</div>
<div class="text-sm opacity-80">
AI企業はモデルの中身を見せたくない。でも外部からは「本当に監査済みなのか」を検証できない。
</div>
</div>

</div>

<div class="pt-6 text-sm opacity-70">
この3つの壁は、どれも「信頼をどう証明するか」に行き着く
</div>

---

# 核心は、1つの問い

<div class="grid grid-cols-2 gap-6 pt-6">

<div class="rounded-xl bg-slate-800/60 p-5">
<div class="text-xs uppercase tracking-wide opacity-60 mb-2">最初の問い</div>
<div class="text-lg font-semibold">「どうやって賢い買い物ロボットを<br>作るか？」</div>
</div>

<div class="rounded-xl bg-emerald-900/40 border border-emerald-700 p-5">
<div class="text-xs uppercase tracking-wide opacity-60 mb-2">たどり着いた核心の問い</div>
<div class="text-lg font-semibold">「ロボに“<b>なぜその商品を選んだか</b>”を証明させられれば、店も客も損保も安心できる。その仕組みをどう作るか？」</div>
</div>

</div>

<div class="pt-6 text-sm opacity-75">
つまり「商品選択の根拠」を第三者に示せること。これが ProofPick の核心です。
</div>

---
layout: section
---

# 研究（CSS2026）

核心を実現する要素技術を、最新学会から特定

---

# 核心に必要な要素技術（CSS2026）

<div class="space-y-2 pt-2 text-sm">

<div class="rounded border border-slate-700 p-3"><b>分岐器トリアージ</b> — 定型注文をLLMなしで高速処理（4E3-5 北島・吉塚・宮本・高橋・櫻井）</div>

<div class="rounded border border-slate-700 p-3"><b>ASIDE＋ICA 動的ゲート</b> — 悪意ある指示をデータから分離して無力化（4E3-4 米田・大塚）</div>

<div class="rounded border border-slate-700 p-3"><b>VLA 動的 Action Chunking</b> — 視覚ノイズによる暴走を抑止（2D4-1 山辺・佐久間）</div>

<div class="rounded border border-slate-700 p-3"><b>CNEI モデル外強制</b> — 許可した操作の範囲を超えさせない（1E2-2 中井・東・大西）</div>

<div class="rounded border border-slate-700 p-3"><b>決定論的 Lint（証跡拘束）</b> — 根拠の記録を改ざん・劣化させない（1D2-4 古川・津田・渡邉ら）</div>

<div class="rounded border border-slate-700 p-3"><b>OP-TEE 自動署名</b> — 安全が確認できた時だけ自動で承認（4B2-1 濱口・瀧田・野村ら）</div>

<div class="rounded border border-slate-700 p-3"><b>DCSS 墨塗署名</b> — 機密は隠したまま検証可能に（5B1-4 廣瀬・駒野）</div>

</div>

<div class="pt-4 text-xs opacity-60">
上記は CSS2026 学術論文集の報告手法です。自チームではこれらを調査・選定し、まず核心の1点を形にしました（次のセクション）。
</div>

---
layout: section
---

# 落とし込み（実際に形にしたもの）

理想を、まず「動くデモ」にまで下ろした

---

# 落とし込み — 核心を1つのデモに

<div class="grid grid-cols-2 gap-5 pt-4 items-center">

<div class="space-y-3 text-sm">

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-bold text-slate-100 mb-1">理想は大きい</div>
<div class="opacity-80">インフラ分離・知財秘匿・自動監査。全部やるのは時間がかかる。</div>
</div>

<div class="rounded-xl border border-emerald-700/60 bg-emerald-950/30 p-4">
<div class="font-bold text-emerald-300 mb-1">だから核心1点に絞った</div>
<div class="opacity-80">「<b>なぜその商品を選んだか</b>」の根拠を、画面で見せて記録するデモをブラウザで作った。</div>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-bold text-slate-100 mb-1">ここに暗号はまだ載せていない</div>
<div class="opacity-80">まず「人が分かる形」で核心を提示。証明の強化はこの先（理想）。</div>
</div>

</div>

<div class="text-center">
<div class="text-xs font-mono text-slate-400 mb-2">動作するデモ（右は埋め込み）</div>
<a href="/demo.html" target="_blank" class="text-emerald-300 text-sm hover:underline">→ 別タブで開く</a>
</div>

</div>

---

# デモの流れ（4ステップ）

<div class="grid grid-cols-4 gap-3 pt-4 text-sm">

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-mono text-cyan-300 text-xs mb-1">STEP 1</div>
<b>注文</b><br><span class="opacity-80">「小麦不使用のルー」を注文。氏名・住所は即マスク。</span>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-mono text-purple-300 text-xs mb-1">STEP 2</div>
<b>候補の比較</b><br><span class="opacity-80">小麦あり198円 vs 米粉258円。アレルゲン→価格で比較。</span>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-mono text-emerald-300 text-xs mb-1">STEP 3</div>
<b>根拠付き選択</b><br><span class="opacity-80">「アレルゲン基準に適合」という理由で米粉を選択。</span>
</div>

<div class="rounded-xl border border-slate-700 p-4">
<div class="font-mono text-amber-300 text-xs mb-1">STEP 4</div>
<b>安心バッジ</b><br><span class="opacity-80">「✓基準適合」「✓根拠記録済」を緑バッジで表示。</span>
</div>

</div>

<iframe src="/demo.html" class="mt-5 w-full h-[300px] rounded-xl border border-slate-700 bg-slate-950" loading="lazy"></iframe>

---

# デモが示していること

<div class="space-y-3 pt-3 text-sm">

<div class="rounded border border-slate-700 p-3"><b>専門用語ゼロ</b> — お客さまが見るのは「✓ アレルギー基準適合」の緑バッジだけ。数式は出さない。</div>

<div class="rounded border border-slate-700 p-3"><b>根拠が残る</b> — 裏では「決定証跡」（どの候補を、何の基準で、なぜ選んだか）を記録し、あとから検証できる。</div>

<div class="rounded border border-slate-700 p-3"><b>個人情報を出さない</b> — 注文時点で氏名・住所はマスク。お客さまのプライバシーを守る。</div>

<div class="rounded border border-slate-700 p-3"><b>ここからが「理想」への道</b> — この根拠を暗号で第三者に証明できるようにするのが、次のステップ。</div>

</div>

---
layout: section
---

# 落とし込みの先（理想の全体像）

核心が動いたら、この全体へ拡張する

---

# 理想の全体像（システム構成）

```mermaid {scale: 0.72}
flowchart LR
  subgraph L1[入力層]
    A[注文テキスト<br>店内カメラ・棚札]
  end
  subgraph L2[前段・分岐器]
    B[PII事前マスク]
    C[分岐器 Router]
  end
  subgraph L3[推論・制御]
    D[分散LLM<br>ASIDE+ICA]
    E[VLA動的<br>Action Chunking]
  end
  subgraph L4[Lookup証明・TEE]
    F[商品LUT参照証明]
    G[OP-TEE + CNEI<br>操作上限強制]
  end
  subgraph L5[チェーン・保険監査]
    H[報酬自動決済]
    I[平時 無開示査定<br>有事 開示検証]
  end
  A --> B --> C
  C -- 定型 --> F
  C -- 非定型 --> D --> E --> F
  F --> G --> H --> I
```

---

# 作るもの：3点セット

<div class="grid grid-cols-3 gap-4 pt-4">

<div class="rounded-xl border border-cyan-700/60 p-4">
<div class="font-bold text-cyan-300 mb-2">① 実行基盤</div>
<div class="text-sm opacity-80">
店舗・倉庫に常設するインフラ。分岐器・PIIマスク・操作上限強制でモデルの外から安全を担保。
</div>
</div>

<div class="rounded-xl border border-purple-700/60 p-4">
<div class="font-bold text-purple-300 mb-2">② 標準モデル</div>
<div class="text-sm opacity-80">
ロボットに搭載するベースラインAI。悪意ある指示の無力化と、視覚ノイズによる暴走の抑止。
</div>
</div>

<div class="rounded-xl border border-amber-700/60 p-4">
<div class="font-bold text-amber-300 mb-2">③ 根拠の証明（本デモ）</div>
<div class="text-sm opacity-80">
「なぜ選んだか」を記録・提示する画面。まずはここを形にした。
</div>
</div>

</div>

---

# 展望 — どこへ広がるか

<div class="space-y-3 pt-3 text-sm">

<div class="rounded border border-slate-700 p-3"><b>病院・薬局の調剤</b> — 処方ミスゼロを、データを隠したまま証明。</div>

<div class="rounded border border-slate-700 p-3"><b>介護施設の見守り・配膳</b> — プライバシー映像を漏らさず、安全な行動だけを家族・保険会社へ証明。</div>

<div class="rounded border border-slate-700 p-3"><b>物流・自動運転・ドローン</b> — 事故時に、警察や裁判所だけが検証できる基盤へ。</div>

</div>

<div class="pt-6 text-sm opacity-80">
同じ「実行基盤＋根拠の証明」を、シーン別データに差し替えるだけで横展開できる。
</div>

---

# 各賞へのマッピング

<div class="space-y-3 pt-3 text-sm">

<div class="rounded border border-slate-700 p-3"><b>ソフトバンク AIチャレンジ賞</b> — AIに丸投げせず「判断理由」を証明する設計。質疑ではCSS2026の理解で応答。</div>

<div class="rounded border border-slate-700 p-3"><b>東進 AIデータサイエンス賞</b> — 情報Ⅱの探究4プロセス（課題設定→収集→分析→表現）を実践。</div>

<div class="rounded border border-slate-700 p-3"><b>スペースブロック クリエイティブイノベーション賞</b> — モノ（ロボット）× デジタル（証明）を、実際のデモまで落とし込んだ。</div>

<div class="rounded border border-slate-700 p-3"><b>SAMURAIチャレンジ賞／やりたいをカタチに賞</b> — 「店がロボットを買い取る」常識を壊す発想を、動く形にした挑戦。</div>

</div>

---
layout: section
---

# 探究のプロセス

情報Ⅱの4プロセスに沿って

---

# 探究の4プロセス

<div class="grid grid-cols-4 gap-3 pt-4 text-sm">

<div class="rounded-xl border border-slate-700 p-3"><b>① 課題設定</b><br><span class="opacity-80">街の配膳・清掃ロボを見て「間違った商品を届けたら怖い」と疑問を持つ</span></div>

<div class="rounded-xl border border-slate-700 p-3"><b>② 収集</b><br><span class="opacity-80">CSS2026論文を調査し、核心に必要な要素技術を特定</span></div>

<div class="rounded-xl border border-slate-700 p-3"><b>③ 分析</b><br><span class="opacity-80">「全部やるのは無理」と判明 → 「根拠の証明」が本質と気づく</span></div>

<div class="rounded-xl border border-slate-700 p-3"><b>④ 表現</b><br><span class="opacity-80">核心を「商品選択の根拠」デモとして形にした</span></div>

</div>

<div class="pt-6 text-sm opacity-80">
<b>次にやりたいこと</b>：実店舗での試用 → 損保会社との共同実証 → 暗号による証明の強化
</div>

---

# 倫理・プライバシーへの配慮

<div class="space-y-3 pt-2 text-sm">

<div class="rounded border border-slate-700 p-3"><b>プライバシー</b> — 氏名・住所は注文時点でマスク。生データは外部へ出さない。</div>

<div class="rounded border border-slate-700 p-3"><b>著作権・出典</b> — OSSはライセンス準拠、CSS2026の手法は出典を明記。</div>

<div class="rounded border border-slate-700 p-3"><b>データ安全</b> — 決定証跡は改ざんできない形で記録し、権限のある人だけが検証できる。</div>

<div class="rounded border border-slate-700 p-3"><b>AI倫理</b> — AIに判断を丸投げせず、根拠を残すことで説明責任を果たす。</div>

</div>

---
layout: center
---

# まとめ

<div class="text-left max-w-3xl mx-auto space-y-3 pt-4 text-sm opacity-90">

<div>ProofPick は、<b>「なぜその商品を選んだか」を証明できる</b>という核心から始まります。</div>

<div>理想は「誰でもAIロボを安心して走らせられる社会」。まずその核心を<b>動くデモ</b>に落とし込みました。</div>

<div>ここから、暗号による証明の強化と、実行基盤全体への拡張へ進みます。</div>

</div>

<div class="pt-8 text-xs opacity-60">
デモ: html/demo.html ／ リポジトリ: github.com/sururu-k/ProofPick
</div>