from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass(frozen=True)
class Rule:
    id: str
    pattern: str
    message: str
    severity: str = "warn"   
    scope: str = "text"      

def load_rules(path: Path) -> list[Rule]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    rules: list[Rule] = []
    for r in data.get("rules", []):
        rules.append(Rule(
            id=r.get("id", "rule"),
            pattern=r["pattern"],
            message=r.get("message", ""),
            severity=r.get("severity", "warn"),
            scope=r.get("scope", "text"),
        ))
    return rules


def apply_text_rules(text: str, rules: list[Rule]) -> list[dict]:
    issues: list[dict] = []
    for rule in rules:
        if rule.scope != "text":
            continue
        rx = re.compile(rule.pattern, re.IGNORECASE | re.UNICODE)
        for m in rx.finditer(text):
            issues.append({
                "start": m.start(),
                "end": m.end(),
                "word": text[m.start():m.end()],
                "type": "rule",
                "severity": rule.severity,
                "message": rule.message,
                "rule_id": rule.id,
                "suggestions": []
            })
    return issues

    

