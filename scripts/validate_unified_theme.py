#!/usr/bin/env python3
"""A7 Cloud Orbit acceptance: site-only theme, mascot and source engine integrity."""
import hashlib,json,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/"registry/decisions/cloud-orbit-theme.v0.1.json").read_text())
assert d["id"]=="A7-THEME-CLOUD-ORBIT-001"
assert d["status"]=="ADOPTED_SITE_PRESENTATION_ONLY"
assert d["scope"].startswith("A7 GitHub Pages")
assert len(d["pages"])==10
all_html={p.name for p in (ROOT/"site").glob("*.html")}
assert set(d["pages"]).issubset(all_html),(sorted(all_html),d["pages"])
assert all_html-set(d["pages"])=={"history.html"},sorted(all_html-set(d["pages"]))
for name in sorted(all_html):
    c=(ROOT/"site"/name).read_text(encoding="utf-8")
    assert c.count('assets/a7-unified-theme.css')==1,name
    assert c.count('assets/fluffy-rocket.js')==1,name
    assert c.index('assets/a7-unified-theme.css')<c.index('</head>'),name
    assert c.index('assets/fluffy-rocket.js')<c.index('</body>'),name
    css_links=[c.index(x) for x in ['assets/a7-unified-theme.css']]
    assert c.rfind('<link ',0,c.index('</head>')) < c.index('assets/a7-unified-theme.css'),name
    assert '<meta name="viewport"' in c,name
css=(ROOT/d["css"]).read_text(encoding="utf-8")
for required in ("color-scheme:light","body.galactic-arc","body.standalone-page",".space-field",".galaxy-inspector",".reveal-panel",".a7-rocket-mascot","@media print","prefers-reduced-motion"):
    assert required in css,required
for token in d["tokens"].values():assert token in css,token
svg=ROOT/d["mascot"]["svg"]
ET.parse(svg)
js=(ROOT/d["mascot"]["controller"]).read_text(encoding="utf-8")
for word in ("document.createElement","prefers-reduced-motion","visibilitychange","pagehide","rocket.animate","random(17000,32000)","points.length-1","saveData"):
    assert word in js,word
assert "pointer-events:none" in css
assert 'aria-hidden","true"' in js
assert len(d["preserved_engine_git_blobs"])==6
for path,expected in d["preserved_engine_git_blobs"].items():
    b=(ROOT/path).read_bytes()
    sha=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    assert sha==expected,(path,sha,expected)
for rel in ["site/data","site/.nojekyll"]:
    pass
assert "Validate unified site theme" in (ROOT/".github/workflows/validate-registry.yml").read_text()
assert "site/**" in (ROOT/".github/workflows/deploy-a7-pages.yml").read_text()
print("A7 CLOUD ORBIT PASS original_pages=10 current_pages=11 preserved_engines=6 mascot=accessible source=unchanged")
