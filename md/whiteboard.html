<!DOCTYPE html>
<html lang="ja" class="dark">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>オープンロボット実行基盤 & ZK/vFHE/監査インフラ統合ホワイトボード (PNG図解・CSS2026・ビジネスモデル完全統合版)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Noto+Sans+JP:wght@400;500;700&display=swap');
    body {
      font-family: 'Inter', 'Noto Sans JP', sans-serif;
      background-color: #020617;
      color: #e2e8f0;
      overflow: hidden;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    .canvas-grid {
      background-size: 32px 32px;
      background-image: 
        linear-gradient(to right, rgba(30, 41, 59, 0.35) 1px, transparent 1px),
        linear-gradient(to bottom, rgba(30, 41, 59, 0.35) 1px, transparent 1px);
    }
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #0f172a;
    }
    ::-webkit-scrollbar-thumb {
      background: #334155;
      border-radius: 3px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #475569;
    }
  </style>
</head>
<body class="h-screen w-screen flex flex-col select-none">

  <!-- Top Header -->
  <header class="h-14 border-b border-slate-800 bg-slate-900/95 backdrop-blur px-4 flex items-center justify-between shrink-0 z-30">
    <div class="flex items-center space-x-3">
      <div class="w-3 h-3 rounded-full bg-emerald-500 shadow-sm shadow-emerald-500/50 animate-pulse"></div>
      <h1 class="text-sm font-bold tracking-wide text-slate-100">
        ホワイトボード統合設計: <span class="text-emerald-400 font-mono">物流・店舗ロボット実行基盤 × Verifiable FHE (ZK+FHE) × AIエージェント保険 (ZK, or not ZK)</span>
      </h1>
      <span class="text-[11px] px-2 py-0.5 rounded bg-amber-950/70 text-amber-300 border border-amber-700/50 font-mono">PNG 3枚 + CSS2026 + 実行基盤モック</span>
    </div>

    <!-- View Switcher & Action Tools -->
    <div class="flex items-center space-x-2">
      <!-- Domain Filter Dropdown -->
      <div class="flex items-center space-x-1.5 mr-2">
        <span class="text-[11px] text-slate-400 font-mono uppercase">レイヤ絞り込み:</span>
        <select id="domainFilterSelect" onchange="filterByDomain(this.value)" class="bg-slate-800 border border-slate-700 rounded text-xs text-slate-200 px-2.5 py-1 focus:outline-none focus:border-emerald-500">
          <option value="all">全レイヤ表示 (ALL PIPELINES)</option>
          <option value="biz_econ">⓪ 収益化・資本効率モデル (インフラ分離 &amp; 知財秘匿)</option>
          <option value="png_core">🖼️ PNG原案: vFHE (ZK+FHE) &amp; 手書きホワイトボード保険設計</option>
          <option value="triage">① 前段・分岐器 &amp; PIIマスク (Router / Triage)</option>
          <option value="llm_vla">② 分散LLM・標準モデル &amp; 対インジェクション・VLA制御</option>
          <option value="lookup_zk">③ 商品Lookup数学的証明 &amp; CNEI強制</option>
          <option value="chain">④ 店舗・物流オープンチェーン &amp; 漸進的トラスト(MPT)</option>
          <option value="insurance">⑤ 顧客トラスト検証 × ZK/第三者監査(DCSS) 保険モデル</option>
        </select>
      </div>

      <div class="flex bg-slate-800 p-0.5 rounded-lg border border-slate-700 text-xs font-medium">
        <button id="viewBtnGraph" onclick="switchView('graph')" class="px-3 py-1.5 rounded-md bg-emerald-600 text-white transition-all shadow-sm">
          ホワイトボード構成図
        </button>
        <button id="viewBtnNotes" onclick="switchView('notes')" class="px-3 py-1.5 rounded-md text-slate-400 hover:text-slate-200 transition-all">
          PNG 3枚図解 &amp; ビジネス・CSS2026着想表
        </button>
        <button id="viewBtnExport" onclick="switchView('export')" class="px-3 py-1.5 rounded-md text-slate-400 hover:text-slate-200 transition-all">
          仕様書出力 (Markdown / JSON)
        </button>
      </div>

      <div class="h-4 w-px bg-slate-800 mx-1"></div>

      <button onclick="resetZoom()" class="px-2.5 py-1 text-xs font-mono rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-300 transition-colors">
        表示リセット
      </button>
      <button onclick="openAddNodeModal()" class="px-3 py-1 text-xs font-medium rounded bg-indigo-600 hover:bg-indigo-500 text-white transition-colors">
        + ノード追加
      </button>
    </div>
  </header>

  <!-- Main Workspace Container -->
  <div class="flex-1 relative overflow-hidden flex">

    <!-- 1. Interactive Graph Canvas View -->
    <main id="viewGraph" class="flex-1 relative overflow-hidden canvas-grid">
      <!-- Flow Legend HUD -->
      <div class="absolute top-4 right-4 z-20 bg-slate-900/90 backdrop-blur-md border border-slate-800 p-3.5 rounded-xl text-xs space-y-2 shadow-2xl max-w-xs">
        <div class="font-bold text-slate-200 pb-1.5 border-b border-slate-800 flex items-center justify-between">
          <span>アーキテクチャ &amp; PNG統合レイヤ</span>
          <span class="text-[10px] font-mono text-emerald-400">14 Nodes</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500 shrink-0"></span>
          <span class="text-slate-200 font-semibold">00. 収益化・資本効率モデル (インフラ分離)</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-cyan-400 shrink-0"></span>
          <span class="text-cyan-300 font-semibold">🖼️ PNG原案: vFHE &amp; 損保ホワイトボード</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-amber-500 shrink-0"></span>
          <span class="text-slate-300">01. 場の考慮・PIIマスク &amp; 分岐器トリアージ</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-purple-500 shrink-0"></span>
          <span class="text-slate-300">02. 標準/独自LLM &amp; 動的チャンク制御</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-sky-500 shrink-0"></span>
          <span class="text-slate-300">03. モデル知財秘匿 × Lookup証明 &amp; CNEI強制</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-indigo-500 shrink-0"></span>
          <span class="text-slate-300">04. 店舗/物流チェーン・インセンティブ決済</span>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2.5 h-2.5 rounded-full bg-teal-500 shrink-0"></span>
          <span class="text-slate-300">05. 顧客トラスト検証 × ZK/第三者監査保険</span>
        </div>
        <div class="pt-1.5 border-t border-slate-800/80 text-[11px] text-slate-400 leading-relaxed">
          💡 <strong>「PNG 3枚図解 &amp; 着想表」タブ</strong>で、`image.png` / `image copy.png` / `image copy 2.png` の実画像と完全書き起こしを確認できます。
        </div>
      </div>

      <!-- Bottom Quick Summary HUD -->
      <div class="absolute bottom-4 left-4 z-20 bg-slate-900/95 backdrop-blur-md border border-slate-800 px-4 py-2.5 rounded-xl text-xs flex items-center space-x-5 shadow-xl">
        <div>
          <span class="text-cyan-400 block text-[10px] font-mono font-bold">image.png (Verifiable FHE)</span>
          <span class="text-slate-200 font-semibold">User(秘密x) → E(x) → Server FHE評価 → E(f(x))+π (機密性+計算の正しさ)</span>
        </div>
        <div class="h-6 w-px bg-slate-800"></div>
        <div>
          <span class="text-teal-400 block text-[10px] font-mono font-bold">image copy.png &amp; copy 2.png (AI保険ホワイトボード)</span>
          <span class="text-slate-200 font-semibold">(task, trace=APIコールlist)をMPC/FHEで暗号化check・事故率/成功率/約款合致を損保へ証明</span>
        </div>
        <div class="h-6 w-px bg-slate-800"></div>
        <div>
          <span class="text-rose-400 block text-[10px] font-mono font-bold">物流・店舗インフラ分離</span>
          <span class="text-slate-200 font-semibold">実行基盤 ＋ 標準モデル ＋ ピックアップモック実演</span>
        </div>
      </div>

      <!-- SVG Connections Layer -->
      <svg id="connectionsLayer" class="absolute inset-0 w-full h-full pointer-events-none z-0">
        <defs>
          <marker id="arrow" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748b" />
          </marker>
        </defs>
      </svg>

      <!-- Draggable Nodes Container -->
      <div id="nodesContainer" class="absolute inset-0 w-full h-full z-10 origin-top-left"></div>
    </main>

    <!-- 2. Structured Notes & PNG Gallery & CSS2026 Matrix View -->
    <section id="viewNotes" class="hidden flex-1 overflow-y-auto p-8 bg-slate-950 select-text">
      <div id="notesContent" class="max-w-6xl mx-auto space-y-8 pb-16"></div>
    </section>

    <!-- 3. Markdown / JSON Export View -->
    <section id="viewExport" class="hidden flex-1 overflow-y-auto p-8 bg-slate-950 select-text">
      <div class="max-w-5xl mx-auto space-y-6 pb-16">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-lg font-bold text-slate-100">ホワイトボード完全仕様書エクスポート (Markdown / JSON)</h2>
            <p class="text-xs text-slate-400">PNG 3枚の内容・ビジネスモデル・CSS2026着想をすべて含んだ完全仕様書です。</p>
          </div>
          <div class="space-x-2">
            <button onclick="copyExport('md')" class="px-3 py-1.5 rounded bg-emerald-600 hover:bg-emerald-500 text-xs font-medium text-white">Markdownをコピー</button>
            <button onclick="copyExport('json')" class="px-3 py-1.5 rounded bg-slate-800 hover:bg-slate-700 border border-slate-700 text-xs font-mono text-slate-200">JSONをコピー</button>
          </div>
        </div>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="text-xs font-mono text-emerald-400 uppercase">Markdown Specification</label>
            <textarea id="exportMarkdownArea" readonly class="w-full h-[600px] bg-slate-900 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-200 focus:outline-none"></textarea>
          </div>
          <div class="space-y-2">
            <label class="text-xs font-mono text-sky-400 uppercase">Nodes &amp; Edges Graph JSON</label>
            <textarea id="exportJsonArea" readonly class="w-full h-[600px] bg-slate-900 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 focus:outline-none"></textarea>
          </div>
        </div>
      </div>
    </section>

    <!-- Right Detail Drawer -->
    <aside id="detailDrawer" class="w-96 border-l border-slate-800 bg-slate-900/95 backdrop-blur-md p-6 overflow-y-auto shrink-0 z-20 hidden select-text">
      <div class="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
        <span id="drawerCategory" class="text-[10px] font-mono uppercase px-2 py-0.5 rounded">Category</span>
        <button onclick="closeDetailDrawer()" class="text-slate-400 hover:text-slate-200 text-sm font-mono">✕ 閉じる</button>
      </div>
      <h3 id="drawerTitle" class="text-base font-bold text-slate-100 mb-1"></h3>
      <p id="drawerSubtitle" class="text-xs font-mono text-emerald-400 mb-4"></p>
      <div id="drawerPaperBadge" class="mb-4 p-2.5 rounded-lg bg-slate-950 border border-slate-800 text-[11px] text-slate-300 font-mono"></div>
      <p id="drawerDesc" class="text-xs text-slate-300 leading-relaxed mb-5"></p>
      <div class="space-y-2 mb-6">
        <h4 class="text-xs font-bold text-slate-200 uppercase tracking-wider font-mono">設計ポイント &amp; 実装メカニズム</h4>
        <ul id="drawerPoints" class="space-y-2 text-xs text-slate-300 list-disc pl-4 leading-relaxed"></ul>
      </div>
      <div class="space-y-2">
        <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider font-mono">関連技術タグ</h4>
        <div id="drawerTags" class="flex flex-wrap gap-1.5"></div>
      </div>
    </aside>

  </div>

  <!-- Add Node Modal -->
  <div id="addNodeModal" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 hidden flex items-center justify-center">
    <div class="bg-slate-900 border border-slate-700 rounded-xl w-full max-w-md p-6 space-y-4">
      <h3 class="text-sm font-bold text-slate-100">新規設計ノードの追加</h3>
      <div class="space-y-3 text-xs">
        <div>
          <label class="block text-slate-400 mb-1">タイトル</label>
          <input id="newNodeTitle" type="text" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-slate-200" placeholder="例: 棚札QR署名検証モジュール" />
        </div>
        <div>
          <label class="block text-slate-400 mb-1">サブタイトル (英字/数式)</label>
          <input id="newNodeSubtitle" type="text" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-slate-200" placeholder="例: Shelf Price Commitment" />
        </div>
        <div>
          <label class="block text-slate-400 mb-1">レイヤ区分</label>
          <select id="newNodeDomain" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-slate-200">
            <option value="biz_econ">⓪ 収益化・資本効率モデル</option>
            <option value="png_core">🖼️ PNG原案: vFHE &amp; 損保ホワイトボード</option>
            <option value="triage">① 前段・分岐器 &amp; PIIマスク</option>
            <option value="llm_vla">② 分散LLM &amp; 対インジェクション・VLA制御</option>
            <option value="lookup_zk">③ モデル知財秘匿 × Lookup証明 &amp; CNEI強制</option>
            <option value="chain">④ 店舗・物流オープンチェーン &amp; 漸進的トラスト</option>
            <option value="insurance">⑤ 顧客トラスト検証 × ZK/第三者監査 保険モデル</option>
          </select>
        </div>
        <div>
          <label class="block text-slate-400 mb-1">詳細説明</label>
          <textarea id="newNodeDesc" rows="3" class="w-full bg-slate-950 border border-slate-800 rounded px-3 py-1.5 text-slate-200"></textarea>
        </div>
      </div>
      <div class="flex justify-end space-x-2 pt-2">
        <button onclick="closeAddNodeModal()" class="px-3 py-1.5 rounded bg-slate-800 text-slate-300 text-xs">キャンセル</button>
        <button onclick="confirmAddNode()" class="px-3 py-1.5 rounded bg-emerald-600 text-white text-xs font-medium">追加する</button>
      </div>
    </div>
  </div>

  <script>
    // --- Categories Definition ---
    const CATEGORIES = {
      biz_econ:  { name: '00. 収益化・資本効率 & 大会スコープ', color: 'border-rose-500/60 bg-rose-950/30 text-rose-300', tagColor: 'bg-rose-500/20 text-rose-300 border-rose-500/40' },
      png_core:  { name: '🖼️ PNG原案 (vFHE & 手書き白板)', color: 'border-cyan-400/70 bg-cyan-950/35 text-cyan-200', tagColor: 'bg-cyan-500/20 text-cyan-300 border-cyan-400/40' },
      triage:    { name: '01. 前段・分岐器 & PIIマスク', color: 'border-amber-500/50 bg-amber-950/25 text-amber-300', tagColor: 'bg-amber-500/15 text-amber-300 border-amber-500/30' },
      llm_vla:   { name: '02. 標準/独自LLM & VLA防御制御', color: 'border-purple-500/50 bg-purple-950/25 text-purple-300', tagColor: 'bg-purple-500/15 text-purple-300 border-purple-500/30' },
      lookup_zk: { name: '03. モデル知財秘匿 × Lookup証明', color: 'border-sky-500/50 bg-sky-950/25 text-sky-300', tagColor: 'bg-sky-500/15 text-sky-300 border-sky-500/30' },
      chain:     { name: '04. 店舗/物流チェーン & 漸進的信頼', color: 'border-indigo-500/50 bg-indigo-950/25 text-indigo-300', tagColor: 'bg-indigo-500/15 text-indigo-300 border-indigo-500/30' },
      insurance: { name: '05. 顧客トラスト × ZK/第三者監査保険', color: 'border-teal-500/50 bg-teal-950/25 text-teal-300', tagColor: 'bg-teal-500/15 text-teal-300 border-teal-500/30' }
    };

    // --- All 14 Nodes Integrating Business Model, 3 PNG Files, and CSS2026 ---
    let nodes = [
      // === LAYER 0: BUSINESS MODEL, LOGISTICS OPTIMIZATION & CONTEST DELIVERABLES ===
      {
        id: 'node_biz_platform',
        domain: 'biz_econ',
        category: 'biz_econ',
        title: 'スーパー・物流センター最適化 & インフラ分離モデル',
        subtitle: '店舗は「場とZK検証基盤」を提供 ／ ロボット維持管理の外部化',
        paperRef: 'ビジネス・資本効率設計 (DePIN / Multi-Vendor Robotics Execution Platform)',
        x: 40,
        y: 40,
        desc: 'スーパーや中小物流センターが自前で高価なロボット群やAIモデルを購入・維持管理(CAPEX/OPEX)するのは経営上困難。店舗・倉庫側は「ロボットを受け入れる物理インフラ＋ZK監査・決済インフラ」のみを整備し、多様な外部ロボット・AIベンダーが参入して稼働・報酬を得るプラットフォームモデル。',
        points: [
          '【設備投資(CAPEX)と維持管理の分離】: 店舗・物流センターはロボットを所有・保守せず、標準化された「実行基盤(Execution Harness)と商品LUT・ZK検証ゲート」だけを設置',
          '【資本経済的インセンティブ還流】: 外部のロボットオーナーやAIモデル開発者がタスク(商品ピッキング・棚補充・検品)を完遂しZK証明を提出するたび、スマートコントラクトで即座に報酬(インセンティブ)と計算資源・データ利用権が分配されるため、自然に高性能なロボット・モデルが集まり稼働率が極大化',
          '【ダークストア・物流倉庫とのシームレス統合】: 昼間はスーパー店内の買い物代行ピックアップ、夜間やバックヤードでは物流センターのピッキング・仕分け最適化として同じ実行基盤で24時間収益化',
          '【全情コン(コンテスト)での発表・実装スコープ】: ①誰もがこのインフラ上でロボットを動かせる「オープン実行基盤」の実装、②ベースラインとなる「標準モデル(Reference Model)」の公開、③実機/シミュレータによる「商品ピックアップ・モック」の実演'
        ],
        tags: ['物流センター最適化', 'ロボット維持管理の外部化', 'インセンティブ経済圏', '実行基盤+標準モデル+モック', '資本効率最大化']
      },
      {
        id: 'node_ip_secret_zk',
        domain: 'biz_econ',
        category: 'biz_econ',
        title: 'モデル知財(IP)の完全秘匿 × 安全性・脆弱性の数学的証明',
        subtitle: '革新的アルゴリズム・重みを明かさず、店舗とお客様へトラストを提供',
        paperRef: 'CSS2026 2D1-2 (重み空間ドリフト安全性監査) / 2D1-4 (AI-BOM構成整合性) / ZKP・vFHE知財保護',
        x: 430,
        y: 40,
        desc: 'サードパーティのAI開発企業にとって「モデルの革新的な構造・独自ファインチューニング重み・プロンプト制御」は最高機密(IP)であり、監査のためにソースや重みを開示したくない。しかし店舗や顧客は「脆弱性やバックドアがないか・プライバシーを守っているか」の監査を急務としているジレンマを数学的証明(ZK)で解決。',
        points: [
          '【モデルの革新的部分(IP)を知られない監査】: AI開発者はモデルの重み W や独自アルゴリズム f を一切開示せず、ハッシュコミット H(W) のみを登録。推論とポリシールックアップが「承認済み安全制約の範囲内で正しく実行されたこと」だけをゼロ知識証明(zkVM / vFHE)で数学的に証明',
          '【脆弱性・安全性監査のゼロ知識化】: 事前レッドチーミング(プロンプトインジェクション耐性率・要求超過0%・AI-BOM整合性)をパスしたモデルであることの検証証跡を、重みを秘匿したままオンチェーン証明書として発行',
          '【お客様(エンドユーザー)自身のトラスト検証】: 来店客やネットスーパー注文者も、スマホの軽量Verifier(QR/NFC)で「自分の注文を処理したロボットが、個人情報をマスクし、アレルゲン・鮮度基準を数学的に満たして選んだこと」をワンタップで直接検証可能',
          '「ブラックボックスだから信用できない」と「全部公開すると知財が盗まれる」の二律背反を打ち破り、競争力ある革新モデルの参入を促進'
        ],
        tags: ['モデル知財(IP)秘匿', '数学的トラスト証明', 'お客様直接検証 (User Verifiable)', '脆弱性・プライバシー監査', 'AI-BOM / zkVM']
      },

      // === LAYER PNG: EXACT CONTENT FROM THE 3 PNG IMAGES ===
      {
        id: 'node_png_vfhe',
        domain: 'png_core',
        category: 'png_core',
        title: '【image.png】Verifiable FHE：FHEに「計算の正しさ」を足す (ZK + FHE)',
        subtitle: 'User (秘密データ x 🔒) ⇄ E(x) / E(f(x)) + π ⇄ Server (中身は見えない)',
        paperRef: 'md/image.png (Sources: Verifiable FHE (ZK + FHE) | EagleEye | Gentry 2009 / Merkle Japan p.27)',
        x: 820,
        y: 40,
        desc: 'md/image.png に描かれた暗号プロトコル図の完全統合。FHEによる「データの機密性」と、ZKによる「計算fの正しさの証明(π)」を同時に達成するアーキテクチャ。',
        points: [
          '① User (注文者・店舗・ロボット) は「秘密データ x 🔒 (個人情報・購買履歴・店舗の秘密パラメータ)」を完全準同型暗号で E(x) に暗号化して Server へ送信',
          '② Server (クラウド推論・検証ノード) は「中身は見えない」状態のまま、FHE: 暗号文のまま関数 f (AI推論・安全ポリシー評価・保険査定式) を評価し E(f(x)) を算出',
          '③ 同時に Server は「ZK: 正しく関数 f を計算した証明 π」を生成し、E(f(x)) + π を User へ返送',
          '④ ユーザが復号 + π を検証: 「✓ 機密性 (FHE) AND 計算の正しさ (ZK) を同時に得る」ことで、データを一切見せられない相手にも高負荷な推論や監査を安全に委託可能'
        ],
        tags: ['image.png', 'Verifiable FHE (ZK+FHE)', 'E(x) → E(f(x)) + π', '機密性 + 計算の正しさ', 'EagleEye']
      },
      {
        id: 'node_png_wb_insurance',
        domain: 'png_core',
        category: 'png_core',
        title: '【image copy.png & copy 2.png】手書き白板 & ZK, or not ZK (AIエージェント保険)',
        subtitle: '(task, trace=APIコールlist) の check を MPC/FHE で encryption したまま評価',
        paperRef: 'md/image copy.png (手書きホワイトボード写真) & md/image copy 2.png (ケーススタディ: AIエージェント保険)',
        x: 1210,
        y: 40,
        desc: 'md/image copy.png (手書きホワイトボード: タカハシさん・モトキさん・アベさん・ナガイさん・タマイ・えびえOさん議論) と md/image copy 2.png (スライド) の完全構造化。',
        points: [
          '【グループ課題 (image copy 2.png)】: AIエージェントの運用実績(e.g., タスク完了率)を「サービスの機密データ(e.g., 顧客データ・DB)を渡さずに」外部の損保会社に対して証明するシステム設計 (ユーザー ⇄ UI ⇄ AIエージェント ⇄ DB / 外部データソース ⇄ 損保会社)',
          '【① 指標？ (image copy.png 左上)】: task に対する trace (APIコールlist / 商品Lookupリスト) の check →「APIコールが"正しいか"（タスクリストに必要なAPIのみ呼び出す）」「1. 正しいAPIを使ったか？」＋「事故率 (etc...) / 統計」「成功率 (etc...)」',
          '【② ①の運用 & データの元 (image copy.png 中央)】: データの元＝「個人」と「法人 (AIエージェントを使ってサービスを提供してる会社)」。この法人と「損保会社」の間でデータやりとりを行い、法人が「約款に合致している事を証明」し損保が「検証」する',
          '【暗号化評価スキーム (image copy.png 左下 & copy 2.png 右下)】: 「MPC / FHE で (task, trace) の check を encryption したまま評価する」＋「トラストモデル（誰・何を信頼するモデルか）と現実的なトレードオフ（ZK vs MPC vs FHE vs TEE）」'
        ],
        tags: ['image copy.png (手書き白板)', 'image copy 2.png', '(task, trace) 暗号化check', 'APIコール正当性・事故率・成功率', '約款合致の証明']
      },

      // === LAYER 1: TRIAGE & PRIVACY PRE-PROCESSING ===
      {
        id: 'node_pii_context',
        domain: 'triage',
        category: 'triage',
        title: '店舗・倉庫の「場」考慮 & 軽量PII事前マスク基盤',
        subtitle: 'Regex/Dict/NER + 曖昧候補のみローカルLLM補正',
        paperRef: 'CSS2026 5C1-3 (朝比奈ら: 正規表現とローカルLLMによる軽量PII事前検出) / 2B3-3 (STAMP/STPA 四足ロボ安全分析)',
        x: 40,
        y: 380,
        desc: '外部ベンダーのロボットやモデルにタスクを渡す前に、実行基盤側で来店客の顔・個人情報(PII)・店舗の非公開エリア情報を確実にマスク化するゲートウェイ。データやタスクを外部へ積極的に渡してインセンティブを回すための安全前提を作る。',
        points: [
          '定型情報(顧客ID・決済番号・住所・電話)は決定論的Regex/ルールで即時マスク化 (LLM推論不要で超高速処理)',
          '表記ゆれのある非定型情報(注文メモや背景映り込み)のみ、Recall優先で候補抽出しエッジの標準ローカルLLMでKEEP/DISCARD/REPLACE境界補正 (処理速度3.2倍高速化・推論失敗0件)',
          '「場」の安全制約(STAMP/STPA): スーパー通路の混雑度や物流倉庫のフォークリフト動線・死角に応じ、最大速度・接近マージンを基盤側で動的制限',
          'センサ・カメラ直結のTEEハードウェア署名により「入力データ自体の現実真正性(トラストアンカー)」を担保'
        ],
        tags: ['場の考慮', 'PII事前マスク', 'ローカルLLM境界補正', 'STAMP/STPA', 'トラストアンカー']
      },
      {
        id: 'node_rf_router',
        domain: 'triage',
        category: 'triage',
        title: '実行基盤の分岐器トリアージ (RF/TF-IDF Router)',
        subtitle: '定型ピッキングの高速バイパスと選択的LLMルーティング',
        paperRef: 'CSS2026 4E3-5 (北島ら: Random Forest+LLMによるPI検出の再考：分類器トリアージと選択的LLM呼び出し)',
        x: 40,
        y: 680,
        desc: '物流センターや店舗で発生する大量のピッキング指示のすべてに高コストなLLMを使わず、実行基盤の前段にある「分岐器(Router)」でトリアージし、計算資源と電力を劇的に節約。',
        points: [
          '頻出・定型の商品ピックアップ要求(JANコード指定・定番品の補充・倉庫棚番ピッキング)は、NP較正閾値(τ_NP)以下の低リスク入力としてLLMをバイパスし、直接高速Lookupへルーティング (LLM呼出を23.2%以上削減)',
          '分類器の権限は「検証済みソースの低リスク入力のバイパス許可」のみに限定し、最終安全判定は委ねない設計',
          '適応的パディング攻撃対策として「良性重み Density Gate」と「ソース分布監視(PSI / KS検定)」を実行基盤に標準搭載',
          '複雑な自然言語注文(「傷んでない果物とアレルギー対応の代替品を選んで」)のみ、登録された標準LLMまたはサードパーティ革新LLMへルーティングしインセンティブを付与'
        ],
        tags: ['分岐器 (Router)', 'Random Forest / LR', '選択的LLM呼び出し', 'Density Gate', '計算コスト最適化']
      },

      // === LAYER 2: DECENTRALIZED LLM & VLA INJECTION DEFENSE ===
      {
        id: 'node_ica_llm',
        domain: 'llm_vla',
        category: 'llm_vla',
        title: '標準モデル & 独自LLMハーネス (ASIDE + ICA防御)',
        subtitle: '悪意ある商品POP・偽ラベルからの間接プロンプトインジェクション無力化',
        paperRef: 'CSS2026 4E3-4 (米田・大塚: Instruction-Conditioned Adapter による動的PI防御) / 4E4-5 (敵対的摂動型VPIの内部状態分析)',
        x: 430,
        y: 380,
        desc: 'コンクールで発表する「標準モデル(Reference Model)」および参入企業が持ち込む独自LLMを保護するアダプタ層。店内の悪意あるPOP広告や偽バーコードを読み取った際の間接プロンプトインジェクション(IPI/VPI)を阻止。',
        points: [
          '実行基盤からの正規命令(Instruction)と、店内の棚画像・商品説明テキスト(Data)をASIDEにより埋め込み空間で構造的に直交分離',
          '各Transformer層でInstructionの意味表現から動的ゲート g^(l) = σ(W_g c^(l) + b_g) を生成し、Data側のBottleneck Adapter出力を要素ごとに制御(ICA)',
          '適応的攻撃(PAIR等)に対しても攻撃成功率を大幅低減し、モデル本体の重みを改造することなく軽量Adapterとして標準装着可能',
          'VLMの視覚Merger出力逸脱と後段Logit集中を監視し、敵対的摂動型ビジュアルインジェクション(VPI)を早期検知'
        ],
        tags: ['標準モデル (Reference Model)', 'ASIDE + ICA', '間接PI防御 (IPI/VPI)', '視覚Merger監視', 'プラグイン防御']
      },
      {
        id: 'node_vla_chunk',
        domain: 'llm_vla',
        category: 'llm_vla',
        title: '自律畳み込み制御 & 動的Action Chunking',
        subtitle: '単一時刻の入力摂動・特徴量誘導攻撃(FSA)からの即時回復',
        paperRef: 'CSS2026 2D4-1 (山辺・佐久間: 単一時刻の入力摂動に対するVLAモデルの脆弱性と動的Action Chunking) / 2D4-4 (特徴量誘導攻撃FSA)',
        x: 430,
        y: 680,
        desc: 'ロボットの物理アクチュエータをAIモデルに「投げっぱなし」にしないための実行基盤側フィードバック（畳み込み）制御ループ。照明反射や通信瞬断、特徴量誘導攻撃による商品破損・衝突を防止。',
        points: [
          'VLAモデルが1回の推論で出力する複数ステップの行動列(Action Chunk)において、一瞬のカメラ白飛び・センサスパイクが後続ステップまで持続する脆弱性を解消',
          '直前の推論の未実行行動列 Â と現在予測された行動列 A_t の「割引累積不一致度 D(A_t, Â)」を実行基盤でリアルタイム計算 (追加推論コスト1ms未満)',
          '不一致度が閾値 τ を超えた瞬間、異常摂動または別タスクへの特徴量誘導(FSA)と判断し、実行長 H_t を最小(1ステップ)へ動的に短縮して即座に再推論・減速停止へ畳み込む',
          'どのようなベンダーのVLAモデルが載っても、物理的な暴走を実行基盤側で抑え込むセーフティハーネスとして機能'
        ],
        tags: ['動的Action Chunking', '畳み込み制御ループ', '割引累積不一致度', 'VLA摂動耐性', '実行基盤ハーネス']
      },

      // === LAYER 3: PRODUCT PICKUP LOOKUP PROOF & CNEI ENFORCEMENT ===
      {
        id: 'node_lookup_zk',
        domain: 'lookup_zk',
        category: 'lookup_zk',
        title: '商品ピックアップ「何を比較・検討したか」数学的Lookup証明',
        subtitle: 'ZK Lookup Argument + 三層知識バンドル Locator / 決定論的Lint',
        paperRef: 'CSS2026 1D2-4 (古川ら: 証跡対応関係の劣化測定とLocator/Lint強制) / 3D2-1 (関口・千田: 秘密分散を用いた多層LUT参照)',
        x: 820,
        y: 380,
        desc: 'ロボットが棚から商品をピックアップする際、モデルの内部ノウハウは秘匿したまま、「店舗の正規商品テーブル(LUT)からどの候補群を参照し、どの判断軸(価格・アレルゲン・鮮度・在庫)で比較検討して選んだか」を数学的に証明する。',
        points: [
          '【検討プロセスのZK Lookup証明】: 店舗・物流センターの正規商品マスタ・アレルギー安全基準・特売テーブル(事前コミット済みLUT T)に対し、比較候補集合 {item_1, ..., item_k} と選択結果が確実に T から引かれたことを ZK Lookup (および2次元LUT秘密分散) で証明',
          '【証跡Locatorの永続化と決定論的Lint】: LLMの要約で失われやすい「どの棚画像のどの座標(image_bbox)・どのJAN行(log_line)を根拠に選んだか」をClaim-Artifact-Locator三層バンドルとして拘束し、コミット前に決定論的Lint(Gate)で構造違反を0%に抑止',
          '【モック実演での可視化ポイント】: 「候補A(小麦含有・¥198)と候補B(米粉ルー・¥258)をルックアップ比較し、顧客のアレルギー制約を満たすBを選択した」ことのZK Proof生成と検証をリアルタイム表示',
          'モデルの独自スコアリング関数(企業秘密)は明かさず、「約款・安全基準に違反しない候補選択であったこと」のみをお客様と店舗に数学的保証'
        ],
        tags: ['ZK Lookup証明', '比較検討トレース', '三層知識バンドル (Locator)', '決定論的Lint強制', 'モック実演コア']
      },
      {
        id: 'node_cnei_tee',
        domain: 'lookup_zk',
        category: 'lookup_zk',
        title: 'TEE隔離実行 & 操作上限強制 (CNEI / ContextBoundGate)',
        subtitle: 'Control-State Poisoning 防御と物理ピックアップ自動署名',
        paperRef: 'CSS2026 1E2-2 (中井ら: Control-State PoisoningとCNEI実行前強制) / 4B2-1 (濱口ら: 秘密鍵と署名判断をTEEに隔離した自動署名)',
        x: 820,
        y: 680,
        desc: 'どれほど巧妙なメモ汚染や運用情報の組み合わせ(Control-State Poisoning)でAIモデルが「高額商品を大量購入せよ」「立入禁止区域へ入れ」と誘導されても、モデル外のTEE実行基盤で物理実行を100%遮断する。',
        points: [
          'Capability Non-Expansion Invariant (CNEI): 攻撃者が影響し得る店内POP・過去履歴・LLM出力からは権限上限 τ を一切決定せず、認証済み注文エンドポイントからのみ要求上限 τ = Req(u) を取得',
          '操作レベル分類: L0(棚検索・在庫確認)、L1(代替品提案・ピッキング計画)、L2(物理アーム把持・決済トランザクション実行)を定義し、Level(a) ≤ τ を満たさない行動をfail-closedで遮断(誤介入0件)',
          'OP-TEEセキュアエンクレーブ内で署名対象データ(商品ID・金額・把持トルク・移動速度)を抽出し、事前承認ポリシー P(Tx) と照合して平均670msで自動ハードウェア署名',
          '実行基盤がハードウェアレベルで安全上限を握っているため、サードパーティ製の未知のAIモデルでも安心して店舗・倉庫へ受け入れ可能'
        ],
        tags: ['CNEI (操作非拡張)', 'Control-State Poisoning対策', 'OP-TEE自動署名', 'サードパーティ安全受入', 'zkVM実行証明']
      },

      // === LAYER 4: DECENTRALIZED CHAIN & PROGRESSIVE TRUST ===
      {
        id: 'node_consortium_chain',
        domain: 'chain',
        category: 'chain',
        title: '店舗・物流・ロボ企業・損保の分散コンソーシアムチェーン',
        subtitle: '異種企業ポリシーの秘匿部分グラフ合議 & インセンティブ自動決済',
        paperRef: 'CSS2026 3G1-3 (竹内・面: コンソーシアムブロックチェーンにおける異種ポリシーを扱う取引検証) / 3G2-2 (ERC-8004 証拠多重性とContextBoundGate)',
        x: 430,
        y: 980,
        desc: 'スーパー・物流倉庫・ロボット開発企業・保険会社が参加するブロックチェーン基盤。各社の企業秘密（モデルの革新性・店舗の仕入れ値・倉庫動線・保険査定式）を秘匿したまま、取引検証とインセンティブ配分を自動執行。',
        points: [
          '共通検証 f(X) と企業別個別ポリシー検証 g_i(X) の二段構成。各社の機密ポリシー g_i を算術回路（有向グラフ）の「部分グラフ G_{k,j}」に分割し、ピア間で全容を明かさず分散合議',
          '作業データや空きリソースを他ロボットへ渡すほど報酬トークンが還元されるインセンティブ設計（通路渋滞マップ・棚欠品情報・エッジ計算力のP2P融通）',
          'ERC-8004 Web3エージェントの「証拠多重性(Evidence Multiplicity: 同一主体や複数アドレス分割による評判水増し)」を防ぐため、主体独立性と証拠スナップショットを判断証跡(Receipt)へ拘束する ContextBoundGate を実装'
        ],
        tags: ['コンソーシアムチェーン', '部分グラフ分割検証', 'インセンティブ自動配分', '証拠多重性対策 (ERC-8004)', 'P2Pリソース融通']
      },
      {
        id: 'node_mpt_trust',
        domain: 'chain',
        category: 'chain',
        title: '無記憶漸進的トラスト (MPT) & セッション媒介器 (PE)',
        subtitle: '新規参入ロボットでも「その場の振る舞い証跡」から段階的に仕事と報酬を獲得',
        paperRef: 'CSS2026 2G4-5 (亀谷・八槇: 無記憶漸進的トラスト Agentic AIのための非集権的トラストアーキテクチャー)',
        x: 40,
        y: 980,
        desc: '外部のロボットやAIモデルを店舗・倉庫へ受け入れる際、過去の長期評判だけに頼ると「モデル差し替え」や「汚染」を見抜けない。また新規参入者が不利になる。現セッションの振る舞い証跡のみから漸進的に権限と報酬枠を広げる。',
        points: [
          '信頼を長期アカウントではなく一時セッション主体 σ_B = <sid, pk_B> に帰属させ、初期信頼 T_0 = 0 からスタート (Sybil攻撃や名義ロンダリングを無効化しつつ、新規参入ロボットにも公平な機会を提供)',
          'ピッキング業務を残余リスク R_eff の昇順に分解: τ_1(読取専用の棚在庫スキャン: R_eff=0) → τ_2(日用品・常温品のピッキング) → τ_3(割れ物・高額品・精算決済)',
          '各ステップの Progress Receipt (PR) と Policy Enforcer (PE) ログのハッシュ連鎖を検証し、R_eff ≤ g(T_dec) の範囲でのみ次タスクの Capability Token を発行',
          '事前コミットされたルーブリック Γ により、店舗側が事後的に採点基準を変えてロボットへの報酬支払を不当に拒否することも防止'
        ],
        tags: ['無記憶漸進的トラスト (MPT)', '新規参入インセンティブ', 'Policy Enforcer (PE)', 'ハッシュ連鎖レシート', '残余リスク較正']
      },

      // === LAYER 5: HYBRID ZK & THIRD-PARTY AUDITABLE INSURANCE ===
      {
        id: 'node_zk_insurance',
        domain: 'insurance',
        category: 'insurance',
        title: 'AIロボット保険: ZK/vFHE 無開示監査 & 顧客トラスト証明',
        subtitle: 'モデルの革新性と顧客プライバシーを秘匿し「約款遵守と検討妥当性」を数学的証明',
        paperRef: 'PNG原案 (image.png / image copy.png / copy 2.png) + CSS2026 1G2-4 / 4F3-3',
        x: 1210,
        y: 380,
        desc: 'ロボット開発社・店舗・お客様・損保会社の四者間トラストを数学的に成立させる保険モデル。平時は企業のモデル知財や顧客データを一切開示せず、ZK/MPC/vFHE証明によって安全稼働実績と保険料割引・即時補償を自動執行。',
        points: [
          '【手書き白板 (image copy.png) の実装】: 法人が (task, trace=APIコール/Lookupリスト) を MPC / vFHE で暗号化したまま損保会社とcheckし、「正しいAPIのみ呼んだか」「事故率・成功率の統計」「約款合致」をゼロ知識で証明',
          '【お客様への直接トラスト提供】: 注文したお客様に対しても「あなたの注文商品は、アレルゲン・消費期限・価格の正規LUTから正しく比較検討され、個人情報もマスク処理されました」という数学的証明(ZK Receipt)を発行',
          '【誤ピックアップ・破損時の免責切り分け】: 事故発生時、「店舗インフラ側のLUT登録ミス」か「ロボットモデルの推論ミス」か「不可抗力」かをZKトレースで即座に切り分け、正当なロボット開発者を保護'
        ],
        tags: ['AIエージェント保険', 'ZK/MPC/vFHE暗号化評価', 'お客様トラスト証明', 'モデル知財秘匿', '約款合致の数学的証明']
      },
      {
        id: 'node_dcss_audit',
        domain: 'insurance',
        category: 'insurance',
        title: '有事の第三者監査 & 裁判所開示 (DCSS × AuditGuard 3-of-5)',
        subtitle: '指定確認者墨塗署名 (DCSS) + Shamir 3-of-5 閾値エスクロー',
        paperRef: 'CSS2026 5B1-4 (廣瀬・駒野: 監査ログシステムに適した指定確認者墨塗署名 DCSS の実装評価) + AuditGuard (Shamir + Schnorr PoK)',
        x: 1210,
        y: 680,
        desc: '「平時はZKでモデルの革新的部分やプライバシーを完全に隠しつつ、万が一の重大事故や訴訟時には、指定された第三者（監査機関・裁判所）だけが墨塗り箇所を検証できる」ハイブリッド監査アーキテクチャ。',
        points: [
          '【第1段階: 公開墨塗監査 (DCSS Sanitizable Signature)】: カメレオンハッシュを用い、ロボットの行動・Lookupログのうち「モデルの独自ノウハウ部分」や「顧客の個人情報ブロック」だけを監査人が墨塗り(Sanitize)してチェーンへ記録。一般第三者は墨塗り状態のまま監査済み署名の正当性を検証可能 (16ブロック全墨塗でも約102ms)',
          '【第2段階: 指定確認者検証 (Designated Confirmer)】: 墨塗り前の元の情報の正しさは、指定された確認者(裁判所・公的第三者事故調査機関)との対話プロトコルでのみ確認でき、競合他社へのモデル知財流出やデータの独り歩きを完全防止 (1ブロック約0.58ms)',
          '【第3段階: AuditGuard 3-of-5 閾値復号】: 復号Release Keyを Shamir秘密分散 (3-of-5: ロボット開発社・店舗/倉庫・損保会社・消費者機関・裁判所) で分割保持し、Fiat-Shamir Schnorr PoK により3者の合意が揃った有事のみ開示'
        ],
        tags: ['指定確認者墨塗署名 (DCSS)', 'カメレオンハッシュ', 'AuditGuard (Shamir 3-of-5)', 'モデル知財流出防止', '第三者・裁判所監査']
      }
    ];

    // --- Directed Edges Connecting All 14 Nodes ---
    let edges = [
      // Layer 0 & PNG Core connections
      { from: 'node_biz_platform', to: 'node_pii_context', label: '店舗/倉庫インフラ提供' },
      { from: 'node_biz_platform', to: 'node_consortium_chain', label: 'ロボット受入 & 報酬配分ルール' },
      { from: 'node_ip_secret_zk', to: 'node_png_vfhe', label: 'モデル知財(IP)とデータの暗号化 E(x)' },
      { from: 'node_png_vfhe', to: 'node_lookup_zk', label: 'E(f(x)) + π (機密性+計算の正しさ)' },
      { from: 'node_png_wb_insurance', to: 'node_zk_insurance', label: '(task, trace) 暗号化check・約款証明' },
      { from: 'node_ip_secret_zk', to: 'node_ica_llm', label: '独自モデルの重み秘匿搭載' },

      // Layer 1 -> Layer 2 & 3
      { from: 'node_pii_context', to: 'node_rf_router', label: 'PIIマスク済み注文・倉庫タスク' },
      { from: 'node_rf_router', to: 'node_lookup_zk', label: '定型ピッキングの高速バイパス (23%削減)' },
      { from: 'node_rf_router', to: 'node_ica_llm', label: '非定型タスクのみ選択的LLM呼出' },

      // Layer 2 -> Layer 3
      { from: 'node_ica_llm', to: 'node_vla_chunk', label: 'ICA動的ゲート制御済み行動計画' },
      { from: 'node_ica_llm', to: 'node_lookup_zk', label: '候補商品の比較推論 & 根拠Locator' },
      { from: 'node_vla_chunk', to: 'node_cnei_tee', label: '動的実行長 H_t 補正済み制御指令' },

      // Layer 3 internal & -> Layer 4/5
      { from: 'node_lookup_zk', to: 'node_cnei_tee', label: 'LUT参照ZK証明 + Lint済み判断証跡' },
      { from: 'node_cnei_tee', to: 'node_consortium_chain', label: 'OP-TEE署名済み完了Tx → 報酬獲得' },
      { from: 'node_mpt_trust', to: 'node_cnei_tee', label: '現セッション許容リスク上限 τ / CT発行' },
      { from: 'node_cnei_tee', to: 'node_mpt_trust', label: 'Progress Receipt (PR) 還流・信頼拡大' },

      // Layer 4 -> Layer 5 (Insurance & Audit)
      { from: 'node_consortium_chain', to: 'node_zk_insurance', label: '部分グラフ検証済み実績 & インセンティブ精算' },
      { from: 'node_lookup_zk', to: 'node_zk_insurance', label: '「何を比較検討したか」ZK Lookup Proof' },
      { from: 'node_zk_insurance', to: 'node_dcss_audit', label: '有事・事故争議時のエスカレーション' },
      { from: 'node_consortium_chain', to: 'node_dcss_audit', label: 'DCSS墨塗署名ログ記録 & 3-of-5閾値開示' }
    ];

    // --- Canvas Pan & Zoom State ---
    let panX = 18;
    let panY = 12;
    let zoom = 0.78;
    let isPanning = false;
    let startPanX = 0;
    let startPanY = 0;
    let draggedNode = null;
    let dragOffsetX = 0;
    let dragOffsetY = 0;
    let activeDomainFilter = 'all';

    const viewGraph = document.getElementById('viewGraph');
    const nodesContainer = document.getElementById('nodesContainer');
    const connectionsLayer = document.getElementById('connectionsLayer');

    function updateCanvasTransform() {
      nodesContainer.style.transform = `translate(${panX}px, ${panY}px) scale(${zoom})`;
      renderConnections();
    }

    function resetZoom() {
      panX = 18;
      panY = 12;
      zoom = 0.78;
      updateCanvasTransform();
    }

    function filterByDomain(domain) {
      activeDomainFilter = domain;
      renderNodes();
      renderConnections();
    }

    // --- Render Nodes ---
    function renderNodes() {
      nodesContainer.innerHTML = '';
      nodes.forEach(node => {
        const cat = CATEGORIES[node.category] || CATEGORIES.lookup_zk;
        const isDimmed = activeDomainFilter !== 'all' && node.domain !== activeDomainFilter;

        const nodeEl = document.createElement('div');
        nodeEl.id = node.id;
        nodeEl.className = `absolute w-[355px] p-4 rounded-xl border ${cat.color} backdrop-blur-md shadow-xl transition-opacity duration-200 hover:shadow-2xl hover:border-slate-300 cursor-pointer select-none ${isDimmed ? 'opacity-15 pointer-events-none' : 'opacity-100'}`;
        nodeEl.style.left = `${node.x}px`;
        nodeEl.style.top = `${node.y}px`;

        nodeEl.innerHTML = `
          <div class="flex items-center justify-between pb-2 mb-2 border-b border-slate-800/80">
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${cat.tagColor}">
              ${cat.name}
            </span>
            <span class="text-[10px] font-mono text-slate-400">${node.domain === 'png_core' ? 'PNG SOURCE' : node.domain === 'biz_econ' ? 'BIZ / IP' : 'CSS2026'}</span>
          </div>
          <h4 class="text-sm font-bold text-slate-100 tracking-tight leading-snug mb-1">${node.title}</h4>
          <p class="text-[11px] font-mono text-emerald-400/90 mb-2">${node.subtitle}</p>
          <div class="text-[10px] font-mono text-slate-400 bg-slate-950/70 border border-slate-800/80 rounded px-2 py-1 mb-2.5 truncate" title="${node.paperRef}">
            📄 ${node.paperRef}
          </div>
          <p class="text-xs text-slate-300/90 line-clamp-3 leading-relaxed mb-3">${node.desc}</p>
          <div class="flex flex-wrap gap-1">
            ${node.tags.slice(0, 4).map(tag => `<span class="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900/90 border border-slate-800 text-slate-300">${tag}</span>`).join('')}
            ${node.tags.length > 4 ? `<span class="text-[10px] text-slate-400 font-mono">+${node.tags.length - 4}</span>` : ''}
          </div>
        `;

        let isDraggingNode = false;
        nodeEl.addEventListener('mousedown', (e) => {
          e.stopPropagation();
          draggedNode = node;
          isDraggingNode = false;
          dragOffsetX = (e.clientX - panX) / zoom - node.x;
          dragOffsetY = (e.clientY - panY) / zoom - node.y;
        });

        nodeEl.addEventListener('mousemove', () => {
          if (draggedNode) isDraggingNode = true;
        });

        nodeEl.addEventListener('click', (e) => {
          e.stopPropagation();
          if (!isDraggingNode) {
            openDetailDrawer(node.id);
          }
        });

        nodesContainer.appendChild(nodeEl);
      });
    }

    // --- Render Connections with Labels ---
    function renderConnections() {
      const existing = connectionsLayer.querySelectorAll('.edge-group');
      existing.forEach(el => el.remove());

      edges.forEach((edge) => {
        const fromNode = nodes.find(n => n.id === edge.from);
        const toNode = nodes.find(n => n.id === edge.to);
        if (!fromNode || !toNode) return;

        const isVisible = (activeDomainFilter === 'all') ||
                          (fromNode.domain === activeDomainFilter || toNode.domain === activeDomainFilter);
        const strokeColor = isVisible ? '#64748b' : '#1e293b';
        const opacity = isVisible ? '0.9' : '0.12';

        const cardW = 355;
        const cardH = 220;

        const x1 = (fromNode.x + cardW / 2) * zoom + panX;
        const y1 = (fromNode.y + cardH / 2) * zoom + panY;
        const x2 = (toNode.x + cardW / 2) * zoom + panX;
        const y2 = (toNode.y + cardH / 2) * zoom + panY;

        const dx = (x2 - x1) * 0.45;
        const dy = (y2 - y1) * 0.15;
        const dStr = `M ${x1} ${y1} C ${x1 + dx} ${y1 + dy}, ${x2 - dx} ${y2 - dy}, ${x2} ${y2}`;

        const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        g.setAttribute('class', 'edge-group');
        g.setAttribute('opacity', opacity);

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', dStr);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', strokeColor);
        path.setAttribute('stroke-width', isVisible ? '2' : '1');
        path.setAttribute('stroke-dasharray', '5 4');
        path.setAttribute('marker-end', isVisible ? 'url(#arrow)' : '');
        g.appendChild(path);

        if (isVisible && edge.label) {
          const midX = (x1 + x2) / 2;
          const midY = (y1 + y2) / 2 - 6;
          const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
          text.setAttribute('x', midX);
          text.setAttribute('y', midY);
          text.setAttribute('text-anchor', 'middle');
          text.setAttribute('fill', '#94a3b8');
          text.setAttribute('font-size', '10');
          text.setAttribute('font-family', 'JetBrains Mono, Noto Sans JP, sans-serif');
          text.textContent = edge.label;
          g.appendChild(text);
        }

        connectionsLayer.appendChild(g);
      });
    }

    // --- Canvas Mouse Interaction ---
    viewGraph.addEventListener('mousedown', (e) => {
      if (e.target === viewGraph || e.target === connectionsLayer || e.target === nodesContainer) {
        isPanning = true;
        startPanX = e.clientX - panX;
        startPanY = e.clientY - panY;
      }
    });

    window.addEventListener('mousemove', (e) => {
      if (draggedNode) {
        draggedNode.x = Math.round((e.clientX - panX) / zoom - dragOffsetX);
        draggedNode.y = Math.round((e.clientY - panY) / zoom - dragOffsetY);
        const el = document.getElementById(draggedNode.id);
        if (el) {
          el.style.left = `${draggedNode.x}px`;
          el.style.top = `${draggedNode.y}px`;
        }
        renderConnections();
      } else if (isPanning) {
        panX = e.clientX - startPanX;
        panY = e.clientY - startPanY;
        updateCanvasTransform();
      }
    });

    window.addEventListener('mouseup', () => {
      draggedNode = null;
      isPanning = false;
    });

    viewGraph.addEventListener('wheel', (e) => {
      e.preventDefault();
      const scaleFactor = e.deltaY < 0 ? 1.08 : 0.92;
      zoom = Math.min(Math.max(zoom * scaleFactor, 0.4), 1.8);
      updateCanvasTransform();
    }, { passive: false });

    // --- Detail Drawer ---
    function openDetailDrawer(nodeId) {
      const node = nodes.find(n => n.id === nodeId);
      if (!node) return;
      const cat = CATEGORIES[node.category] || CATEGORIES.lookup_zk;

      const drawer = document.getElementById('detailDrawer');
      const catEl = document.getElementById('drawerCategory');
      catEl.className = `text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${cat.tagColor}`;
      catEl.textContent = cat.name;

      document.getElementById('drawerTitle').textContent = node.title;
      document.getElementById('drawerSubtitle').textContent = node.subtitle;
      document.getElementById('drawerPaperBadge').textContent = `📄 着想元: ${node.paperRef}`;
      document.getElementById('drawerDesc').textContent = node.desc;

      const pointsList = document.getElementById('drawerPoints');
      pointsList.innerHTML = node.points.map(p => `<li>${p}</li>`).join('');

      const tagsDiv = document.getElementById('drawerTags');
      tagsDiv.innerHTML = node.tags.map(t => `<span class="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-emerald-400">${t}</span>`).join('');

      drawer.classList.remove('hidden');
    }

    function closeDetailDrawer() {
      document.getElementById('detailDrawer').classList.add('hidden');
    }

    // --- View Switching ---
    function switchView(view) {
      const views = ['graph', 'notes', 'export'];
      views.forEach(v => {
        const section = document.getElementById('view' + v.charAt(0).toUpperCase() + v.slice(1));
        const btn = document.getElementById('viewBtn' + v.charAt(0).toUpperCase() + v.slice(1));
        if (v === view) {
          section.classList.remove('hidden');
          btn.className = 'px-3 py-1.5 rounded-md bg-emerald-600 text-white transition-all shadow-sm';
        } else {
          section.classList.add('hidden');
          btn.className = 'px-3 py-1.5 rounded-md text-slate-400 hover:text-slate-200 transition-all';
        }
      });
      if (view === 'notes') renderNotesView();
      if (view === 'export') generateExportData();
    }

    // --- Render Structured Notes, PNG Gallery & CSS2026 Matrix ---
    function renderNotesView() {
      const container = document.getElementById('notesContent');
      container.innerHTML = `
        <!-- 0. PNG 3枚 完全図解・書き起こしギャラリー -->
        <div class="p-6 rounded-2xl border border-cyan-500/40 bg-cyan-950/15 space-y-5">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-cyan-300">
              🖼️ md/ 内の PNG 3枚 (image.png / image copy.png / image copy 2.png) 完全構造化 &amp; ホワイトボード反映
            </h2>
            <span class="text-xs font-mono px-2.5 py-1 rounded bg-cyan-900/50 text-cyan-200 border border-cyan-700/50">
              3 PNG Files Embedded
            </span>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-5 text-xs">
            <!-- PNG 1: image.png -->
            <div class="bg-slate-900/95 border border-slate-800 rounded-xl overflow-hidden flex flex-col">
              <div class="p-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                <span class="font-mono font-bold text-cyan-400">1. md/image.png</span>
                <span class="text-[10px] font-mono text-slate-400">Merkle Japan p.27</span>
              </div>
              <img src="image.png" alt="Verifiable FHE" class="w-full h-44 object-contain bg-white p-1" />
              <div class="p-4 space-y-2 flex-1">
                <div class="font-bold text-slate-100">Verifiable FHE：FHEに「計算の正しさ」を足す (ZK + FHE)</div>
                <ul class="list-disc pl-4 space-y-1 text-slate-300 leading-relaxed">
                  <li><strong>User (秘密データ x 🔒)</strong> → <code>E(x)</code> を送信</li>
                  <li><strong>Server (中身は見えない)</strong> → FHE: 暗号文のまま <code>f</code> を評価</li>
                  <li>Server → <code>E(f(x)) + π</code> （🛡️ <strong>ZK: 正しく計算した証明 π</strong>）を返送</li>
                  <li><strong>④ ユーザが復号 + π を検証</strong>：機密性 (FHE) AND 計算の正しさ (ZK) を同時に得る</li>
                </ul>
              </div>
            </div>

            <!-- PNG 2: image copy.png -->
            <div class="bg-slate-900/95 border border-slate-800 rounded-xl overflow-hidden flex flex-col">
              <div class="p-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                <span class="font-mono font-bold text-teal-400">2. md/image copy.png</span>
                <span class="text-[10px] font-mono text-slate-400">手書きホワイトボード原案</span>
              </div>
              <img src="image copy.png" alt="Handwritten Whiteboard" class="w-full h-44 object-cover bg-slate-950" />
              <div class="p-4 space-y-2 flex-1">
                <div class="font-bold text-slate-100">手書きホワイトボード完全書き起こし</div>
                <ul class="list-disc pl-4 space-y-1 text-slate-300 leading-relaxed">
                  <li><strong>① 指標？</strong>: <code>task</code> → <code>trace (APIコールlist)</code> の <code>check</code>。<strong>APIコールが"正しいか"</strong>（タスクリストに必要なAPIのみ呼び出す）＋ <strong>事故率 (etc...) / 統計</strong>、<strong>成功率 (etc...)</strong>、「1. 正しいAPIを使ったか？」</li>
                  <li><strong>② ①の運用 &amp; データの元</strong>: 「個人」「法人 (AIエージェントを使ってサービスを提供してる会社)」⇄「損保会社」の間でデータやりとり。法人が<strong>「約款に合致している事を証明」</strong>し、損保が<strong>「検証」</strong>。</li>
                  <li><strong>暗号評価</strong>: <strong>「MPC / FHE で (task, trace) の check を encryption したまま評価する」</strong></li>
                  <li><strong>右端メンバー</strong>: ①タカハシさん ②モトキさん ③アベさん ④ナガイさん ⑤タマイ / えびえOさん</li>
                </ul>
              </div>
            </div>

            <!-- PNG 3: image copy 2.png -->
            <div class="bg-slate-900/95 border border-slate-800 rounded-xl overflow-hidden flex flex-col">
              <div class="p-3 bg-slate-950 border-b border-slate-800 flex items-center justify-between">
                <span class="font-mono font-bold text-indigo-400">3. md/image copy 2.png</span>
                <span class="text-[10px] font-mono text-slate-400">ケーススタディ課題定義</span>
              </div>
              <img src="image copy 2.png" alt="ZK or not ZK Case Study" class="w-full h-44 object-contain bg-white p-1" />
              <div class="p-4 space-y-2 flex-1">
                <div class="font-bold text-slate-100">ZK, or not ZK（ケーススタディ：AIエージェント保険）</div>
                <ul class="list-disc pl-4 space-y-1 text-slate-300 leading-relaxed">
                  <li><strong>グループ課題</strong>: AIエージェントの運用実績（e.g., タスク完了率）を<span class="text-pink-400 font-semibold">サービスの機密データ（e.g., 顧客データ）を渡さずに</span>外部の保険会社に対して証明するシステムの設計</li>
                  <li><strong>システム構成図</strong>: ユーザー ⇄ [サービス: UI ⇄ AIエージェント ⇄ DB] ⇄ 外部データソース ／ サービス ⇄ <strong>?</strong> ⇄ 損保会社</li>
                  <li><strong>検討すべき事項</strong>: ①指標(e.g., ISO)と運用実績の測定・証明方法、②機密データの秘匿方法・具体的スキーム（<strong>トラストモデル：誰・何を信頼するモデルか</strong>、<strong>現実的なトレードオフ</strong>）</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <!-- Business Model & Contest Strategy Banner -->
        <div class="p-6 rounded-2xl border border-rose-500/40 bg-rose-950/15 space-y-4">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-bold text-rose-300">
              🚀 ビジネス・収益化モデル &amp; 全国情報教育コンテスト発表戦略
            </h2>
            <span class="text-xs font-mono px-2.5 py-1 rounded bg-rose-900/50 text-rose-200 border border-rose-700/50">
              DePIN型ロボット実行基盤 × 知財秘匿ZK監査
            </span>
          </div>
          <p class="text-xs text-slate-200 leading-relaxed">
            <strong>【課題の本質】</strong> スーパーマーケットや地域の物流センターが、自前で大量の自律ロボットを購入・保守・AIモデル更新（維持管理）し続けることは資金的にも技術的にも困難です。一方で、優秀なロボット・AIモデルを開発するスタートアップや研究者は「自社のモデルの革新的な部分（重み・独自アルゴリズム）は企業秘密として隠したいが、安全性やプライバシー保護を証明して店舗・倉庫で稼働させたい」と考えています。
          </p>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 pt-2 text-xs">
            <div class="bg-slate-900/90 p-4 rounded-xl border border-rose-500/30">
              <span class="text-rose-400 font-bold font-mono block mb-1">1. 店舗・物流センターの分離モデル</span>
              <span class="text-slate-300 leading-relaxed">店や倉庫はロボットを所有・維持管理せず、<strong>「ロボットを置ける物理環境」と「ZK検証・ブロックチェーン決済インフラ」だけを提供</strong>。多様な外部ロボットが参入してピッキング作業を代行する。</span>
            </div>
            <div class="bg-slate-900/90 p-4 rounded-xl border border-amber-500/30">
              <span class="text-amber-400 font-bold font-mono block mb-1">2. 資本経済的インセンティブ設計</span>
              <span class="text-slate-300 leading-relaxed">タスクや環境データを外部ロボットへ積極的に渡すほど、完了証跡(ZK Proof)に応じて<strong>自動で報酬・インセンティブが分配</strong>される。昼は店内ピックアップ、夜は物流倉庫の仕分け最適化として資本効率を最大化。</span>
            </div>
            <div class="bg-slate-900/90 p-4 rounded-xl border border-sky-500/30">
              <span class="text-sky-400 font-bold font-mono block mb-1">3. モデル知財(IP)秘匿 × 数学的証明</span>
              <span class="text-slate-300 leading-relaxed">急務であるプライバシー・脆弱性監査に対し、<strong>「AIモデルの革新的部分（重み・独自ロジック）は一切開示せず、安全基準とLookup検討を遵守した事実だけを数学的(ZK)に証明」</strong>する。</span>
            </div>
            <div class="bg-slate-900/90 p-4 rounded-xl border border-emerald-500/30">
              <span class="text-emerald-400 font-bold font-mono block mb-1">4. お客様トラスト &amp; 大会発表スコープ</span>
              <span class="text-slate-300 leading-relaxed"><strong>お客様自身も数学的証明でトラスト検証</strong>が可能。今回のコンクールでは<strong>①オープン実行基盤の構築、②標準モデル(Reference Model)の提示、③商品ピックアップのモック実演</strong>を行う。</span>
            </div>
          </div>
        </div>

        <!-- CSS2026 Proceedings Inspiration Mapping Table -->
        <div class="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 space-y-4">
          <h3 class="text-base font-bold text-slate-100 flex items-center space-x-2">
            <span>📚 CSS2026 論文集 (md/CSS2026_proceedings) からのインスピレーション・技術マッピング</span>
          </h3>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse text-xs">
              <thead>
                <tr class="border-b border-slate-800 text-slate-400 font-mono">
                  <th class="py-2.5 px-3">CSS2026 論文コード・タイトル</th>
                  <th class="py-2.5 px-3">論文の核心メカニズム</th>
                  <th class="py-2.5 px-3">本ロボット実行基盤・ビジネスモデルへの統合箇所</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800/70 text-slate-300">
                <tr>
                  <td class="py-2.5 px-3 font-mono text-amber-300">4E3-5 (IPSJ-CSS2026272)<br>Random Forest＋LLMによるPI検出の再考：分類器トリアージと選択的LLM呼び出し</td>
                  <td class="py-2.5 px-3">分類器を最終判定ではなく「低リスク入力のバイパス許可」に限定。NP較正閾値＋Density Gate＋PSI分布監視でLLM呼出を23.2%削減。</td>
                  <td class="py-2.5 px-3 text-emerald-300">実行基盤の「分岐器(Router)」。定型の倉庫ピッキングや定番品注文はLLMを通さず直接Lookupへバイパスし、計算資源とコストを節約。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-amber-300">5C1-3 (IPSJ-CSS2026331)<br>個人識別情報保護に向けた正規表現ルールとローカルLLMによる軽量な事前検出手法</td>
                  <td class="py-2.5 px-3">定型PIIは正規表現で即座に処理し、非定型・曖昧な候補のみローカルLLMでKEEP/DISCARD/REPLACE補正(3.24倍高速・推論失敗0件)。</td>
                  <td class="py-2.5 px-3 text-emerald-300">外部のサードパーティ製ロボットへ仕事やデータを安全に渡すための「実行基盤側での高速PIIマスキング」。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-purple-300">4E3-4 (IPSJ-CSS2026271)<br>Instruction-Conditioned Adapter (ICA)：Instructionに基づく動的制御によるPI防御</td>
                  <td class="py-2.5 px-3">ASIDEによるInstruction/Data分離に加え、Instructionの意味表現から各層の動的ゲートを生成しData側Adapter出力を制御。適応的攻撃ASRを19.2pt低減。</td>
                  <td class="py-2.5 px-3 text-emerald-300">コンクールで発表する「標準モデル」および参入企業の独自モデルにプラグイン可能な「間接プロンプトインジェクション(IPI)防御ハーネス」。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-purple-300">2D4-1 / 2D4-4 (IPSJ-CSS2026082 / 085)<br>単一時刻の入力摂動に対するVLAの脆弱性と動的Action Chunking / 特徴量誘導攻撃(FSA)</td>
                  <td class="py-2.5 px-3">VLAのAction Chunkingが1時刻のカメラ白飛びや摂動を増幅する問題を解明。未実行行動列との割引累積不一致度で実行長Hを動的短縮。</td>
                  <td class="py-2.5 px-3 text-emerald-300">「モデルに物理制御を投げっぱなしにしない実行基盤」。照明反射や敵対的パッチによるロボット暴走を1ms未満で検知し実行長を短縮。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-sky-300">1E2-2 (IPSJ-CSS2026024)<br>Control-State Poisoning (CSP) と Capability Non-Expansion Invariant (CNEI)</td>
                  <td class="py-2.5 px-3">正当に見える行動方針・運用情報・履歴の組合せで要求範囲を超えさせる攻撃を定義。モデル外の信頼ホストで Level(a) ≤ τ を実行前強制(誤介入0・100%遮断)。</td>
                  <td class="py-2.5 px-3 text-emerald-300">未知の外部AIモデルがメモ汚染等で「許可されたピッキング範囲を超える操作」を選んでも、店舗インフラ側のCNEIゲートで100%遮断。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-sky-300">1D2-4 / 3D2-1 (IPSJ-CSS2026017 / 146)<br>証跡対応関係の劣化測定とLocator/Lint強制 / 秘密分散を用いた多層LUT参照</td>
                  <td class="py-2.5 px-3">AIの要約反復で根拠位置(Locator)が0%へ劣化する非対称性を解明。Claim-Artifact-Locator三層バンドルと決定論的Lintで違反0%維持。2次元LUT秘密分散でO(1)ラウンド参照。</td>
                  <td class="py-2.5 px-3 text-emerald-300">モデルの革新的ロジックは秘匿したまま、「正規LUTからどの候補群を比較検討し、どの棚画像Locatorを根拠に選んだか」をお客様と店舗へ数学的に証明。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-indigo-300">3G1-3 / 3G2-2 / 2G4-5 (CSS2026 197 / 200 / 120)<br>コンソーシアムチェーン異種ポリシー検証 / ERC-8004証拠多重性 / 無記憶漸進的トラスト(MPT)</td>
                  <td class="py-2.5 px-3">企業別ポリシーを有向グラフ分割で秘匿合議。オンチェーン評判の帰属消失(証拠多重性)をContextBoundGateで防ぎ、現セッションの振る舞いのみで段階的に権限付与。</td>
                  <td class="py-2.5 px-3 text-emerald-300">店舗・物流・ロボ開発社・損保が各自の企業秘密を守りつつ合議するブロックチェーン基盤と、新規参入ロボットに段階的に仕事とインセンティブを与えるMPT。</td>
                </tr>
                <tr>
                  <td class="py-2.5 px-3 font-mono text-teal-300">5B1-4 / 4B2-1 (IPSJ-CSS2026321 / 228)<br>監査ログに適した指定確認者墨塗署名(DCSS) / 秘密鍵と署名判断をTEEに隔離した自動署名</td>
                  <td class="py-2.5 px-3">機密箇所をカメレオンハッシュで墨塗り(Sanitize)して公開検証可能にしつつ、有事には裁判所(指定確認者)のみが元文書を0.58msで検証できるDCSS。OP-TEEでのポリシー自動署名。</td>
                  <td class="py-2.5 px-3 text-emerald-300">「モデルの革新的部分や個人情報を墨塗り秘匿したまま公開監査でき、万が一の事故争議時のみ第三者・裁判所が検証できる」ハイブリッド保険モデル。</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      `;

      // Append individual node cards in Notes view
      const grid = document.createElement('div');
      grid.className = 'grid grid-cols-1 md:grid-cols-2 gap-6';
      nodes.forEach(node => {
        const cat = CATEGORIES[node.category] || CATEGORIES.lookup_zk;
        const card = document.createElement('div');
        card.className = `p-5 rounded-xl border ${cat.color} space-y-3`;
        card.innerHTML = `
          <div class="flex items-center justify-between">
            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${cat.tagColor}">${cat.name}</span>
            <span class="text-[10px] font-mono text-slate-400">${node.id}</span>
          </div>
          <h4 class="text-base font-bold text-slate-100">${node.title}</h4>
          <p class="text-xs font-mono text-emerald-400">${node.subtitle}</p>
          <p class="text-[11px] font-mono text-slate-400 bg-slate-950/60 p-2 rounded border border-slate-800">📄 ${node.paperRef}</p>
          <p class="text-xs text-slate-300 leading-relaxed">${node.desc}</p>
          <ul class="space-y-1.5 text-xs text-slate-300 list-disc pl-4 leading-relaxed">
            ${node.points.map(p => `<li>${p}</li>`).join('')}
          </ul>
        `;
        grid.appendChild(card);
      });
      container.appendChild(grid);
    }

    // --- Generate Export Markdown & JSON ---
    function generateExportData() {
      let md = `# スーパー・物流センター オープンロボット実行基盤 × モデル知財秘匿ZK監査 × トークン経済圏 統合仕様書\n\n`;
      md += `> **ビジネス・収益化モデル要約**: スーパーや物流センターがロボット群を自前で維持管理するのは困難であるため、店舗・倉庫側は「ロボットが稼働できる物理環境」と「ZK検証・ブロックチェーン決済インフラ（実行基盤）」のみを整備する。タスクや環境データを積極的に外部へ渡すことでサードパーティのロボット・AIモデル開発者にインセンティブ（報酬）が還流し、資本経済的に最も効率的なピッキング・物流最適化が実現する。この際、AI開発企業の「モデルの革新的部分（重み・独自アルゴリズム）」や「顧客のプライバシー」は一切開示せず、脆弱性・安全性の監査と「ルックアップで何と比較検討したか」の証明を数学的（ZK / vFHE / DCSS）に行うことで、店舗・開発者・保険会社・お客様の全員がトラストできるエコシステムを構築する。\n\n`;
      md += `> **PNG 3枚の統合内容**:\n`;
      md += `> - **image.png (Verifiable FHE)**: User(秘密データ x 🔒) → E(x) 送信 → Server(中身は見えない)がFHEで暗号文のまま f を評価 → E(f(x)) + π (ZK: 正しく計算した証明) を返送 → ④ユーザが復号 + π を検証し「機密性(FHE) AND 計算の正しさ(ZK)」を同時に得る。\n`;
      md += `> - **image copy.png (手書きホワイトボード)**: ①指標？ task → trace (APIコールlist) の check。「APIコールが"正しいか"（タスクリストに必要なAPIのみ呼び出す）」「事故率(etc...)/統計」「成功率(etc...)」「1. 正しいAPIを使ったか？」。②データの元（個人・法人）と損保会社の間でやりとりし、法人が「約款に合致している事を証明」、損保が「検証」。下部：「MPC / FHE で (task, trace) の check を encryption したまま評価する」。\n`;
      md += `> - **image copy 2.png (ZK, or not ZK: AIエージェント保険)**: サービスの機密データ(e.g., 顧客データ)を渡さずにAIエージェントの運用実績(e.g., タスク完了率)を外部の損保会社に証明する設計。検討事項：指標(e.g., ISO)と測定・証明方法、トラストモデル（誰・何を信頼するか）、現実的なトレードオフ。\n\n`;

      Object.keys(CATEGORIES).forEach(catKey => {
        const cat = CATEGORIES[catKey];
        md += `## ${cat.name}\n\n`;
        nodes.filter(n => n.category === catKey).forEach(n => {
          md += `### ${n.title} (${n.subtitle})\n`;
          md += `- **着想・根拠**: ${n.paperRef}\n`;
          md += `- **概要**: ${n.desc}\n`;
          n.points.forEach(p => {
            md += `  - ${p}\n`;
          });
          md += `- **タグ**: ${n.tags.join(', ')}\n\n`;
        });
      });

      document.getElementById('exportMarkdownArea').value = md;
      document.getElementById('exportJsonArea').value = JSON.stringify({ nodes, edges }, null, 2);
    }

    function copyExport(type) {
      const el = document.getElementById(type === 'md' ? 'exportMarkdownArea' : 'exportJsonArea');
      el.select();
      document.execCommand('copy');
    }

    // --- Add Node Modal ---
    function openAddNodeModal() {
      document.getElementById('addNodeModal').classList.remove('hidden');
    }
    function closeAddNodeModal() {
      document.getElementById('addNodeModal').classList.add('hidden');
    }
    function confirmAddNode() {
      const title = document.getElementById('newNodeTitle').value.trim();
      const subtitle = document.getElementById('newNodeSubtitle').value.trim();
      const domain = document.getElementById('newNodeDomain').value;
      const desc = document.getElementById('newNodeDesc').value.trim();
      if (!title) return;
      nodes.push({
        id: 'node_custom_' + Date.now(),
        domain: domain,
        category: domain,
        title: title,
        subtitle: subtitle || 'Custom Module',
        paperRef: 'Custom Whiteboard Extension',
        x: 400,
        y: 300,
        desc: desc || 'カスタム追加ノード',
        points: [desc || 'カスタム仕様ポイント'],
        tags: ['Custom', domain]
      });
      closeAddNodeModal();
      renderNodes();
      renderConnections();
    }

    // --- Initial Boot ---
    renderNodes();
    updateCanvasTransform();
  </script>
</body>
</html>
