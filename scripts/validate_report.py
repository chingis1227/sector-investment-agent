#!/usr/bin/env python3
"""Config-driven gatekeeper validator for Sector Investment Agent reports.

Usage:
  py -3 scripts/validate_report.py outputs/sector/report.md
  py -3 scripts/validate_report.py --mode standard outputs/sector/report.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "configs" / "report_contract.yaml"


def load_contract(path: Path = CONTRACT_PATH) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"contract not found: {path}")
    # The file is YAML-compatible JSON to avoid a runtime PyYAML dependency.
    return json.loads(path.read_text(encoding="utf-8-sig"))


def count_sentences(text: str) -> int:
    cleaned = re.sub(r"\s+", " ", text.strip())
    parts = re.findall(r"[^.!?]+[.!?]", cleaned)
    return len([p for p in parts if p.strip()])


def title_to_pattern(title: str) -> str:
    escaped = re.escape(title)
    escaped = escaped.replace(re.escape("–"), r"[–-]")
    escaped = escaped.replace(re.escape("/"), r"\s*/\s*")
    escaped = escaped.replace(r"\ ", r"\s+")
    return escaped


def heading_pattern_for_titles(titles: list[str]) -> str:
    alternatives = "|".join(title_to_pattern(t) for t in titles)
    return rf"^#{{1,3}}\s*(?:\d+\.\s*)?(?:{alternatives})\s*$"


def has_heading(text: str, title: str) -> bool:
    return bool(re.search(heading_pattern_for_titles([title]), text, re.I | re.M))


def section_after_titles(text: str, titles: list[str]) -> str:
    pattern = heading_pattern_for_titles(titles)
    m = re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    if not m:
        return ""
    start = m.end()
    nxt = re.search(r"^#{1,3}\s+", text[start:], flags=re.MULTILINE)
    end = start + nxt.start() if nxt else len(text)
    return text[start:end].strip()


def table_headers(text: str) -> list[str]:
    headers: list[str] = []
    lines = text.splitlines()
    for i, line in enumerate(lines[:-1]):
        stripped = line.strip()
        next_line = lines[i + 1].strip()
        if stripped.startswith("|") and stripped.endswith("|") and next_line.startswith("|") and "---" in next_line:
            headers.append(stripped)
    return headers


def table_header_contains(text: str, required_terms: list[str]) -> bool:
    headers = table_headers(text)
    for header in headers:
        lower = header.lower()
        if all(term.lower() in lower for term in required_terms):
            return True
    return False


def count_table_rows(section: str) -> int:
    rows = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|") and "---" not in stripped:
            rows.append(stripped)
    return max(0, len(rows) - 1)


def independent_source_count(sources_section: str) -> int:
    names: set[str] = set()
    for line in sources_section.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or "---" in stripped:
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0].lower()
        if first in {"source", "sources"} or "источник" in first:
            continue
        if cells[0] and not re.search(r"\[[^\]]+\]|<[^>]+>|TBD|TODO", cells[0], re.I):
            names.add(cells[0].lower())
    urls = set(re.findall(r"https?://([^/\s)]+)", sources_section, flags=re.I))
    return max(len(names), len(urls))


def contains_all_term_groups(text: str, groups: list[list[str]]) -> bool:
    lower = text.lower()
    return all(any(term.lower() in lower for term in group) for group in groups)


def contains_all_terms(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return all(term.lower() in lower for term in terms)


def contains_any(text: str, terms: list[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def final_conclusion_body(section: str) -> str:
    m = re.search(r"(?:^|\n)\s*(?:Вывод|Conclusion)\s*:\s*(.*)$", section, flags=re.I | re.S)
    if m:
        return m.group(1).strip()
    skip_prefixes = (
        "facts:",
        "fact:",
        "interpretations:",
        "interpretation:",
        "assumptions:",
        "assumption:",
        "confidence level:",
    )
    cleaned_lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip().lstrip("-* ").strip()
        low = stripped.lower()
        if any(low.startswith(prefix) for prefix in skip_prefixes):
            continue
        if any(low.startswith(prefix.lower()) for prefix in ["Факты:", "Факт:", "Интерпретации:", "Интерпретация:", "Допущения:", "Допущение:", "Уровень уверенности:", "Confidence level:"]):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines).strip()


def is_scenario_doc(text: str, contract: dict[str, Any]) -> bool:
    markers = contract.get("scenario_markers", [])
    return sum(1 for marker in markers if marker.lower() in text.lower()) >= 2


def has_placeholders(text: str, contract: dict[str, Any]) -> bool:
    text_without_comments = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for pattern in contract.get("placeholder_patterns", []):
        if re.search(pattern, text_without_comments, re.I):
            return True
    return False


def has_confidence_level(text: str, contract: dict[str, Any]) -> bool:
    keywords = contract["confidence"]["keywords"]
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        if any(keyword.lower() in stripped.lower() for keyword in keywords):
            return True
    return False


def confidence_is_high(text: str, contract: dict[str, Any]) -> bool:
    keywords = contract["confidence"]["keywords"]
    high_values = contract["confidence"]["high_values"]
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        lower = stripped.lower()
        if any(keyword.lower() in lower for keyword in keywords) and any(value.lower() in lower for value in high_values):
            return True
    return False


def add_check(checks: list[tuple[str, bool, str]], name: str, ok: bool, fix: str) -> None:
    checks.append((name, ok, fix))


def validate(text: str, mode: str, contract: dict[str, Any]) -> tuple[int, int, list[tuple[str, bool, str]]]:
    mode_contract = contract["modes"][mode]
    checks: list[tuple[str, bool, str]] = []

    missing_sections = [title for title in mode_contract["required_sections"] if not has_heading(text, title)]
    add_check(
        checks,
        f"has required sections for mode={mode}",
        not missing_sections,
        "Missing sections: " + ", ".join(missing_sections) if missing_sections else "",
    )

    if mode == "deep":
        add_check(
            checks,
            "deep mode has all 18 required sections",
            len(mode_contract["required_sections"]) == 18 and not missing_sections,
            "Deep mode must include all 18 sections from the report contract.",
        )

    add_check(checks, "has no template placeholders", not has_placeholders(text, contract), "Replace template placeholders/TBD/TODO text with report-specific content.")
    add_check(checks, "has scope fields", contains_all_term_groups(text, contract["scope_terms"]), "Add date, sector, object type, geography, and horizon/scope.")
    add_check(checks, "has confidence level", has_confidence_level(text, contract), "Add confidence level and reason.")

    evidence = section_after_titles(text, ["Evidence table", "Размер рынка и рост", "Market size and growth"])
    if mode_contract.get("require_evidence_table"):
        add_check(
            checks,
            "has evidence table with required schema",
            table_header_contains(text, contract["evidence_schema"]["required_fields"]),
            "Add evidence table with metric, Tier, value, observation period, publication/access dates, source, freshness, and reliability.",
        )
        add_check(
            checks,
            "evidence table has at least one data row",
            count_table_rows(evidence) >= 1,
            "Add at least one report-specific evidence row.",
        )

    sources = section_after_titles(text, ["Источники и надежность данных", "Sources and data reliability", "Sources"])
    if mode_contract.get("require_source_table"):
        add_check(
            checks,
            "has source table with required schema",
            table_header_contains(text, contract["source_schema"]["required_fields"]),
            "Add source table with support, observation period, publication date, access date, freshness, reliability, and limitation.",
        )
        add_check(
            checks,
            "source table has at least one source row",
            count_table_rows(sources) >= 1,
            "Add at least one concrete source row in the sources section.",
        )

    source_count = independent_source_count(sources)
    market_titles = ["Размер рынка и рост", "Market size and growth", "Evidence table"]
    market = section_after_titles(text, market_titles)
    market_claim = contains_any(market, contract["market_size_terms"]) and any(ch.isdigit() for ch in market) and contains_any(market, ["%", "CAGR", "bn", "billion", "млрд", "трлн"])
    hedged_or_limited = contains_any(market + "\n" + sources, ["single source", "один источник", "low confidence", "низкая уверенность", "гипотез"])
    add_check(
        checks,
        "market size/growth has >=2 sources or is explicitly limited",
        (not market_claim) or source_count >= 2 or hedged_or_limited,
        f"Found {source_count} independent source(s). Add a second source or mark market size/growth as limited/hypothesis.",
    )

    if mode_contract.get("require_tiered_metrics"):
        add_check(checks, "has Tier 1/2/3 metrics", contains_all_terms(text, contract["tier_terms"]), "Add Tier 1, Tier 2, and Tier 3 metrics.")

    if mode_contract.get("require_fact_interpretation_assumption"):
        add_check(
            checks,
            "has Fact / Interpretation / Assumption split",
            contains_all_terms(text, contract["claim_type_terms"][:3]) or contains_all_terms(text, ["Факт", "Интерпретация", "Допущение"]),
            "Separate important claims into Fact, Interpretation, and Assumption.",
        )

    if mode_contract.get("require_anti_thesis"):
        anti = section_after_titles(text, ["Анти-тезис", "Anti-thesis и риски", "Риски и anti-thesis"])
        add_check(checks, "has substantive anti-thesis/risk section", bool(anti and len(re.sub(r"\s+", "", anti)) >= 80), "Add a substantive anti-thesis that attacks the main thesis.")
        add_check(checks, "states what breaks the thesis", contains_any(text, contract["anti_thesis_terms"]), "State what breaks the thesis/conclusion.")

    if mode_contract.get("require_monitoring_metrics_3_to_5"):
        metrics = section_after_titles(text, ["Метрики мониторинга", "Monitoring metrics"])
        metric_rows = count_table_rows(metrics)
        bullet_count = len(re.findall(r"^\s*[-*]\s+", metrics, re.M))
        add_check(checks, "has 3-5 monitoring metrics", 3 <= max(metric_rows, bullet_count) <= 5, "Add exactly 3-5 monitoring metrics.")

    final_titles = ["Итоговый инвестиционный вывод", "Final investment conclusion", "Вердикт", "Next steps, sources and confidence"]
    final = section_after_titles(text, final_titles)
    sentence_rule = mode_contract.get("final_conclusion_sentences", {})
    if final:
        n = count_sentences(final_conclusion_body(final))
        if "exact" in sentence_rule:
            ok = n == int(sentence_rule["exact"])
            fix = f"Found {n}; make it exactly {sentence_rule['exact']} sentences."
        else:
            min_n = int(sentence_rule.get("min", 1))
            max_n = int(sentence_rule.get("max", 999))
            ok = min_n <= n <= max_n
            fix = f"Found {n}; expected {min_n}-{max_n} sentences."
        add_check(checks, "final conclusion sentence count matches mode", ok, fix)
    else:
        add_check(checks, "has final conclusion/verdict content", False, "Add final conclusion/verdict section.")

    high_confidence = confidence_is_high(text, contract)
    stale_or_unknown = contains_any(text, contract["confidence"]["stale_markers"])
    add_check(
        checks,
        "high confidence is not used with stale/unknown/limited data",
        not (high_confidence and stale_or_unknown),
        "Lower confidence when sources are stale, unknown, limited, or freshness is not verified.",
    )

    tier3_primary = bool(re.search(r"Tier\s*3[^\n]{0,140}(primary|main|strong|key|основ|главн|сильн)", text, re.I))
    add_check(checks, "high-confidence conclusion is not based on Tier 3", not (high_confidence and tier3_primary), "Do not base a high-confidence conclusion on Tier 3 data.")

    passed = sum(1 for _, ok, _ in checks if ok)
    return passed, len(checks), checks


def main(argv: list[str] | None = None) -> int:
    contract = load_contract()
    parser = argparse.ArgumentParser(description="Validate Sector Investment Agent markdown reports.")
    parser.add_argument("report", help="Path to report markdown file")
    parser.add_argument("--mode", choices=sorted(contract["modes"].keys()), default=None)
    args = parser.parse_args(argv)

    default_mode = contract.get("default_mode", "deep")
    if default_mode not in contract["modes"]:
        print(f"ERROR: default_mode is not configured in modes: {default_mode}")
        return 2
    mode = args.mode or default_mode

    p = Path(args.report)
    if not p.exists():
        print(f"ERROR: file not found: {p}")
        return 2
    text = p.read_text(encoding="utf-8-sig", errors="ignore")

    if is_scenario_doc(text, contract):
        print("ERROR: this looks like an eval scenario document, not a report fixture. Move it under evals/scenarios or validate an actual report.")
        return 2

    passed, total, checks = validate(text, mode, contract)
    for name, ok, fix in checks:
        status = "PASS" if ok else "FAIL"
        print(f"{status}: {name}")
        if not ok and fix:
            print(f"      Fix: {fix}")
    mode_source = "explicit --mode" if args.mode else "configs/report_contract.yaml default_mode"
    print(f"\nScore: {passed}/{total} checks passed (mode={mode}, mode_source={mode_source})")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())




