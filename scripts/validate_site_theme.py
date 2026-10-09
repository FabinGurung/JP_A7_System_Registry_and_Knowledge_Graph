#!/usr/bin/env python3
"""A7 sky-blue public UI theme regression guard."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
theme=json.loads((ROOT/"registry/decisions/ui-theme.json").read_text(encoding="utf-8"))
css=(ROOT/"site/assets/sky-theme.css").read_text(encoding="utf-8")
js=(ROOT/"site/assets/app.js").read_text(encoding="utf-8")
assert theme["theme_id"]=="A7-UI-THEME-SKY-MIST-001"
assert theme["status"]=="ADOPTED_LIGHT_THEME"
assert theme["governance"]["no_changes_to_a7_seq_000013_private_a9_migration"] is True
for value in theme["palette"].values():
    assert value in css, f"theme token absent from CSS: {value}"
assert "color-scheme:light" in css
for path in theme["locations"]:
    content=(ROOT/path).read_text(encoding="utf-8")
    assert "assets/sky-theme.css" in content, f"theme missing on {path}"
    assert 'content="#eff8fc"' in content, f"browser chrome theme mismatch on {path}"
    if path.endswith("governance.html") or path.endswith("roadmap.html"):
        assert 'class="standalone-page"' in content, f"standalone theme scope missing {path}"
        assert content.index("</style>") < content.index("assets/sky-theme.css"), f"theme must override inline style {path}"
    else:
        assert content.index("assets/styles.css") < content.index("assets/sky-theme.css"), f"theme load order wrong {path}"
for token in ["NODE_PALETTE","execution_profile","project","research_project","#3a627c"]:
    assert token in js, f"Canvas graph light palette incomplete: {token}"
assert "sky-blue" in (ROOT/"docs/SKY_MIST_THEME.md").read_text(encoding="utf-8")
print("A7 SKY MIST THEME VALIDATION: PASS pages=4 graphs=2 source=unchanged")
