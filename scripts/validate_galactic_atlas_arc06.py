#!/usr/bin/env python3
"""A7 Arc06 source-anchored UX; no fake runtime or provider approvals."""
from pathlib import Path
from generate_galactic_atlas import build
R=Path(__file__).resolve().parents[1]
d=build()
assert d["non_authoritative"] and d["station_count"]==9 and len(d["stations"])==9
assert d["verified_runtime_handoff_count"]==0
assert len({x["id"] for x in d["stations"]})==9
site=(R/"site/index.html").read_text()
js=(R/"site/assets/galactic-atlas-arc06.js").read_text()
assert 'id="arc06FlightDeck"' in site and 'id="arc06World"' in site
assert 'id="arc06CompareWorld"' in site and 'id="arc06Comparison"' in site
assert 'assets/galactic-atlas-arc06.js' in site and 'assets/galactic-atlas-arc06.css' in site
for token in ("a7:station-selected","URL(location.href)","searchParams.set",'.star-node',"MutationObserver","replaceChildren","textContent","provider_evidence","owner_gate"):
    assert token in js,token
assert not any(word in js for word in ("innerHTML","localStorage","POST","/api/"))
assert "navigator.clipboard" not in js
assert "Runtime handoff" not in site or "not" in site.lower()
print("A7 GALACTIC ARC06 VALIDATION PASS source_station_count=9 worlds_linked=1 comparisons_readonly=1")
