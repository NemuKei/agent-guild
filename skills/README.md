# スキルを選んで準備する

## ファイルの読み方

| 場所 | 何を表すか |
|---|---|
| `skills/catalog.yaml` | スキルの取得元・固定した版・適用ライセンス・必要な環境・使う役割 |
| `roles/<役割>/role.yaml` の `skills` | その役割の主候補。毎回すべてを起動するという意味ではない |
| 同じファイルの `optional_skills` | 条件に合う仕事を頼まれた場合だけ使う候補 |
| 同じファイルの `skill_usage` | 候補ごとの目的と使う条件 |
| 同じファイルの `skill_notes` | 担当範囲の制約、補えない仕事、導入時に確かめること |
| 同じファイルの `openbot.skill_overrides` | OpenBotに同じ用途の既存スキルがある場合の、共通候補からの置き換え条件 |

人が読む一覧は [`OSSスキルの調査と割り当て`](../docs/oss-skill-assignment.md) にあります。`used_by` は主候補・条件付き候補の両方を含みます。実機にインストール済みという意味ではありません。

## 導入するとき

1. 役割と依頼内容に合うスキルを選び、`skill_usage` を読む。OpenBotでは、下記の `skill_overrides` も確認する。
2. `catalog.yaml` の `repo` と `commit` で版を指定し、`path` にあるフォルダを取得する。`entrypoint` は最初に読むファイル。`scripts/`・`references/`・辞書・補助データ、`support_paths` も確認する。
3. 本体を配布する場合は `license_path` のライセンス本文、著作権表示、必要なNOTICE、`additional_licenses` の通知を保つ。変更した部分も記録する。スキルが紹介する第三者の素材には、その素材自身の条件がある。
4. 利用先アプリのツール名・保存場所・接続先・スキルの起動方法へ対応させる。CLIが必要な候補では実行環境も用意する。別のアプリ専用の道具を、利用できるものとして呼び出さない。
5. `instructions.md` にある役割と行動範囲を維持する。スキルの追加によって、下書き担当が送信する、レビュー担当が実装する、といった権限の拡大を起こさない。
6. 少量の入力で、必要なファイルを読めるか、役割に合う結果が出るか、依頼範囲を守るかを確認する。候補のコミット、アプリ名・版、入力、結果、不足を記録する。

必要な候補だけを使います。確認手順や質問の回数を、仕事の規模に関係なく一律に強制しないようにします。自動で一括インストールする仕組みはまだありません。

## 共通候補とアプリごとの置き換え

`skills`・`optional_skills` は、利用先アプリによらない共通候補です。特定のOpenBot環境で同じ用途のスキルを使っていても、共通候補は削除せず、その役割の `openbot.skill_overrides` に差分を記録します。これはこのリポジトリでの導入判断用のメタデータで、OpenBotが自動で読み込む設定ではありません。

```yaml
openbot:
  skill_overrides:
  - skill: anthropics/internal-comms
    action: use_existing_if_available
    existing_skill: internal-communications
    fallback: use_catalog_skill
```

`skill` はその役割に割り当てたカタログID、`existing_skill` はOpenBot内で探す候補名です。`use_existing_if_available` は、利用者のアプリ内で候補の存在・利用可否・用途・利用条件を確認できた場合だけ、共通候補の重複導入を省くという意味です。既存候補がない、確認できない、用途に合わない場合は、`use_catalog_skill` に従ってカタログの固定版を使う準備へ戻ります。共通候補の環境確認と小さな試行も必要です。

既存候補の公開元・版・適用LICENSEはこのリポジトリでは未確認です。名前の一致だけでOSSとみなしたり、存在や互換性を保証したりしません。Mausbotなど別のアプリでは共通候補から選びます。`optional_skills` の発動条件と役割の権限は、置き換えても変わりません。

## 確認した範囲

元作者の公開リポジトリから本文とライセンスを取得し、担当する仕事との相性、必要な道具や参照ファイルを確認しました。`verification.runtime_tested: false` は、利用先アプリでの実行をまだ確かめていないという意味です。

`catalog.yaml` の本体はMITまたはApache-2.0です。yomiyasuのUnicode由来データなど、追加の条件は個別に記録しています。リポジトリ全体や、紹介されている外部素材へ同じライセンスを一律に当てはめないでください。

## 候補と一覧を更新するとき

候補を更新するときは、本文・ライセンス・必要なファイルを同じコミットで確認し直します。役割を増減・変更したときは、`skills`・`optional_skills`・`skill_usage` とカタログの `used_by` も合わせます。アプリ固有の置き換えは、共通候補を残して `openbot.skill_overrides` を更新します。

リポジトリのルートで、次のコマンドを実行します。

```sh
python3 -m pip install -r requirements-dev.txt
python3 tools/sync_skill_assignments.py
python3 tools/sync_skill_assignments.py --check
```

一覧表は `sections.yaml` の役割順と、各役割・カタログのデータから生成します。`docs/oss-skill-assignment.md` のマーカー内は手で編集せず、用途やアプリごとの補足は表の外へ書きます。`--check` はファイルを変更せず、不整合があれば失敗します。変更を出す前の確認は [`PUBLISHING.md`](../PUBLISHING.md) にあります。
