<p align="center">
  <a href="roles/daikenja/"><img src="docs/assets/emblems/daikenja.png" width="72" alt="大賢者の紋章"></a>
  <a href="roles/gunshi/"><img src="docs/assets/emblems/gunshi.png" width="72" alt="軍師の紋章"></a>
  <a href="roles/tankyuusha/"><img src="docs/assets/emblems/tankyuusha.png" width="72" alt="探求者の紋章"></a>
  <a href="roles/zoukeishi/"><img src="docs/assets/emblems/zoukeishi.png" width="72" alt="造形師の紋章"></a>
  <a href="roles/kajishi/"><img src="docs/assets/emblems/kajishi.png" width="72" alt="鍛冶師の紋章"></a>
  <a href="roles/kanteishi/"><img src="docs/assets/emblems/kanteishi.png" width="72" alt="鑑定士の紋章"></a>
  <a href="roles/tsukaima/"><img src="docs/assets/emblems/tsukaima.png" width="72" alt="使い魔の紋章"></a>
</p>

<h1 align="center">agent-guild</h1>

<p align="center">
  <b>AIエージェントのチームを「ギルド」として組むための設計図</b><br>
  26の職業（役割）ごとの指示・紋章・スキル候補と、チームを組むための編成レシピ。
</p>

<p align="center">
  <a href="#入団の手順">入団の手順</a> ·
  <a href="#編成レシピ">編成レシピ</a> ·
  <a href="#ギルド名簿">ギルド名簿</a> ·
  <a href="#ギルドの掟">ギルドの掟</a> ·
  <a href="#ファイルの地図">ファイルの地図</a>
</p>

<p align="center"><sub>↑ 上に並んでいるのは、最初のパーティ（small-team）の7人です。</sub></p>

---

## これは何？

- **何が入っているか**：エージェント1人ずつの指示の全文（`instructions.md`）、役割の設定（`role.yaml`）、アイコン（`avatar.png`）、チームの分け方、まとめて組むためのレシピ。
- **誰向けか**：エージェントを何人も並べて仕事をリレーさせるアプリ（OpenBot、Mausbot など）で、チームを一から組む手間を省きたい人。
- **どこが違うか**：指示もスキルの選び方もファイルで読めます。利用アプリの機能に合わせて、役割と手順を移し替える設計です。
- **なぜ公開しているか**：これから広がりそうな、エージェントが仕事をリレーする型のアプリ向けに、実際に動かしているチームの設定を保管し、参考として公開しています。
- **スキルはOSSが基本**：エージェントに持たせるスキルは、特定のアプリの専用品ではなく、公開されているOSSを基本にしています。アプリを替えても同じ設計を持ち込めるようにするためです。

一括インストーラーではありません。アプリごとの手順を読み、役割と必要なスキルを選んで設定します。

## 入団の手順

1. **パーティを選ぶ** — [編成レシピ](#編成レシピ)から、7人の `small-team` か、26人の `full-guild` を選ぶ。
2. **エージェントを作る** — [`adapters/`](adapters/) にある、使っているアプリの手順に従う。指示は各役割の `instructions.md` をそのまま貼る。
3. **自分の冒険に合わせる** — 指示の最後の「使う人が埋めるところ」を、自分のプロジェクトに合わせて書き足す。大賢者には作業を記録する課題管理の場所も指定する。まだ決まっていなければ会話内で作業状況をまとめ、記録先が必要になった段階で確認する。
4. **装備（スキル）を選ぶ** — 各役割の `skills` と `optional_skills` を共通の候補として、`skill_usage` で用途を確かめる。OpenBotでは `openbot.skill_overrides` にある既存スキルも確認し、使える場合だけ重複する候補の追加を省く。詳しくは [`skills/README.md`](skills/README.md) の手順に従う。

> [!TIP]
> 迷ったら `small-team` から。差配・計画・調査・制作・開発・レビュー・画面操作がそろう、小さな編成です。

## 編成レシピ

| パーティ | 人数 | 向いている使い方 |
|---|---|---|
| 🛡️ [`small-team`](recipes/small-team/recipe.yaml) | 7人 | まず小さく始める。差配・計画・調査・制作・開発・レビュー・画面操作 |
| 🏰 [`full-guild`](recipes/full-guild/recipe.yaml) | 26人 | 運営から営業までそろえる |

役割の指示と編成レシピは、下の開発の流れをおすすめの設計として書いています。モデル名は例です。利用先で使えるものを選んでください。

`small-team` のおすすめの開発の流れ（モデルは例）：

```mermaid
flowchart LR
  owner["持ち主"] <-->|依頼・報告| sage["大賢者"]
  sage --> plan["軍師：計画"] --> build["鍛冶師：実装"] --> review["鑑定士：レビュー"]
  review -->|指摘| sage
  sage -.->|今直す分| build
  sage --> support["探求者・造形師・使い魔"]
```

情報の調査は探求者、制作は造形師、画面操作は使い魔へ。大賢者が結果を取りまとめて持ち主に報告し、レビューの指摘は「今直す／後でよい／直さない（やりすぎ）」に仕分けて、今直す分だけ鍛冶師へ返します。

<details>
<summary>この設計図を作った理由</summary>

エージェントを何人も並べて仕事をリレーさせるアプリ（OpenBot、Mausbot など）は増えています。ただ、使い始めると、まずチームを一から組む手間がかかります。誰に何を任せるか、どんな指示を書くか、どのスキルを持たせるかを、全部自分で決めなければなりません。

公開されているbotのマーケットプレイスもあります。ただ、多くはそのアプリの中でしか使えず、指示やスキルの中身も見えません。

このリポジトリは、チームの組み方をファイルとして公開します。どのアプリを使っていても、同じチームを組めるようにするのが目的です。

</details>

## ギルド名簿

5つの部署に26の職業。紋章を押すと、その役割のファイル（指示・設定・アイコン）が開きます。

### 運営　<sub>ギルドを回す</sub>

<table>
  <tr>
    <td align="center" valign="top">
      <a href="roles/daikenja/"><img src="docs/assets/emblems/daikenja.png" width="88" alt="大賢者の紋章"></a><br>
      <b>大賢者</b><br>
      <sub>Great Sage</sub><br>
      <sub>差配役</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/denrei/"><img src="docs/assets/emblems/denrei.png" width="88" alt="伝令の紋章"></a><br>
      <b>伝令</b><br>
      <sub>Messenger</sub><br>
      <sub>外部チャットの取り次ぎ</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/tsukaima/"><img src="docs/assets/emblems/tsukaima.png" width="88" alt="使い魔の紋章"></a><br>
      <b>使い魔</b><br>
      <sub>Familiar</sub><br>
      <sub>画面操作</sub>
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="roles/shoukanshi/"><img src="docs/assets/emblems/shoukanshi.png" width="88" alt="召喚士の紋章"></a><br>
      <b>召喚士</b><br>
      <sub>Summoner</sub><br>
      <sub>エージェントとスキルの設計</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/renkinjutsushi/"><img src="docs/assets/emblems/renkinjutsushi.png" width="88" alt="錬金術師の紋章"></a><br>
      <b>錬金術師</b><br>
      <sub>Alchemist</sub><br>
      <sub>手順書と自動化</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/shokikan/"><img src="docs/assets/emblems/shokikan.png" width="88" alt="書記官の紋章"></a><br>
      <b>書記官</b><br>
      <sub>Scrivener</sub><br>
      <sub>会議の記録</sub>
    </td>
  </tr>
</table>

### 企画・調査　<sub>地図を描く</sub>

<table>
  <tr>
    <td align="center" valign="top">
      <a href="roles/gunshi/"><img src="docs/assets/emblems/gunshi.png" width="88" alt="軍師の紋章"></a><br>
      <b>軍師</b><br>
      <sub>Strategist</sub><br>
      <sub>計画</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/tankyuusha/"><img src="docs/assets/emblems/tankyuusha.png" width="88" alt="探求者の紋章"></a><br>
      <b>探求者</b><br>
      <sub>Explorer</sub><br>
      <sub>調査</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/senseijutsushi/"><img src="docs/assets/emblems/senseijutsushi.png" width="88" alt="占星術師の紋章"></a><br>
      <b>占星術師</b><br>
      <sub>Astrologer</sub><br>
      <sub>施策の分析</sub>
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="roles/zaimukan/"><img src="docs/assets/emblems/zaimukan.png" width="88" alt="財務官の紋章"></a><br>
      <b>財務官</b><br>
      <sub>Finance Officer</sub><br>
      <sub>経理</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/sokuryoushi/"><img src="docs/assets/emblems/sokuryoushi.png" width="88" alt="測量士の紋章"></a><br>
      <b>測量士</b><br>
      <sub>Surveyor</sub><br>
      <sub>検索対策</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/monomi/"><img src="docs/assets/emblems/monomi.png" width="88" alt="物見の紋章"></a><br>
      <b>物見</b><br>
      <sub>Lookout</sub><br>
      <sub>競合の見張り</sub>
    </td>
  </tr>
</table>

### 制作　<sub>形にする</sub>

<table>
  <tr>
    <td align="center" valign="top">
      <a href="roles/zoukeishi/"><img src="docs/assets/emblems/zoukeishi.png" width="88" alt="造形師の紋章"></a><br>
      <b>造形師</b><br>
      <sub>Shaper</sub><br>
      <sub>画面とLP</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/choukokushi/"><img src="docs/assets/emblems/choukokushi.png" width="88" alt="彫刻師の紋章"></a><br>
      <b>彫刻師</b><br>
      <sub>Sculptor</sub><br>
      <sub>3D</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/doukeshi/"><img src="docs/assets/emblems/doukeshi.png" width="88" alt="道化師の紋章"></a><br>
      <b>道化師</b><br>
      <sub>Jester</sub><br>
      <sub>遊び心のレビュー</sub>
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="roles/kataribe/"><img src="docs/assets/emblems/kataribe.png" width="88" alt="語り部の紋章"></a><br>
      <b>語り部</b><br>
      <sub>Storyteller</sub><br>
      <sub>記事</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/bunkan/"><img src="docs/assets/emblems/bunkan.png" width="88" alt="文官の紋章"></a><br>
      <b>文官</b><br>
      <sub>Bureaucrat</sub><br>
      <sub>文書</sub>
    </td>
  </tr>
</table>

### 開発　<sub>鍛えて守る</sub>

<table>
  <tr>
    <td align="center" valign="top">
      <a href="roles/kajishi/"><img src="docs/assets/emblems/kajishi.png" width="88" alt="鍛冶師の紋章"></a><br>
      <b>鍛冶師</b><br>
      <sub>Blacksmith</sub><br>
      <sub>実装</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/kanteishi/"><img src="docs/assets/emblems/kanteishi.png" width="88" alt="鑑定士の紋章"></a><br>
      <b>鑑定士</b><br>
      <sub>Appraiser</sub><br>
      <sub>レビュー</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/chiyushi/"><img src="docs/assets/emblems/chiyushi.png" width="88" alt="治癒師の紋章"></a><br>
      <b>治癒師</b><br>
      <sub>Healer</sub><br>
      <sub>不具合の調査</sub>
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="roles/kekkaishi/"><img src="docs/assets/emblems/kekkaishi.png" width="88" alt="結界師の紋章"></a><br>
      <b>結界師</b><br>
      <sub>Barrier Master</sub><br>
      <sub>安全性</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/kishu/"><img src="docs/assets/emblems/kishu.png" width="88" alt="旗手の紋章"></a><br>
      <b>旗手</b><br>
      <sub>Banner Bearer</sub><br>
      <sub>リリース</sub>
    </td>
  </tr>
</table>

### 営業・広報　<sub>外とつなぐ</sub>

<table>
  <tr>
    <td align="center" valign="top">
      <a href="roles/sekkou/"><img src="docs/assets/emblems/sekkou.png" width="88" alt="斥候の紋章"></a><br>
      <b>斥候</b><br>
      <sub>Scout</sub><br>
      <sub>商談の下調べ</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/ginyuushijin/"><img src="docs/assets/emblems/ginyuushijin.png" width="88" alt="吟遊詩人の紋章"></a><br>
      <b>吟遊詩人</b><br>
      <sub>Bard</sub><br>
      <sub>営業の文面</sub>
    </td>
    <td align="center" valign="top">
      <a href="roles/annainin/"><img src="docs/assets/emblems/annainin.png" width="88" alt="案内人の紋章"></a><br>
      <b>案内人</b><br>
      <sub>Guide</sub><br>
      <sub>問い合わせの返事</sub>
    </td>
  </tr>
  <tr>
    <td align="center" valign="top">
      <a href="roles/shikenkan/"><img src="docs/assets/emblems/shikenkan.png" width="88" alt="試験官の紋章"></a><br>
      <b>試験官</b><br>
      <sub>Examiner</sub><br>
      <sub>採用面接</sub>
    </td>
  </tr>
</table>

## ギルドの掟

> [!IMPORTANT]
> **一、振り分けと取りまとめは、差配役（大賢者）だけが行う。**
> 持ち主の依頼は差配役が受け、いちばん合う担当に振り、結果をまとめて報告する。
>
> **一、設計・実装・レビューを分担し、指摘は差配役が仕分ける。**
> モデルの例は、設計・計画・別の見方での確認が Claude（Opus）、実装・不具合の調査が GPT-6.1-Sol。レビューも GPT-6.1-Sol を使う別のレビュー役が担当し、差配役が「今直す／後でよい／直さない（やりすぎ）」に仕分け、必要なものだけ実装の担当へ渡す。
>
> **一、持ち主の一言が要る操作がある。**
> 支払い、持ち主の名前での送信や投稿、データの削除、秘密や権限の扱い、公開、取り消せない操作は、持ち主が言うまでしない。

ふつうの開発は、設計・計画→実装→別のレビュー役が細かく確認→差配役が仕分け→必要な修正の順です。条件が絡むバグは、調査→別の見方で確認→修正→レビュー→仕分けの順で進めます。不具合の原因調査は、`full-guild` では治癒師が担います。治癒師のいない `small-team` では鍛冶師が兼務し、修正前に再現して原因を確かめます。原因調査が多いなら治癒師を追加してください。指示の本文は役割で書いており、特定のモデルには依存しません。

## ファイルの地図

| 場所 | 中身 |
|---|---|
| `roles/<役割>/instructions.md` | エージェントへの指示の全文。アプリの設定にそのまま貼れる |
| `roles/<役割>/role.yaml` | 役割の説明、部署、モデルの例、共通のスキル候補。`openbot` にはモデルの実設定と、その環境で確認するスキルの置き換え |
| `roles/<役割>/avatar.png` | 紋章（PNG、512×512） |
| `docs/assets/emblems/<役割>.png` | README表示用の紋章（192×192）。元のアイコンから縮小したもの |
| [`sections.yaml`](sections.yaml) | チームの分け方（運営・企画・調査・制作・開発・営業・広報） |
| [`skills/catalog.yaml`](skills/catalog.yaml) | 調査した43スキル。取得元・固定した版・適用ライセンス・必要な環境 |
| [`skills/README.md`](skills/README.md) | 主候補と条件付き候補の読み方、導入時の手順 |
| [`docs/oss-skill-assignment.md`](docs/oss-skill-assignment.md) | 26人の割り当て一覧と、選定した理由・残る課題 |
| [`tools/sync_skill_assignments.py`](tools/sync_skill_assignments.py) | 役割ファイルから割り当て表を更新し、参照や一覧のずれを確認する保守用ツール |
| [`recipes/`](recipes/) | チームをまとめて組むためのレシピ |
| [`adapters/`](adapters/) | アプリごとの組み方 |

## スキル（装備）について

26人の役割に合わせ、43件のOSSスキルを共通の導入候補として記録しています。取得元の本文と適用ライセンスを同じコミットで確認し、各役割の `role.yaml` に主候補・条件付き候補・用途をまとめました。OpenBotで既存スキルを使う場合の置き換えは、その役割の `openbot.skill_overrides` に分けてあります。

<details>
<summary>くわしく（条件付きの候補、確認の状況）</summary>

- 原文の転送だけを担う伝令は、スキルの追加なしです。
- 大賢者の並列委任と財務官の会計スキルは、条件付きの候補です。
- 使い魔のブラウザ操作・画面取得スキルは Mausbot など別のアプリ向けで、OpenBot では使いません。
- OpenBotで重複を省くときは、置き換え先のスキルが利用環境にあり、用途と利用条件が合うことを確認します。確認できなければ共通のOSS候補を使います。Mausbotなど別のアプリにはOpenBot用の置き換えを適用しません。
- このリポジトリにはスキル本体を同梱していません。各候補の固定版と確認日は `skills/catalog.yaml` に記録しています。アプリへの導入状況は利用環境によって異なります。この設計図だけで動作を保証するものではありません。割り当てを使う前に、必要なファイルとアプリごとの対応を確かめてください。

全員の割り当てと選定理由は [`docs/oss-skill-assignment.md`](docs/oss-skill-assignment.md) にあります。

</details>

表示用の紋章は `roles/<役割>/avatar.png` から縮小しています。

**紋章の画像について**

`docs/assets/emblems/` と `roles/<役割>/avatar.png` の紋章は、OpenAI の ChatGPT（画像生成）で作成した画像です（人の手で描いたものではありません）。作者は、これらの画像に著作権その他の権利がある場合、その範囲で [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/deed.ja) により放棄します（全文は [`docs/assets/emblems/CC0-1.0.txt`](docs/assets/emblems/CC0-1.0.txt)）。コードと文書は MIT License です。画像は現状のまま提供し、他の作品や商標と似ていないことは保証しません。

## ライセンス

[MIT](LICENSE)。紋章の画像は [CC0 1.0](docs/assets/emblems/CC0-1.0.txt)（上の「紋章の画像について」）。スキルは、それぞれのリポジトリのライセンスに従います。

<p align="center"><sub>⚔️ ようこそ、ギルドへ。最初の依頼は、パーティ選びから。</sub></p>
