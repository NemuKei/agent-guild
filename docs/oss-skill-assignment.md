# OSSスキルの調査と割り当て

調査日: 2026-11-01

26人の役割の指示を読み、**43件のOSSスキルを役割別の共通候補として割り当てました**。25人に主候補または条件付きの候補を用意し、原文転送だけを担う伝令は追加なしとしています。

ここでの「割り当て」は、リポジトリに記録した導入候補です。元のスキル本文・ライセンス・必要な環境は確認していますが、OpenBot・Mausbotへの導入や実作業での動作確認はまだです。

## 全員の割り当て

各候補のリンクは、確認したコミットの本文へ移動します。用途と使う条件は各役割の `role.yaml` に記録しています。主候補も毎回すべてを起動するわけではありません。

<!-- BEGIN SKILL ASSIGNMENTS -->

| エージェント | 主候補 | 条件付きの候補 |
|---|---|---|
| [大賢者](../roles/daikenja/role.yaml) | — | [dispatching-parallel-agents][superpowers/dispatching-parallel-agents]、[stakeholder-update][kwp/stakeholder-update] |
| [伝令](../roles/denrei/role.yaml) | — | — |
| [使い魔](../roles/tsukaima/role.yaml) | — | [Screenshot Capture][openai/screenshot]、[agent-browser][vercel/agent-browser] |
| [召喚士](../roles/shoukanshi/role.yaml) | [agent-development][anthropics/agent-development]、[skill-creator][anthropics/skill-creator] | — |
| [錬金術師](../roles/renkinjutsushi/role.yaml) | [workflow-sop-builder][workflow-sop-builder] | [skill-creator][anthropics/skill-creator] |
| [書記官](../roles/shokikan/role.yaml) | [summarize-meeting][pm-skills/summarize-meeting] | [internal-comms][anthropics/internal-comms] |
| [軍師](../roles/gunshi/role.yaml) | [write-spec][kwp/write-spec]、[roadmap-update][kwp/roadmap-update] | [pre-mortem][pm-skills/pre-mortem] |
| [探求者](../roles/tankyuusha/role.yaml) | [knowledge-synthesis][kwp/knowledge-synthesis] | [competitive-brief][kwp/product-competitive-brief] |
| [占星術師](../roles/senseijutsushi/role.yaml) | [explore-data][kwp/explore-data]、[performance-report][kwp/performance-report]、[validate-data][kwp/validate-data] | [statistical-analysis][kwp/statistical-analysis] |
| [財務官](../roles/zaimukan/role.yaml) | — | [reconciliation][kwp/reconciliation]、[journal-entry][kwp/journal-entry] |
| [測量士](../roles/sokuryoushi/role.yaml) | [seo-audit][marketingskills/seo-audit]、[ai-seo][marketingskills/ai-seo]、[content-strategy][marketingskills/content-strategy] | — |
| [物見](../roles/monomi/role.yaml) | [competitive-brief][kwp/product-competitive-brief] | — |
| [造形師](../roles/zoukeishi/role.yaml) | [frontend-design][anthropics/frontend-design]、[yomiyasu][yomiyasu] | [ui-ux-pro-max][ui-ux-pro-max] |
| [彫刻師](../roles/choukokushi/role.yaml) | [Blender image to 3D][blender-game-skills/blender-image-to-3d] | — |
| [道化師](../roles/doukeshi/role.yaml) | [design-critique][kwp/design-critique] | — |
| [語り部](../roles/kataribe/role.yaml) | [content-creation][kwp/content-creation]、[yomiyasu][yomiyasu] | — |
| [文官](../roles/bunkan/role.yaml) | [internal-comms][anthropics/internal-comms]、[yomiyasu][yomiyasu] | — |
| [鍛冶師](../roles/kajishi/role.yaml) | [test-driven-development][superpowers/test-driven-development]、[verification-before-completion][superpowers/verification-before-completion] | — |
| [鑑定士](../roles/kanteishi/role.yaml) | [code-review-excellence][wshobson/code-review-excellence] | [security-best-practices][openai/security-best-practices] |
| [治癒師](../roles/chiyushi/role.yaml) | [systematic-debugging][superpowers/systematic-debugging]、[verification-before-completion][superpowers/verification-before-completion] | [test-driven-development][superpowers/test-driven-development] |
| [結界師](../roles/kekkaishi/role.yaml) | [security-threat-model][openai/security-threat-model]、[security-best-practices][openai/security-best-practices] | — |
| [旗手](../roles/kishu/role.yaml) | [release-notes][pm-skills/release-notes]、[summarize-meeting][pm-skills/summarize-meeting]、[roadmap-update][kwp/roadmap-update] | — |
| [斥候](../roles/sekkou/role.yaml) | [account-research][kwp/account-research] | [call-prep][kwp/call-prep]、[knowledge-synthesis][kwp/knowledge-synthesis] |
| [吟遊詩人](../roles/ginyuushijin/role.yaml) | [account-research][kwp/account-research]、[draft-outreach][kwp/draft-outreach]、[yomiyasu][yomiyasu] | — |
| [案内人](../roles/annainin/role.yaml) | [draft-response][kwp/draft-response]、[ticket-triage][kwp/ticket-triage] | [customer-escalation][kwp/customer-escalation] |
| [試験官](../roles/shikenkan/role.yaml) | [interview-prep][kwp/interview-prep] | [summarize-meeting][pm-skills/summarize-meeting] |

<!-- END SKILL ASSIGNMENTS -->

この表は共通候補の一覧です。大賢者の並列委任はOpenBotで試してから判断し、財務官の候補は実際の帳簿で小さく試すまでは条件付きです。使い魔の画面取得・ブラウザ操作の候補はMausbotなど別のアプリ向けで、OpenBotではアプリの道具を使います。詳しい条件は以下と各役割の `skill_usage` に記録しています。

## 共通候補とOpenBotでの置き換え

共通候補を残したまま、OpenBotでの重複導入を省く条件を各役割の `openbot.skill_overrides` に分けて記録しています。

| 役割 | 共通のOSS候補 | OpenBot内で確認する既存候補名 |
|---|---|---|
| 文官 | `anthropics/internal-comms`（主候補） | `internal-communications` |
| 書記官 | `anthropics/internal-comms`（条件付き） | `internal-communications` |
| 造形師 | `anthropics/frontend-design`（主候補） | `distinctive-frontend-design` |
| 錬金術師 | `anthropics/skill-creator`（条件付き） | `openbot-skill-creator` |

右列は開発時の既存環境の記録にある名前で、どのOpenBot環境にもあるとは限りません。公開元・版・適用LICENSEも未確認のため、OSSカタログには追加していません。利用者のアプリ内で存在・利用可否・用途・利用条件を確認できた場合だけ置き換え、確認できなければ共通候補の固定版を取得する準備へ戻ります。既存スキルの本体を他のアプリへ転載できることを示す記録ではありません。

Mausbotなどから始める場合も、左列の共通候補をカタログの取得元から準備できます。差分の形式と導入手順は [`skills/README.md`](../skills/README.md) にあります。

## 選定した理由

名前から担当を推測せず、現在の `instructions.md` を基準に選びました。試験官には採用面接、測量士にはSEO・AI検索対策、彫刻師には参照画像を使う3D制作を割り当てています。

大賢者の`dispatching-parallel-agents`は条件付きの候補です。Claude Code内部の下請けエージェントを並列に動かす前提のため、OpenBotではチームメイトへの依頼とチャンネルの振り分けを優先し、試してから主候補にするかを決めます。作業状況は役割の指示にある課題管理で管理し、別のタスク台帳を新しく作る設計にはしていません。伝令は原文を転送する専任役なので追加なしです。

### 既存候補から見直した点

- **語り部**: `doc-coauthoring`は選定時に確認した版で適用LICENSEを確定できなかったため、`content-creation`へ変更しました。GitHubで公開されていることだけをApache-2.0の根拠にはしていません。
- **文官・軍師**: `discernment-nudge`は利用者に追加質問を提示する用途で、短い自己検証とは違うため外しました。軍師は重要な計画に限って`pre-mortem`を使い、文官の判断点検は役割の指示で維持します。
- **案内人**: リポジトリのIssue・PRを扱う`triage`から、顧客問い合わせに合う`ticket-triage`へ変更しました。コードの原因調査は治癒師へ渡します。
- **財務官**: `reconciliation`と`journal-entry`は、米国の会社の月次決算を前提としており、日本の個人事業（青色申告）とは前提が違います。両方とも実際の帳簿で小さく試すまでは条件付きとし、照合補助や管轄・会計方針等を確認できた場合の仕訳案に限ります。管轄固有の税務判断や自動仕訳の対応済みとは扱いません。
- **探求者・物見**: 比較用のスキルは `product-management/skills/competitive-brief` を選び、`kwp/product-competitive-brief`というIDで明示しました。同じ公開元にあるmarketing版とは別です。
- **開発担当**: 本文と参照先を確認した、実装・原因調査・検証・独立したレビューの候補へ整理しました。汎用の計画スキルを全員へ一式入れる割り当てにはしていません。

## 出典とライセンス

取得元は作者・提供元のGitHub公開リポジトリです。43件すべてについて、本文と適用LICENSEを同じ40桁のコミットで取得して確認しました。本体は **MIT 15件、Apache-2.0 28件**です。スキル本体はこのリポジトリに同梱していません。

取得元・ファイルの場所・適用ライセンス・必要な環境・確認したファイルの識別子は [`skills/catalog.yaml`](../skills/catalog.yaml) に記録しています。

| 公開元 | 主な用途 |
|---|---|
| [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) | 企画、調査、営業、分析、採用、顧客対応、画面批評 |
| [anthropics/skills](https://github.com/anthropics/skills) / [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | 社内文書、UI、役割とスキルの設計 |
| [obra/superpowers](https://github.com/obra/superpowers) / [wshobson/agents](https://github.com/wshobson/agents) | 委任、実装、原因調査、検証、レビュー |
| [openai/skills](https://github.com/openai/skills) | 脅威分析、安全性のレビュー、画面取得 |
| [phuryn/pm-skills](https://github.com/phuryn/pm-skills) | 会議記録、リリースノート、計画の前提点検 |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | SEO、AI検索対策、記事企画 |
| [nanaism/yomiyasu](https://github.com/nanaism/yomiyasu) / [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 日本語の推敲、UI設計資料 |
| [Gayaya999/workflow-sop-builder](https://github.com/Gayaya999/workflow-sop-builder) | 手順書と自動化の仕様 |
| [majidmanzarpour/blender-game-skills](https://github.com/majidmanzarpour/blender-game-skills) | 参照画像からのBlender制作 |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | CLIが必要な場合のブラウザ操作 |

### 固定した版と追加の条件

- `interview-prep`と`design-critique`は、標準Apache-2.0全文を確認できる過去のコミットに固定しました。調査時の最新コミットとスキル本文は同じです。候補ごとに適用LICENSEを記録し、公開元全体を一律に同じ条件とは扱っていません。
- yomiyasuは確認した2.5.0に固定しています。MIT通知に加え、同梱の[Unicode License V3](https://github.com/nanaism/yomiyasu/blob/29d67ccb05e370b5958d72920a9cd1aa829dee80/skills/yomiyasu/UNICODE-LICENSE.txt)と参照文書の出典を保持します。
- ui-ux-pro-maxは確認した2.15.0に固定しています。スキルのMITライセンスは、生成UIで使う字体・画像・外部ライブラリの利用条件を代わりに与えるものではありません。

## アプリへ持ち込むときに残ること

今回確認したのは、役割との相性と公開元の本文・ライセンス・必要な環境です。OpenBot・Mausbotへの導入、ツールの接続、実作業での品質はまだ検証していません。

| 役割・候補 | 残る確認 |
|---|---|
| 大賢者・召喚士 | メンバーへの依頼、役割・定期実行の登録、実設定の読み戻しを利用先アプリへ対応させる |
| 物見 | 固定対象、前回との差分、取得日時、定期実行、変化なしの記録を用意する |
| 財務官 | 米国の会社向けの前提を確認し、日本の個人事業（青色申告）の実際の帳簿で小さく試す。原本・台帳・機密情報の制限を保つ |
| 結界師・鑑定士 | OpenAIの安全性スキルは明示的な安全性依頼で使う。best-practicesの対象はPython・JavaScript・TypeScript・Go |
| 使い魔 | agent-browserとscreenshotはOpenBotでは使わない。ブラウザ操作・画面取得ともOpenBotの道具を使う。Mausbotなど別のアプリではCLI環境と画面取得の範囲を確認する |
| 彫刻師 | BlenderとPython等の環境を用意し、複製したモデルで参照画像との一致を確かめる |
| yomiyasu・ui-ux-pro-max等 | 本文に加えてscripts・references・辞書・補助データと通知を同じ版で取得する |

スキル本文にある別アプリのツール名やパスは、利用先に合わせます。`agent-development`には固定版に存在しない検証スクリプトへの参照があるため、起動確認を別途用意する必要があります。ブラウザ用の入口ファイルだけ、あるいは`SKILL.md`だけを取得して動作確認済みとは扱いません。

批評・下書き担当の候補に送信や変更の例があっても、役割の指示と依頼範囲を優先します。追加のスキルが操作権限を増やすことはありません。

## 最初の試行

提供した資料だけで結果を比べやすい仕事から始められます。

| 役割 | 小さな試行 | 確かめる点 |
|---|---|---|
| 書記官 | 短い会議メモから決定・担当・期限を整理 | 書かれていない約束を作らないか |
| 案内人 | 既知の問い合わせと製品資料から返信案を作る | 事実・不明点・追加確認を分けられるか |
| 治癒師 | 再現可能な小さな不具合を調べる | 仮説と証拠を結び付け、修正後に元の症状を確認するか |

試した候補のコミット、アプリ名・版、入力、結果、不足を残します。業務手順・Blenderなどのコミュニティ候補も、実務での有効性を小さく確かめてから採用範囲を広げます。準備の手順は [`skills/README.md`](../skills/README.md)、アプリごとの手順は [`adapters/`](../adapters/) にあります。

[kwp/stakeholder-update]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/product-management/skills/stakeholder-update/SKILL.md
[kwp/knowledge-synthesis]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/enterprise-search/skills/knowledge-synthesis/SKILL.md
[kwp/roadmap-update]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/product-management/skills/roadmap-update/SKILL.md
[kwp/write-spec]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/product-management/skills/write-spec/SKILL.md
[kwp/product-competitive-brief]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/product-management/skills/competitive-brief/SKILL.md
[kwp/account-research]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/sales/skills/account-research/SKILL.md
[kwp/call-prep]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/sales/skills/call-prep/SKILL.md
[kwp/performance-report]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/marketing/skills/performance-report/SKILL.md
[kwp/explore-data]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/data/skills/explore-data/SKILL.md
[kwp/validate-data]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/data/skills/validate-data/SKILL.md
[kwp/reconciliation]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/finance/skills/reconciliation/SKILL.md
[pm-skills/pre-mortem]: https://github.com/phuryn/pm-skills/blob/2a12295a7717569baa7be181b4cfebe3ca38a6bb/pm-execution/skills/pre-mortem/SKILL.md
[pm-skills/release-notes]: https://github.com/phuryn/pm-skills/blob/2a12295a7717569baa7be181b4cfebe3ca38a6bb/pm-execution/skills/release-notes/SKILL.md
[pm-skills/summarize-meeting]: https://github.com/phuryn/pm-skills/blob/2a12295a7717569baa7be181b4cfebe3ca38a6bb/pm-execution/skills/summarize-meeting/SKILL.md
[kwp/interview-prep]: https://github.com/anthropics/knowledge-work-plugins/blob/4fa3cb92e2942d6594200fa8d2c800708e086072/human-resources/skills/interview-prep/SKILL.md
[anthropics/internal-comms]: https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/internal-comms/SKILL.md
[yomiyasu]: https://github.com/nanaism/yomiyasu/blob/29d67ccb05e370b5958d72920a9cd1aa829dee80/skills/yomiyasu/SKILL.md
[kwp/draft-outreach]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/sales/skills/draft-outreach/SKILL.md
[kwp/content-creation]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/marketing/skills/content-creation/SKILL.md
[marketingskills/seo-audit]: https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/seo-audit/SKILL.md
[marketingskills/ai-seo]: https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/ai-seo/SKILL.md
[marketingskills/content-strategy]: https://github.com/coreyhaines31/marketingskills/blob/88c79f6528a9347420e57ceb1fff9a60de651768/skills/content-strategy/SKILL.md
[anthropics/frontend-design]: https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/frontend-design/SKILL.md
[ui-ux-pro-max]: https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/3a13158ff1f32156cbe144108de48eda2ecaed9a/.claude/skills/ui-ux-pro-max/SKILL.md
[kwp/design-critique]: https://github.com/anthropics/knowledge-work-plugins/blob/2d6f7e22dd25593f0f748010430ef86f19659735/design/skills/design-critique/SKILL.md
[kwp/draft-response]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/customer-support/skills/draft-response/SKILL.md
[kwp/ticket-triage]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/customer-support/skills/ticket-triage/SKILL.md
[kwp/customer-escalation]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/customer-support/skills/customer-escalation/SKILL.md
[superpowers/test-driven-development]: https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development/SKILL.md
[superpowers/verification-before-completion]: https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md
[superpowers/systematic-debugging]: https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md
[wshobson/code-review-excellence]: https://github.com/wshobson/agents/blob/7e2fb559cf4b824b27f1fec49fe88f7511066d26/plugins/developer-essentials/skills/code-review-excellence/SKILL.md
[openai/security-threat-model]: https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-threat-model/SKILL.md
[openai/security-best-practices]: https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/security-best-practices/SKILL.md
[anthropics/agent-development]: https://github.com/anthropics/claude-plugins-official/blob/a7ba5b93db0c7c8d17f3f1d25853adca79598a1a/plugins/plugin-dev/skills/agent-development/SKILL.md
[anthropics/skill-creator]: https://github.com/anthropics/skills/blob/ca45fc496a3436251f191354091d557da31c15b5/skills/skill-creator/SKILL.md
[workflow-sop-builder]: https://github.com/Gayaya999/workflow-sop-builder/blob/96756a36dcbf61f4a87e9ccca53b932a2556f369/SKILL.md
[blender-game-skills/blender-image-to-3d]: https://github.com/majidmanzarpour/blender-game-skills/blob/f0ef29385a03de139957e6f700b801cdc00b7e29/skills/blender-image-to-3d/SKILL.md
[vercel/agent-browser]: https://github.com/vercel-labs/agent-browser/blob/5868f7c05020e047c00e68e4abf9253cce864f41/skills/agent-browser/SKILL.md
[openai/screenshot]: https://github.com/openai/skills/blob/49f948faa9258a0c61caceaf225e179651397431/skills/.curated/screenshot/SKILL.md
[superpowers/dispatching-parallel-agents]: https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/dispatching-parallel-agents/SKILL.md
[kwp/journal-entry]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/finance/skills/journal-entry/SKILL.md
[kwp/statistical-analysis]: https://github.com/anthropics/knowledge-work-plugins/blob/2574e29377c7173d0cecffef29a6ecbd7f8ccb5d/data/skills/statistical-analysis/SKILL.md
