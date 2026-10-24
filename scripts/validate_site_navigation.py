#!/usr/bin/env python3
"""Validate A7 navigation normalization, history preservation, source separation."""
from pathlib import Path
import json,re,hashlib,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
htmls=sorted((R/"site").glob("*.html"))
assert len(htmls)==13, [x.name for x in htmls]
primary=["index.html","history.html","control-towers.html","repository-status.html","memory-wall.html","roadmap.html"]
archived=["legacy-overview.html","milestone.html","visualization-workspace.html"]
shell=(R/"site/assets/a7-site-shell.js").read_text()
style=(R/"site/assets/a7-site-shell.css").read_text()
assert all(x in shell for x in primary), "Primary pages missing in shared nav"
assert 'history.html' in shell and "Governance" in shell
assert 'legacy-overview.html' in shell and 'milestone.html' in shell and 'visualization-workspace.html' in shell
assert "rocket.animate" in (R/"site/assets/fluffy-rocket.js").read_text()
assert "a7-shell-ready" in style and "a7-shell-header" in style and "a7-shell-footer" in style
assert "body.a7-shell-ready>.topbar:has(#searchButton)" in style, "Legacy search must remain reachable"
assert "pointer-events:none" in (R/"site/assets/a7-unified-theme.css").read_text()
for h in htmls:
 txt=h.read_text()
 assert txt.count('assets/a7-site-shell.css')==1,h.name
 assert txt.count('assets/a7-site-shell.js')==1,h.name
 assert txt.count('assets/a7-unified-theme.css')==1,h.name
 assert txt.count('assets/fluffy-rocket.js')==1,h.name
 assert txt.index('assets/a7-site-shell.css')<txt.index("</head>"),h.name
 assert txt.index('assets/a7-site-shell.js')<txt.index("</head>"),h.name
 assert txt.index('assets/a7-site-shell.css')>txt.index('assets/a7-unified-theme.css'),h.name
assert all(x not in shell.split("const primary=routes.slice(0,6);")[0].split('["index.html"')[0] for x in ["secret","private_drive"])
home=(R/"site/index.html").read_text()
history=(R/"site/history.html").read_text()
memory=(R/"site/memory-wall.html").read_text()
assert 'href="legacy-overview.html"' not in home
assert 'href="visualization-workspace.html"' not in home
assert 'href="milestone.html"' not in home
assert 'href="history.html"' in home
assert 'href="developer-dock.html"' in home
assert 'id="platform-role-board"' in memory
assert '["developer-dock.html","Developer Dock"' in shell
assert 'class="dh-home-jump"' in home
assert '["history.html","Development History"' in shell
assert all('href="'+n+'"' in history for n in archived)
assert 'id="visualization-reminders"' in memory
assert 'memory-visualization.js' in memory
viz=(R/"site/assets/memory-visualization.js").read_text()
assert 'data/visualization-workspace.json' in viz
assert "lane.implementation_state_at_record" in viz
assert 'visualization-workspace.js' in (R/"site/visualization-workspace.html").read_text()
assert 'id="searchButton"' in (R/"site/legacy-overview.html").read_text()
assert '<canvas id="graphCanvas">' in (R/"site/legacy-overview.html").read_text()
assert 'class="galaxy-experience"' in home
assert 'id="spaceField"' in home
assert 'href="history.html"' in home
assert "GitHub remains the source of truth" in history
assert '["resource-navigator.html","Resource Navigator"' in shell
assert (R/"site/resource-navigator.html").is_file()
assert "49c99f7010e53a66fab94cad4a955e195f9b060d" in (R/"site/milestone.html").read_text()
p=(R/"registry/decisions/site-navigation-consolidation.v0.1.json")
d=json.loads(p.read_text())
assert d["status"]=="PRESENTATION_ONLY_NAVIGATION_CHANGE"
assert d["primary_pages"]==primary
assert d["archived_pages"]==archived
assert d["private_a9_reconciliation_complete"] is False
print("A7 SITE NAVIGATION PASS pages=13 main=6 archived=3 memory_views=6 history=preserved")
