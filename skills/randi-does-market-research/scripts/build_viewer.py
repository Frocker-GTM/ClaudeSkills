#!/usr/bin/env python3
"""Validate a Randi Does Market Research JSON file and build the viewer.

Usage:
    python build_viewer.py <data.json> <output.html>

Exit 0 when there are no errors (warnings print but don't fail the build).
Exit 1 when validation finds errors. Fix every error. Decide on every warning.
"""
import json
import os
import re
import sys
from datetime import date
from html import escape

KINDS_REQUIRED = ["claim", "icp_experience", "core_messaging"]
KINDS = set(KINDS_REQUIRED) | {"differentiator"}
VERDICTS = {"validated", "plausible unconfirmed", "invalidated"}
DIRECTIONS = {"validates", "invalidates", "context"}
SOURCE_TYPES = {"independent", "company", "vendor-funded"}
SENTIMENTS = {"happy", "content", "frustrated", "angry"}
CLAIM_ORIGINS = {"user", "proposed"}
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EM_DASH = "\u2014"
BANNED = ["unlock", "elevate", "seamless", "robust", "game-changer", "game changer",
          "in today's landscape"]

errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def need(obj, key, where):
    if not isinstance(obj, dict) or obj.get(key) in (None, "", []):
        err(f"{where}: missing '{key}'")
        return False
    return True


def parse_date(s):
    if isinstance(s, str) and DATE_RE.match(s):
        try:
            return date.fromisoformat(s)
        except ValueError:
            return None
    return None


def check_date(d, where):
    if d is None:
        warn(f"{where}: no date. Use YYYY-MM-DD or 'undated'.")
    elif d == "undated":
        warn(f"{where}: undated source. Fill it in if the date is findable.")
    elif parse_date(d) is None:
        err(f"{where}: date must be YYYY-MM-DD or 'undated'")


def scan_style(node, path="$"):
    if isinstance(node, str):
        if EM_DASH in node:
            warn(f"{path}: em dash. Rewrite the sentence.")
        low = node.lower()
        for w in BANNED:
            if re.search(r"\b" + re.escape(w) + r"\b", low):
                warn(f"{path}: banned filler '{w}'.")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            scan_style(v, f"{path}[{i}]")
    elif isinstance(node, dict):
        for k, v in node.items():
            scan_style(v, f"{path}.{k}")


def check_sources(arr, where):
    if not isinstance(arr, list) or not arr:
        err(f"{where}: needs at least one source")
        return
    for i, s in enumerate(arr):
        w = f"{where}[{i}]"
        if need(s, "source", w):
            check_date(s.get("date"), w)


def validate_stage(stage):
    if not isinstance(stage, dict):
        err("stage: must be an object")
        return set()
    claim = stage.get("claim")
    if need(stage, "claim", "stage"):
        need(claim, "statement", "stage.claim")
        check_sources(claim.get("sources"), "stage.claim.sources")
    icp = stage.get("icp")
    if need(stage, "icp", "stage"):
        need(icp, "summary", "stage.icp")
        check_sources(icp.get("sources"), "stage.icp.sources")
    cm = stage.get("core_messaging")
    if need(stage, "core_messaging", "stage"):
        need(cm, "promise", "stage.core_messaging")
        need(cm, "tone_voice", "stage.core_messaging")
        check_sources(cm.get("sources"), "stage.core_messaging.sources")
    ids = set()
    diffs = stage.get("differentiators", [])
    if not isinstance(diffs, list):
        err("stage.differentiators: must be an array")
        return ids
    for i, d in enumerate(diffs):
        w = f"stage.differentiators[{i}]"
        if need(d, "id", w):
            if d["id"] in ids:
                err(f"{w}: duplicate id {d['id']}")
            ids.add(d["id"])
        need(d, "statement", w)
        need(d, "source", w)
        check_date(d.get("date") if isinstance(d, dict) else None, w)
    return ids


def age_of(d, research):
    pd = parse_date(d)
    if pd is None or research is None:
        return "undated"
    days = (research - pd).days
    if days > 730:
        return "aged"
    if days > 365:
        return "stale"
    return "fresh"


def validate_test(t, where, diff_ids, research):
    if not isinstance(t, dict):
        err(f"{where}: must be an object")
        return
    need(t, "id", where)
    need(t, "subject", where)
    need(t, "bottom_line", where)
    need(t, "reasoning", where)
    kind = t.get("kind")
    if kind not in KINDS:
        err(f"{where}: kind must be one of {sorted(KINDS)}")
    if kind == "differentiator":
        if t.get("differentiator_id") not in diff_ids:
            err(f"{where}: differentiator_id '{t.get('differentiator_id')}' not found in stage.differentiators")
    std = t.get("standard")
    if need(t, "standard", where):
        for k in ("validated", "plausible_unconfirmed", "invalidated"):
            need(std, k, f"{where}.standard")
    verdict = t.get("verdict")
    if verdict not in VERDICTS:
        err(f"{where}: verdict must be one of {sorted(VERDICTS)}")

    ev = t.get("evidence", [])
    if not isinstance(ev, list):
        err(f"{where}.evidence: must be an array")
        return
    if not ev:
        warn(f"{where}: no evidence logged. Every verdict needs its sources shown.")
    for i, e in enumerate(ev):
        w = f"{where}.evidence[{i}]"
        if not isinstance(e, dict):
            err(f"{w}: must be an object")
            continue
        need(e, "finding", w)
        need(e, "source", w)
        if e.get("direction") not in DIRECTIONS:
            err(f"{w}: direction must be one of {sorted(DIRECTIONS)}")
        if e.get("source_type") not in SOURCE_TYPES:
            err(f"{w}: source_type must be one of {sorted(SOURCE_TYPES)}")
        check_date(e.get("date"), w)
        if kind == "icp_experience" and e.get("direction") != "context":
            if e.get("sentiment") not in SENTIMENTS:
                err(f"{w}: ICP experience evidence needs sentiment, one of {sorted(SENTIMENTS)}")
        e["age"] = age_of(e.get("date"), research)

    dirs = {e.get("direction") for e in ev if isinstance(e, dict)}
    if ev and not ({"validates", "invalidates"} <= dirs):
        warn(f"{where}: evidence on one side only. Confirm you searched for the other side.")

    # Evidence weight and freshness checks on the deciding side.
    side = {"validated": "validates", "invalidated": "invalidates"}.get(verdict)
    if side:
        deciding = [e for e in ev if isinstance(e, dict) and e.get("direction") == side]
        if deciding and all(e.get("age") == "aged" for e in deciding):
            err(f"{where}: verdict '{verdict}' rests only on evidence over 24 months old. "
                "Aged evidence can't decide a verdict alone.")
        indep = [e for e in deciding if e.get("source_type") == "independent"]
        company_contra = side == "invalidates" and any(
            e.get("source_type") == "company" for e in deciding)
        if len(indep) < 3 and not company_contra:
            warn(f"{where}: verdict '{verdict}' has {len(indep)} independent '{side}' source(s). "
                 "Three make a finding. Confirm the locked standard allows this and say so in "
                 "reasoning, or change the verdict to plausible unconfirmed.")


def validate(data):
    for k in ("meta", "stage", "tests"):
        if k not in data:
            err(f"top level: missing '{k}'")
    if errors:
        return
    meta = data["meta"]
    for k in ("company_name", "product_name", "research_date"):
        need(meta, k, "meta")
    research = parse_date(meta.get("research_date"))
    if meta.get("research_date") and research is None:
        err("meta.research_date must be YYYY-MM-DD")
    if meta.get("claim_origin") not in CLAIM_ORIGINS:
        err(f"meta.claim_origin must be one of {sorted(CLAIM_ORIGINS)}")

    diff_ids = validate_stage(data["stage"])

    tests = data["tests"]
    if not isinstance(tests, list):
        err("tests: must be an array")
        return
    seen_ids, seen_diff = set(), set()
    for i, t in enumerate(tests):
        validate_test(t, f"tests[{i}]", diff_ids, research)
        if isinstance(t, dict):
            if t.get("id") in seen_ids:
                err(f"tests[{i}]: duplicate id {t.get('id')}")
            seen_ids.add(t.get("id"))
            if t.get("kind") == "differentiator":
                if t.get("differentiator_id") in seen_diff:
                    err(f"tests[{i}]: {t.get('differentiator_id')} is tested twice")
                seen_diff.add(t.get("differentiator_id"))
    kinds = [t.get("kind") for t in tests if isinstance(t, dict)]
    for k in KINDS_REQUIRED:
        n = kinds.count(k)
        if n != 1:
            err(f"tests: need exactly one '{k}' test, found {n}")

    if not isinstance(data.get("open_questions", []), list):
        err("open_questions: must be an array of strings")

    scan_style(data)


def sort_evidence(data):
    for t in data.get("tests", []):
        ev = t.get("evidence")
        if isinstance(ev, list):
            ev.sort(key=lambda e: (parse_date(e.get("date")) is None,
                                   -(parse_date(e.get("date")) or date.min).toordinal()))


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    try:
        with open(src, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read {src}: {e}")
        return 1

    validate(data)
    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"\n{len(errors)} error(s). No file written.")
        return 1

    sort_evidence(data)
    tpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets",
                            "viewer-template.html")
    with open(tpl_path, encoding="utf-8") as fh:
        tpl = fh.read()
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/").replace("<!--", "\\u003c!--")
    title = escape(f"{data['meta']['company_name']}: Randi Does Market Research")
    out = tpl.replace("__RR_TITLE__", title).replace("__RR_DATA__", payload)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    tally = {v: 0 for v in VERDICTS}
    for t in data["tests"]:
        tally[t["verdict"]] += 1
    n_ev = sum(len(t.get("evidence", [])) for t in data["tests"])
    print(f"OK: wrote {dst} ({len(out) // 1024} KB). {len(data['tests'])} tests "
          f"({tally['validated']} validated, {tally['plausible unconfirmed']} plausible unconfirmed, "
          f"{tally['invalidated']} invalidated), {n_ev} sources. {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
