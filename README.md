# ProofPick（プルーフピック）

個別の注文数量を復元せずに共同購入の合計と成立条件を計算するWebアプリです。ブラウザで秘密分散した注文をREP3で集計し、Groth16証明を検証してから発注・受け取りへ進みます。

## 別のWindows PCで起動する

Git、Python 3.12、Node.js 24、Rust 1.90以降（MSVC）、Visual Studio C++ Build Tools（MSVC x64/x86・Windows SDK）が必要です。

```powershell
git clone --depth 1 https://github.com/sururu-k/ProofPick.git
cd ProofPick
python -m venv .venv
$env:Path = "$PWD\.venv\Scripts;$env:Path"
powershell -File crypto-groupbuy/install.ps1 -BuildNative
python prototype/groupbuy_server.py
```

[アプリを開く](http://127.0.0.1:8765/)。すでにcloneしている場合は `git pull --ff-only` で更新できます。初回のRustビルドには数分かかります。DBとノード用の鍵は起動したPCで作成されます。

Gitを使わずに移す場合は [ソースZIP](submission/groupbuy-source.zip) を展開し、展開先で `python -m venv .venv` から実行してください。[詳しい再現手順](crypto-groupbuy/REPRODUCE.txt)

## 試用と応募資料

1. 販売者が募集を作成し、別々のブラウザプロファイルから2〜8件の注文を出す。
2. 主催者が受付を締め切り、販売者が「秘密のまま集計・ZK検証」を実行する。
3. 成立したら販売者が注文を開いて発注し、準備完了後に参加者が受け取りを記録する。

実証では3件の注文から合計9個・1,620円の証明を共同生成し、別実装で検証してから受け取りまで進めました。[応募資料と検証結果](submission/index.html)

1商品・固定単価の試用版です。同一PCの管理者・OSと開発用の証明パラメータを信頼します。成立後は、商品を用意する販売者に個別注文を開示します。予算確認はブラウザ内で行い、実決済や配送は接続していません。

[参考元と実装範囲](submission/product.html)。ソースZIPは `python submission/build_groupbuy_bundle.py` で再生成できます。
