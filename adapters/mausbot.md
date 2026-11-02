# Mausbot（OpenMausBot）で組む

Mausbot では、エージェントを「ボット」と呼びます。最初からリーダーのボットがいる形です。

## 手順

1. レシピを選び、既存のリーダーを `leader` に指定された大賢者（`daikenja`）として使う。新しく作るのは `roles` から大賢者を除いた役割だけ。`small-team` なら残り6人、`full-guild` なら残り25人を作る。
2. 既存のリーダーを含む各ボットに、対応する役割のファイルを使って次を設定する。リーダーには `roles/daikenja/` の設定を使う。
   - **名前・肩書き**：`role.yaml` の `name` と `summary`
   - **指示**：`instructions.md` の全文。最後の「使う人が埋めるところ」を、自分のプロジェクトに合わせて書き足す
   - **モデルと考える深さ**：`role.yaml` の `model_example` を参考に選ぶ
   - **セクション**：`role.yaml` の `section`
   - **アイコン**：`avatar.png`
3. 選んだレシピの `roles`・`rules`・`handoffs` を大賢者に共有する。`handoffs` は成果物の受け渡し先を表し、実際の依頼は大賢者が振り分ける。大賢者の `{{issue_tracker}}` に作業の記録先を設定する。未設定・未接続なら、指示にあるとおり会話内で一時管理する。
4. 共通の `skills` を主候補として、`optional_skills` は `skill_usage` の条件に合うものだけ選ぶ。`openbot` 配下の実設定や `skill_overrides` はOpenBot専用なので、Mausbotで候補を省略する根拠にはしない。[`スキルの準備手順`](../skills/README.md) に従って、`catalog.yaml` の固定コミットから必要なファイルとライセンス通知を取得する。利用するエージェント（Claudeなど）の配置方法・参照パスを確かめ、少量の入力で試す。

## わかったこと（2026-11-01、OpenMausBot 0.1.137）

### ボットの設定

- ボットをまとめて読み込む機能はない。リーダー（大賢者）が1体ずつ設定する。
- リーダーは、チームのボットの名前・肩書き・指示を書き換えられる。変更はすぐ反映され、利用者は元に戻せる。
- アイコンはツールから設定できない。各ボットの設定画面で、利用者が `avatar.png` を手で設定する。
- 指示を同期するときは、`instructions.md` の本文をそのまま使い、「使う人が埋めるところ」だけに自分のプロジェクトの中身を書く。こうすると、次の同期でもプロジェクト固有の中身を失わない。

### スキル

- スキルはボットごとに持たせられる。リーダーが他のボットのスキルを直接登録することはできないので、各ボットに「`role.yaml` の `skills` を固定コミットから取得して、自分で登録する」よう頼む。
- 登録できる形には次の制限がある。
  - 置けるのは `SKILL.md` と `references/<小文字の名前>.md` だけ。
  - 補助ファイルは1スキルあたり最大8個まで。
  - 1ファイルの大きさは約32KBまで。
  - プログラムのファイル（`.py`・`.sh`・`.ts`・`.html`・`.json` など）は置けない。
- 元の構成が違う場合は、中身を変えずに置き場所とリンクだけを直す。
  - `SKILL.md` の隣や `examples/` にある参照ファイルは `references/` に移し、本文の参照先もそれに合わせて書き換える。
  - スキルのフォルダの外を指すリンク（例：`../../CONNECTORS.md`）は、同じコミットのファイルを `references/connectors.md` として取り込み、リンク先を書き換える。
  - ライセンスの本文は `references/license.md` として残す。
- yomiyasu は、利用者の環境でプラグインとして導入済みで、そのボットから使える場合は、ボットごとの登録が要らない。導入していない場合は、ほかのスキルと同じ手順で登録する。
- 登録したスキルの中身は、`~/.openmausbot/workspaces/<ボットID>/skills/<スキル名>/` に保存される。あとで更新すると、`skills/.revisions/<ハッシュ>/` に移る。
- 登録後は、リーダーが登録されたファイルと固定コミットの元ファイルを比べ、上の書き換え以外に差がないことを確かめた。

### Slack

- Slackからの依頼の取り次ぎ（伝令）は、Slackbotとしての接続を使う。そうすると、返事は利用者本人ではなくボットの名前で投稿される。
- Slackのメッセージは依頼の内容として扱い、指示や承認としては扱わない。

## OSSスキルの確認状況

元の本文とライセンスを確認した候補を記録しています。下の表は、OpenMausBot 0.1.137 で各ボットが登録し、固定コミットの元ファイルと中身が一致すること（置き場所とリンクの書き換えを除く）を確かめた結果です。少量の入力で試す動作確認はまだなので、`catalog.yaml` の `runtime_tested` は `false` のままにしています。

| スキル | 役割 | 結果 | 書き換え |
|---|---|---|---|
| superpowers/systematic-debugging | 治癒師 | 登録済み | 隣の参照ファイル7つ（テスト用を含む）を `references/` に移した |
| superpowers/verification-before-completion | 治癒師 | 登録済み | なし |
| wshobson/code-review-excellence | 鑑定士 | 登録済み | なし |
| openai/security-threat-model | 結界師 | 登録済み | なし |
| anthropics/frontend-design | 造形師 | 登録済み（ライセンス本文は未同梱。**未完了**） | ライセンス本文を `references/license.md` として残す作業が残っている。済むまで、再配布の条件を満たした登録とは言えない |
| anthropics/internal-comms | 文官 | 登録済み | `examples/` を `references/` に移した |
| kwp/draft-response・ticket-triage | 案内人 | 登録済み | CONNECTORS.md を取り込んだ |
| kwp/design-critique | 道化師 | 登録済み | CONNECTORS.md を取り込んだ |
| kwp/write-spec・roadmap-update | 軍師・旗手 | 登録済み | CONNECTORS.md を取り込んだ |
| kwp/product-competitive-brief | 物見 | 登録済み | CONNECTORS.md を取り込んだ |
| kwp/explore-data・validate-data・performance-report | 占星術師 | 登録済み | CONNECTORS.md を取り込んだ |
| kwp/account-research・draft-outreach | 吟遊詩人・斥候 | 登録済み | なし |
| kwp/content-creation | 語り部 | 登録済み | なし |
| kwp/interview-prep | 試験官 | 登録済み | なし |
| kwp/knowledge-synthesis | 探求者 | 登録済み | なし |
| pm-skills/release-notes・summarize-meeting | 旗手・書記官 | 登録済み | なし |
| marketingskills/content-strategy・seo-audit | 測量士 | 登録済み | なし |
| blender-game-skills/blender-image-to-3d | 彫刻師 | **部分登録・依存ファイル未準備** | `scripts/` と `assets/` のPythonは置けないので除いた。Markdownの手順だけが入っていて、手順が参照するPythonがないため、そのままは実行できない。必要なファイルをMausbotの外に用意する手順は未作成 |
| openai/security-best-practices | 結界師 | 登録できない | 必要な参照ファイルが32KBを超える |
| marketingskills/ai-seo | 測量士 | 登録できない | `SKILL.md` が約37KBで、参照ファイルも15個ある |
| workflow-sop-builder | 錬金術師 | 登録できない | 参照ファイルが11個あり、8個にまとめると32KBを超える |

登録できない3つは、制限に合わせて中身を削ると元の手順が変わるため、見送りました。必要になったら、使う部分だけを抜き出した版を別に作るかを検討します。
