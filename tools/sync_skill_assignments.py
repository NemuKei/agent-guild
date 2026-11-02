#!/usr/bin/env python3
"""役割データから割り当て表を同期する。--check は変更せず不一致を検出する。"""

import argparse
from pathlib import Path
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAMLが必要です。python -m pip install -r requirements-dev.txt を実行してください。", file=sys.stderr)
    raise SystemExit(2)


BEGIN = "<!-- BEGIN SKILL ASSIGNMENTS -->"
END = "<!-- END SKILL ASSIGNMENTS -->"
DOCUMENT = Path("docs/oss-skill-assignment.md")


class InvalidData(ValueError):
    """人が修正できる入力データの不整合。"""


def mapping(value, label):
    if not isinstance(value, dict):
        raise InvalidData(f"{label}: オブジェクトが必要です")
    return value


def sequence(value, label):
    if not isinstance(value, list):
        raise InvalidData(f"{label}: リストが必要です")
    return value


def string(value, label):
    if not isinstance(value, str) or not value.strip():
        raise InvalidData(f"{label}: 空でない文字列が必要です")
    return value


def string_list(value, label):
    values = sequence(value, label)
    for entry in values:
        string(entry, label)
    if len(values) != len(set(values)):
        raise InvalidData(f"{label}: 重複があります")
    return values


def load_yaml(root, path):
    value = yaml.safe_load((root / path).read_text(encoding="utf-8"))
    return mapping(value, str(path))


def load_assignments(root):
    catalog = load_yaml(root, "skills/catalog.yaml")
    skills = {}
    for raw in sequence(catalog.get("skills"), "catalog.skills"):
        entry = mapping(raw, "catalog.skillsの項目")
        skill_id = string(entry.get("id"), "catalog.skill.id")
        if skill_id in skills:
            raise InvalidData(f"catalog: スキルIDが重複しています: {skill_id}")
        string(entry.get("name"), f"{skill_id}.name")
        string(entry.get("source_url"), f"{skill_id}.source_url")
        string_list(entry.get("used_by"), f"{skill_id}.used_by")
        skills[skill_id] = entry

    roles = []
    seen_roles = set()
    actual_usage = {skill_id: set() for skill_id in skills}
    sections = load_yaml(root, "sections.yaml")
    for raw in sequence(sections.get("sections"), "sections"):
        section = mapping(raw, "sectionsの項目")
        name = string(section.get("name"), "section.name")
        for slug in string_list(section.get("roles"), f"section {name}.roles"):
            if not re.fullmatch(r"[a-z0-9][a-z0-9_-]*", slug):
                raise InvalidData(f"役割名に使えない文字があります: {slug}")
            if slug in seen_roles:
                raise InvalidData(f"複数の部署に同じ役割があります: {slug}")
            seen_roles.add(slug)
            role = load_yaml(root, Path("roles") / slug / "role.yaml")
            if role.get("slug") != slug or role.get("section") != name:
                raise InvalidData(f"{slug}: slugまたはsectionがsections.yamlと一致しません")
            string(role.get("name"), f"{slug}.name")
            primary = string_list(role.get("skills"), f"{slug}.skills")
            optional = string_list(role.get("optional_skills", []), f"{slug}.optional_skills")
            selected = primary + optional
            if len(selected) != len(set(selected)):
                raise InvalidData(f"{slug}: 主候補と条件付き候補に同じスキルがあります")
            for skill_id in selected:
                if skill_id not in skills:
                    raise InvalidData(f"{slug}: カタログにないスキルです: {skill_id}")
                actual_usage[skill_id].add(slug)
            usage_ids = [
                string(mapping(item, f"{slug}.skill_usageの項目").get("id"), f"{slug}.skill_usage.id")
                for item in sequence(role.get("skill_usage"), f"{slug}.skill_usage")
            ]
            if len(usage_ids) != len(set(usage_ids)) or set(usage_ids) != set(selected):
                raise InvalidData(f"{slug}: skill_usageとskills / optional_skillsが一致しません")
            validate_overrides(role, selected)
            roles.append(role)

    existing_roles = {path.parent.name for path in (root / "roles").glob("*/role.yaml")}
    if existing_roles != seen_roles:
        missing = ", ".join(sorted(existing_roles - seen_roles))
        raise InvalidData(f"sections.yamlに登録されていない役割があります: {missing}")
    for skill_id, entry in skills.items():
        if set(entry["used_by"]) != actual_usage[skill_id]:
            expected = ", ".join(sorted(actual_usage[skill_id])) or "なし"
            raise InvalidData(f"{skill_id}: used_byが役割の割り当てと一致しません（期待値: {expected}）")
    return roles, skills


def validate_overrides(role, selected):
    slug = role["slug"]
    openbot = mapping(role.get("openbot", {}), f"{slug}.openbot")
    overrides = sequence(openbot.get("skill_overrides", []), f"{slug}.openbot.skill_overrides")
    seen = set()
    for raw in overrides:
        entry = mapping(raw, f"{slug}.openbot.skill_overridesの項目")
        skill_id = string(entry.get("skill"), f"{slug}.skill_overrides.skill")
        if skill_id not in selected:
            raise InvalidData(f"{slug}: OpenBot差分の参照先が共通候補にありません: {skill_id}")
        if skill_id in seen:
            raise InvalidData(f"{slug}: OpenBot差分のスキルが重複しています: {skill_id}")
        seen.add(skill_id)
        if entry.get("action") != "use_existing_if_available":
            raise InvalidData(f"{slug}: 未対応のOpenBot差分actionです: {skill_id}")
        string(entry.get("existing_skill"), f"{slug}.{skill_id}.existing_skill")
        if entry.get("fallback") != "use_catalog_skill":
            raise InvalidData(f"{slug}: 既存スキルがない場合は共通候補へ戻すfallbackが必要です: {skill_id}")


def markdown_label(value):
    return " ".join(value.split()).replace("\\", "\\\\").replace("[", r"\[").replace("]", r"\]").replace("|", r"\|")


def render_table(roles, skills):
    def links(ids):
        return "、".join(f"[{markdown_label(skills[skill_id]['name'])}][{skill_id}]" for skill_id in ids) or "—"

    lines = ["| エージェント | 主候補 | 条件付きの候補 |", "|---|---|---|"]
    for role in roles:
        lines.append(
            f"| [{markdown_label(role['name'])}](../roles/{role['slug']}/role.yaml) "
            f"| {links(role['skills'])} | {links(role.get('optional_skills', []))} |"
        )
    return "\n".join(lines)


def synchronized_document(document, table, skills):
    if document.count(BEGIN) != 1 or document.count(END) != 1:
        raise InvalidData(f"{DOCUMENT}: BEGIN / ENDのマーカーを各1つ置いてください")
    start = document.index(BEGIN) + len(BEGIN)
    end = document.index(END)
    if start > end:
        raise InvalidData(f"{DOCUMENT}: マーカーの順序が逆です")
    definitions = {}
    for skill_id, url in re.findall(r"^\[([^\]]+)\]:[ \t]+(\S+)[ \t]*$", document, flags=re.MULTILINE):
        if skill_id in definitions:
            raise InvalidData(f"{DOCUMENT}: 出典リンク定義が重複しています: {skill_id}")
        definitions[skill_id] = url
    for skill_id, skill in skills.items():
        if definitions.get(skill_id) != skill["source_url"]:
            raise InvalidData(f"{DOCUMENT}: [{skill_id}]の出典リンクをcatalog.source_urlと一致させてください")
    return document[:start] + "\n\n" + table + "\n\n" + document[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="変更せず、一致していなければ終了コード1を返す")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="リポジトリの場所")
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        roles, skills = load_assignments(root)
        path = root / DOCUMENT
        document = path.read_text(encoding="utf-8")
        expected = synchronized_document(document, render_table(roles, skills), skills)
        if expected != document:
            if args.check:
                print(f"不一致: {DOCUMENT}。python tools/sync_skill_assignments.py で表を更新してください。", file=sys.stderr)
                return 1
            path.write_text(expected, encoding="utf-8")
            print(f"更新: {DOCUMENT}（マーカー内の表のみ）")
        else:
            print(f"一致: {DOCUMENT}")
        print(f"確認: {len(roles)}役、カタログ{len(skills)}件、割り当て・出典リンク・OpenBot差分")
        return 0
    except (OSError, InvalidData, yaml.YAMLError) as error:
        print(f"確認できません: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
