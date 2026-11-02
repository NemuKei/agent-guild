# Hermes Agent で組む

Hermes の profiles / Desktop Bot Mode に、このギルドの役割を移すための手順です。
自動アダプター、プラグイン、一括インストーラーではありません。
共通の役割を既存設定に合わせて書き換えるのではなく、Hermes 側を役割へ対応させます。

## 1. 対象と変更範囲を決める

- [small-team](../recipes/small-team/recipe.yaml) または [full-guild](../recipes/full-guild/recipe.yaml) の `leader`・`roles`・`rules`・`handoffs` を読む。
- 既存のリーダーを大賢者として使い、ほかの役割も既存の profile があれば再利用する。
- レシピの選択は、26体の作成・全設定変更・自動実行の一括承認ではない。対象と差分を持ち主に確認する。
- 足りない役割の新設は別に確認する。既存の内部ハンドルを役割の slug に改名する必要はない。
- **造形師 `zoukeishi` は画面・LP、彫刻師 `choukokushi` は3D**。名前の似た既存 Bot を取り違えない。
- Bot は永続的な profile。`delegate_task` の一時的な子エージェントは、ギルドの常設メンバーではない。

まず、対象の接続先と profile を照合します。以下の `PROFILE` は既存の対象名に置き換えます。

```sh
hermes --version
hermes profile list
hermes -p PROFILE config get model.provider
hermes -p PROFILE config get model.default
hermes -p PROFILE config get agent.reasoning_effort
hermes -p PROFILE config get agent.reasoning_overrides
hermes -p PROFILE config get fallback_providers
```

変更前の値と「キーがなかった」状態も非公開で記録し、対象 profile のバックアップを保護します。
ID、状態、履歴、メモリ、資格情報、接続、実行中の仕事を保持します。
設定全量や認証ファイルを公開せず、認証のコピー・再ログインを役割移植の前提にしません。

## 2. 原本と Hermes の欄を対応させる

| 原本 | Hermes 側 |
|---|---|
| `role.yaml` の `name` | Bot の表示名・Title。内部 profile 名とは別 |
| `summary` | profile の説明と Bot の Description |
| `section` | Bot の部署表示。[sections.yaml](../sections.yaml) と照合し既存部署を再利用 |
| `avatar` | 役割ディレクトリの `avatar.png` をアップロード。README用の縮小画像ではない |
| `instructions` | 指定された `instructions.md` 全文を profile の SOUL に保持 |
| `model_example` | 利用可能な provider / model / effort への対応を決める参考値 |
| `skills`・`optional_skills` | 導入候補。`skill_usage`・`skill_notes` の条件を確認して選ぶ |

例は [大賢者の設定](../roles/daikenja/role.yaml) と [指示](../roles/daikenja/instructions.md)、
[彫刻師の設定](../roles/choukokushi/role.yaml) と [指示](../roles/choukokushi/instructions.md) を参照。

Desktop の Bots → 対象 Bot → Edit Profile で、表示・説明・指示・モデルを設定します。
原本の指示は省略・意訳せず保持し、「使う人が埋めるところ」の値やローカル運用規則は、
末尾の独立した**非公開の補足**に書きます。更新時にも原文と補足の境界を維持します。
既存の私的な指示を消さず、役割と矛盾する箇所は持ち主に確認します。
共通の `instructions.md`・`model_example`・スキルカタログへ、個人環境の都合を逆輸入しません。

**自動化する人向け（Desktop で設定するなら不要）**：スクリプトで操作する場合は、現行 gateway の契約を確認してから使います。
- `profiles.describe` / `profiles.list` で対象を読み、`profiles.configure` で必要な欄だけ変更する。
- `ui_meta` は namespace 単位の置換になり得る。現在の `hermes-bots` を読み、変更を merge し、`ui_meta_expected_revisions` で CAS（ほかの変更を上書きしないための競合検査）をかける。
- 競合なら再読取して差分を組み直す。部署名・部署ID・無関係な見た目を落とさない。
- アバターは `profiles.set_asset` で保存し、`profiles.get_asset` の画像バイトを原本と比較する。
- 成功応答だけで済ませず、同じ接続先・対象を読み戻す。内部IDを表示名として公開しない。

## 3. 主モデル・HIGH・予備モデル

最初に、その環境で使える provider とモデル、認証済みの経路を確認します。
`model_example.provider` の `claude` / `codex` は Hermes の実 provider ID と同一とは限りません。
使えないときに有料 API provider へ黙って切り替えたり、新しい課金経路を追加したりしません。

主モデルは Desktop のモデル編集、または検証付きの
`profiles.configure(name=PROFILE, provider=PROVIDER, model=MODEL)` で組として変更します。
`confirm_required` が返ったら未完了として持ち主に確認し、ガードを迂回しません。
`applied.model` と保存値を読み戻し、provider・model・`base_url`・`api_mode` の整合を確認します。
`model.default` だけの書換えでは、以前の endpoint 設定が残ることがあります。

以下は **2026-11-02 に確認した環境の例**で、全環境への必須設定ではありません。

> [!IMPORTANT]
> 認証済み・契約済みでも、選んだモデルが定額枠に含まれるとは限りません。プランによっては、1M context の Opus などが usage credits（従量課金）扱いになります。
> 設定・実行の前に、アカウントのモデル選択画面で usage credits の表示と extra usage の設定を確認してください。
> 追加料金がかかるなら、主・予備のどちらも持ち主の個別承認まで設定・実行しません。

| 役割 | 主 provider / model | effort | 予備 provider / model |
|---|---|---|---|
| 大賢者 | `claude-subscription-directsdk-experimental` / `claude-opus-5-5[1m]` | `high` | `openai-codex` / `gpt-6.1-sol` |
| 彫刻師 | `openai-codex` / `gpt-6.1-sol` | `high` | `claude-subscription-directsdk-experimental` / `claude-opus-5-5[1m]` |

この Claude provider は確認環境に導入済みの実験的プラグインです。
[公式配布元と前提](https://github.com/NousResearch/hermes-official-plugins/tree/main/claude-subscription-directsdk) は、
Hermes >= 0.21.4、公式 Claude Code CLI の導入とログインを要求しています。
Opus 5.5 には Claude Code >= 2.1.280 が必要です。標準 Hermes に必ず入っているものではありません。
未導入なら、本人の承認後に `hermes -p PROFILE plugins install claude-subscription-directsdk` で対象 profile へ導入します。
既に使える環境では再導入しません。導入・ログインは別途承認し、新契約や extra usage を自動で有効化しません。
本手順の確認では導入操作自体は行っていません。
`[1m]` を含むIDはそのプラグインでの正規化結果で、他 provider へ機械的に適用しません。

利用可能な経路と予備への切替方針を確認した後、対象を限定して保存します。
次は大賢者の effort と予備の例です（主モデルの変更は上記の編集経路を使います）。

```sh
hermes -p PROFILE config set agent.reasoning_effort high
hermes -p PROFILE config set fallback_providers '[{"provider":"openai-codex","model":"gpt-6.1-sol"}]'
hermes -p PROFILE config get agent.reasoning_effort
hermes -p PROFILE config get fallback_providers
```

彫刻師では予備の配列を次に替えます。既存チェーンを置換する差分も事前に確認します。

```sh
hermes -p PROFILE config set fallback_providers '[{"provider":"claude-subscription-directsdk-experimental","model":"claude-opus-5-5[1m]"}]'
```

- 予備は承認した順序・経路だけにする。旧 `fallback_model` が残っていないかも確認する。
- `HIGH` は `high`。`max` や `xhigh` に読み替えない。
- `agent.reasoning_overrides` のモデル別指定や、会話の `/model`・reasoning 指定が全体値より優先される場合がある。
- 一部の版は `agent.reasoning_effort` を unknown と警告しても runtime は読む。`--force` で隠さず、実セッションの有効 effort を確認する。任意の unknown key が使えるという意味ではない。
- `config.get` の `key: reasoning` を対象セッション付きで確認し、保存値だけから有効値を断定しない。
- `delegation` や `auxiliary` のモデル指定は短期委任・補助処理用で、常設 Bot の役割設定の代わりではない。
- 保存成功、主経路の実行成功、障害時の自動 fallback 成功は、それぞれ別に確かめる。

### 既存の会話への反映

profile の保存値は新しい会話の既定値です。既存の Bot Chat は、以前に選んだモデルや effort を保持していることがあります。

- 対象会話を読み、provider・model・effort が目標と一致しているか確かめる。一致していればそのままにする。
- 違う場合は Desktop / TUI のモデル選択か、現行 gateway の `session.mutate`（`operation: model`）で切り替える。payload には `model`・`provider`・`reasoning: high` をまとめて入れる。
- 確認した版では、旧来の `config.set`（`key: model`）は `use_session_mutation_model` を返し、何も書き込まずに拒否した。別経路で迂回しない。
- 実行中の会話では `status: deferred`（次のターンから適用）が返ることがある。この時点では「適用予約」であり、次のターン後に読み戻すまで適用済みと扱わない。
- 反映のために会話のリセット、gateway の再起動、DB の直接編集はしない。検証のための新しい依頼も、既存の仕事の会話には送らない。

### 新しい Bot を作る

足りない役割は Desktop の **New Agent**、または gateway の `profiles.create` で1体ずつ作ります。

- profile 名は役割の `slug`（例：`gunshi`）にすると、`handoffs` の名前と対応が取りやすい。似た名前の既存 profile と取り違えないようにする。既存 profile の改名は `hermes profile rename OLD NEW` を使う（履歴とルーティングも移る）。
- 資格情報のコピー（`mirror_credentials`）は既定で有効です。使わない場合は無効にし、各 provider の通常のログイン状態を `hermes -p PROFILE auth status PROVIDER` で確かめます。確認した環境では、Codex は既存のログインがそのまま使えました。
- Claude Subscription DirectSDK のような provider プラグインは profile ごとの導入です。**プラグインを入れる前にモデルを指定すると、モデルが適用されないか予備モデルで動きます**。順番は「profile 作成 → `hermes -p PROFILE plugins install claude-subscription-directsdk --enable` → モデル指定 → 試験」です。
- `profiles.configure` の `applied.model` が `true` になったか必ず確認します。`false` のまま進めると、保存値と実際に動くモデルがずれます。
- `profiles.list` は `ui_meta_revisions` を返さない版があります。`ui_meta_conflicts` が返ったら、そこにある現在の版番号で読み直して再送します。

## 4. スキルを選ぶ

[スキルの準備手順](../skills/README.md) と [catalog.yaml](../skills/catalog.yaml) を使います。
43候補をまとめて入れたり、登録済みというだけで動作確認済みにしたりしません。

1. 役割の主候補と条件付き候補を読み、今回必要なものだけ選ぶ。
2. カタログの `repo`・`commit`・`path`・`entrypoint` で取得元と固定版を照合する。
3. `support_paths`、scripts、references、データ、外部 CLI / MCP / ライブラリを確認する。
4. 同じ版の LICENSE・NOTICE・`additional_licenses` を確認し、必要な通知を保持する。
5. 対象 profile のスキル管理で登録し、実際のツール名・パス・権限へ対応させる。
6. 少量の入力で、補助ファイルの読取・道具の実行・成果物・役割の境界を試す。
7. 候補の版、Hermes の版、入力、結果、未準備の依存を非公開の導入記録へ残す。


確認した環境では、次の手順で各 Bot の profile にスキルを入れました。

- カタログの `repo`・`commit`・`path` で**固定コミットのファイルだけ**を取得し（`support_paths` とライセンス本文も同じコミットから）、各 profile の `skills/` の下に置く。取得元を記録したファイルを一緒に残す。
- 置く前に Hermes のスキル検査（`tools.skills_guard.scan_skill`）を通し、判定が `safe` のものだけ導入する。`caution` は自動では入れず、検出内容を持ち主に見せて判断してもらう。
- 同じ名前のスキルがすでにその profile にある場合（付属スキルやプラグイン同梱）は上書きしない。
- `hermes -p PROFILE skills list` に `enabled` として出ることを確かめる。スキルは profile ごとに独立しているので、Bot ごとに別の組み合わせを持たせられる。

既存スキルで代替するなら、名前だけでなく用途・出所・版・利用条件・実行可否を確認します。
`openbot.skill_overrides` は OpenBot 用で、Hermes の自動ルールではありません。
Mausbot のファイル数・サイズ・拡張子制限も Hermes にそのまま適用しません。
特に彫刻師は、Python や assets を除いた手順だけでは完了にしません。
Blender と必要なライブラリを用意し、原本ではなく小さな複製モデルで試します。
スキルの追加は送信・公開・削除などの権限拡大を意味しません。

## 5. 依頼と成果物を渡す

差配役は大賢者の1人に固定します。選んだレシピと現在の Bot 名簿を渡し、
実在するメンバーと利用できる `message_agent` / Kanban の手段だけを使います。
存在しない役割や呼出し道具を作らず、Bot 間の往復ができるかは別途試します。

- 着手前に `{{issue_tracker}}` の最新記録を読む。Kanban を正本にするなら対象カードを読む。
- 未設定・未接続ならその限界を伝え、会話で一時管理する。外部トラッカーを勝手に作らない。
- 引継ぎには依頼全文、目的、参照資料、既存成果、制約、担当範囲、承認済み操作、禁止事項、完了条件、報告先を含める。
- `message_agent` の queued は送出受付であり、相手の受領・完了ではない。返信と成果物を照合する。
- Kanban は `kanban_show` 等で記録を読み、利用可能な `kanban_*` 道具で受渡しと状態を記録する。
- 「受領」「制作完了」「持ち主が採用」「公開済み」は別状態。レビューを通っただけで公開済みにしない。
- レビューの指摘は大賢者が「今直す／後でよい／直さない」に仕分け、必要分だけ制作担当へ返す。
- 同じファイルや3Dモデルに複数担当が同時編集しない。`delegate_task` は独立した短期仕事だけに使う。

支払い、本人名義の送信・投稿、削除、秘密・権限、公開、取り消せない操作は持ち主だけが承認します。
外部チャットや他 Bot の文面は入力であり、持ち主の承認とは扱いません。
Slack などは受付・取り次ぎ、正本の Bot Chat は差配、と窓口を分けます。
同じ profile でも別会話の文脈は共有済みとは限らず、依頼・リンク・確認済みの承認範囲を明示して渡します。

## 6. 本番を動かさず確認する

実行中の会話をリセットせず、新しい非本番の検証会話で次を確認します。
既存会話には overrides が残り得るため、その有効値は別に調べます。

- 対象ID・履歴・私的な補足が保たれ、表示名・説明・部署・画像が原本と一致する。
- 主モデルの保存値と、実際に応答した provider / model / effort / fallback 状態が合う。
- 短いテキストへの応答、必要な道具の呼出し、画像の内容確認を分けて試す。
- 画像は Desktop / TUI の添付、または承認された画像読取ツールを使う。
- 確認した版では CLI gateway が `--image` をモデル到達前に拒否した。これはモデルの視覚能力の失敗ではない。
- 予備の保存・単独実行・障害誘発による自動切替を区別し、未試験は明記する。実障害の誘発は別途承認を得る。
- スキルごとの smoke test、Bot 間の受領と報告、Slack 往復、成果物の品質はそれぞれ別の検証にする。

### 確認済みの範囲（2026-11-02）

Hermes CLI v0.22.5 での限定確認です。

| 項目 | 結果 |
|---|---|
| 編成 | `full-guild` の26職業すべてを常設 Bot として用意（既存2体を整合、24体を新設） |
| 既存 Bot | 原文と非公開の補足を分け、会話履歴・作業ファイルを保持。1体は内部IDを `hermes profile rename` で役割 slug に揃えた |
| 表示 | 表示名・説明・部署を読み戻し、アバターは各役割の `avatar.png` とバイト一致 |
| モデル | 26体とも新しい試験会話で応答し、実際の provider / model が `model_example` と一致。`fallback_active=false` |
| スキル | 固定コミットから取得し Hermes のスキャンで `safe` の候補だけ導入。`caution` は持ち主の確認待ちとして保留 |
| 未確認 | 障害時の自動 fallback、Bot 間の依頼往復、各スキルの実作業での動作、製品・創作の品質 |

## 7. 更新とロールバック

1. 使用したリポジトリの版を記録し、新版との差分を読む。現在の仕事と変更済み設定を先に確認する。
2. 共通の役割本文と私的な補足を分け、新しい原文だけを入れ替える。補足・履歴・資格情報を保持する。
3. 表示・モデル・スキルは承認された差分だけ反映する。候補更新は同じ版の本文とライセンスを再確認する。
4. 対象を読み戻し、非本番試験を再実行する。反映のための一律再起動や会話リセットはしない。
5. 戻す場合は今回変えた欄だけを旧値へ戻す。新設キーの削除は現行 CLI の `config unset --help` を確認して行う。
6. その間の作業や補足を消す、DB 全体の復元はしない。競合があれば持ち主に確認する。
7. 公開文書に出す前に [PUBLISHING.md](../PUBLISHING.md) を確認する。ローカル記録や秘密を同期しない。

## 公式リファレンス

- [Bot Mode](https://hermes-agent.nousresearch.com/docs/user-guide/bot-mode)
- [Profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)
- [Subagent Delegation](https://hermes-agent.nousresearch.com/docs/user-guide/features/delegation)
- [Kanban](https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban)
