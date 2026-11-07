# ProofPick（プルーフピック）

個別の注文数量を復元せずに共同購入の合計と成立条件を計算するWebアプリです。ブラウザで秘密分散した注文をREP3で集計し、Groth16証明を検証してから発注・受け取りへ進みます。

[ファイルの案内を開く（HTML）](index.html)

## フォルダの役割

- `src/`：共同購入アプリと分散 ID の連携。
- `crypto/`：秘密集計・証明・検証の回路と実行コード。
- `tests/`：テスト。`tests/reports/` は過去の検証結果。
- `integration/`：分散 IdP を接続するための設定。
- `slides/`：現在の発表スライド。`submission/`：応募資料と配布 ZIP。
- `true/`：大会の基本情報。元の位置と内容のまま。
- `archive/`：旧構想の資料、旧応募用紙、整理前の配布 ZIP。
- `docs/`：旧構想の公開用データ。現在の発表内容は `slides/` を参照。

VS Code 用に Material Icon Theme の拡張機能を推奨設定しています。有効になっていない場合は、拡張機能を有効化し、ファイルアイコンテーマとして選んでください。

## 別のWindows PCで起動する

Git、Python 3.12、Node.js 24、Rust 1.90以降（MSVC）、Visual Studio C++ Build Tools（MSVC x64/x86・Windows SDK）が必要です。

```powershell
git clone --depth 1 https://github.com/sururu-k/ProofPick.git
cd ProofPick
python -m venv .venv
$env:Path = "$PWD\.venv\Scripts;$env:Path"
powershell -File crypto/install.ps1 -BuildNative
python src/groupbuy_server.py
```

[アプリを開く](http://127.0.0.1:8765/)。すでにcloneしている場合は `git pull --ff-only` で更新できます。初回のRustビルドには数分かかります。DBとノード用の鍵は起動したPCで作成されます。

Gitを使わずに移す場合は [ソースZIP](submission/groupbuy-source.zip) を展開し、展開先で `python -m venv .venv` から実行してください。[詳しい再現手順](crypto/REPRODUCE.txt)

## 試用と応募資料

[発表スライド（HTML）](slides/index.html) — 矢印キーまたは画面下のボタンで進めます。

1. 販売者が募集を作成し、別々のブラウザプロファイルから2〜8件の注文を出す。
2. 主催者が受付を締め切り、販売者が「秘密のまま集計・ZK検証」を実行する。
3. 成立したら販売者が注文を開いて発注し、準備完了後に参加者が受け取りを記録する。

実証では3件の注文から合計9個・1,620円の証明を共同生成し、別実装で検証してから受け取りまで進めました。[応募資料と検証結果](submission/index.html)

1商品・固定単価の試用版です。同一PCの管理者・OSと開発用の証明パラメータを信頼します。成立後は、商品を用意する販売者に個別注文を開示します。予算確認はブラウザ内で行い、実決済や配送は接続していません。

[参考元と実装範囲](submission/product.html)。ソースZIPは `python submission/build_groupbuy_bundle.py` で再生成できます。

## 分散IDと共同購入を組み合わせる（ローカル試用）

[分散 IdP](https://github.com/sururu-k/decentralized_identity_provider) の PASTA / FROST 認証でログインし、ProofPick の注文を利用者に結びつけます。指定先のコミット `a54aa71` を使います。IdP の3ノードと ProofPick の秘密集計3者は別の仕組みです。

Docker と Docker Compose、Git、上記の ProofPick の実行環境が必要です。PowerShell の例：

```powershell
git clone https://github.com/sururu-k/decentralized_identity_provider.git .tools/pasta-idp
git -C .tools/pasta-idp checkout a54aa71
docker compose -f .tools/pasta-idp/docker-compose.yml -f integration/pasta-compose.yml up -d --build --wait
$env:PROOFPICK_IDENTITY = '1'
python src/groupbuy_server.py
```

`http://127.0.0.1:8765/` を開き「分散IDでログイン」を押します。IdP の事前登録ユーザー `alice` / `password123` を使うデモです。別の利用者は `bob` / `password456` です。動作確認にはブラウザプロファイルを分けてください。終了するときは `docker compose -f .tools/pasta-idp/docker-compose.yml -f integration/pasta-compose.yml down` を実行します。

認証モードでは API ごとに IdP の署名、発行元・宛先・期限と DPoP 証明（端末鍵・要求先・トークン・再利用）を検証します。参加者の注文操作には同じ分散IDと注文アクセス情報の両方が必要です。販売者・主催者の操作にはログインに加えて従来の秘密コードが必要で、秘密コード自体は特定のIDに固定されません。認証なしで作成した注文は認証モードの注文と別扱いです。販売者の復号鍵と注文アクセス情報は従来どおり各自で保存してください。

これは同一PC向けの試用で、IdP のユーザーや鍵はデモ用です。公開サービス向けの登録・鍵管理・HTTPS は未整備です。認証モードを使わない従来の起動方法も利用できます。元実装の利用条件は [IdP の README](https://github.com/sururu-k/decentralized_identity_provider/blob/a54aa71/README.md) に MIT License と記載されています。
