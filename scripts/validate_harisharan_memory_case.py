#!/usr/bin/env python3
"""Validates that the A7 reference never impersonates CAD engineering authority."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'registry/curations/harisharan-cad-evidence-mnemonic.v0.1.json'
q=root/'site/data/harisharan-cad-evidence-mnemonic.json'
src=json.loads(p.read_text(encoding='utf8'))
dst=json.loads(q.read_text(encoding='utf8'))
assert src==dst,'A7 Memory Wall derived evidence does not match canonical source'
assert src['id']=='A7-MEM-CAD-HAR-20261110-001'
assert src['revision']=='R000001'
assert src['ownership']=='A7_PUBLIC_CROSS_REFERENCE_ONLY'
assert src['constructionApproval'] is False
assert src['sourceApproval'] is False
assert all(x['status']!='APPROVED' for x in src['reminders'])
assert len(src['reminders'])==3
assert all(x['url'].startswith('https://') for x in src['sourceLinks'])
assert 'drive.google.com' not in p.read_text()
html=(root/'site/memory-wall.html').read_text()
assert 'id="harisharan-cad-source-memory"' in html
assert 'assets/harisharan-cad-case.js' in html
js=(root/'site/assets/harisharan-cad-case.js').read_text()
assert 'harisharan-cad-evidence-mnemonic.json' in js
assert 'NOT FOR CONSTRUCTION' in html
print('A7_HARISHARAN_PUBLIC_SAFE_MEMORY_PASS source=canonical curation, approval=false')
