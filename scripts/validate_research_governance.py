#!/usr/bin/env python3
"""Validate public research routes without inventing scientific state."""
import json
from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((root/p).read_text())
repos=load('registry/entities/repositories.json')['repositories']
research=next(r for r in repos if r['provider_object_id']=='1312113873')
assert research['repository_id']=='REPO-000006'
projects=load('registry/entities/projects.json')['projects']
slugs=set()
for project in projects:
    assert project['research_repository_id']==research['repository_id']
    assert project['scientific_state']=='NOT_ASSERTED'
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+){2,}',project['slug'])
    assert project['slug'] not in slugs
    slugs.add(project['slug'])
    assert project['public_research_route']==f"https://fabingurung.github.io/JP_Research-and-Development/projects/{project['slug']}/"
    assert len(project['canonical_label'].split())>=3
dependency=load('registry/dependencies/research-governance.json')
assert dependency['a9']['provider_id'] is None and dependency['a9']['status']=='OPTIONAL_NOT_PROVISIONED'
assert dependency['adopted_governance_location']['repository_id']=='1312113873'
assert dependency['scientific_authority']=='GOOGLE_DRIVE'
assert dependency['saugat_thesis_execution']=='EXCLUDED_SEPARATE_CHAT'
assert dependency['mass_migration']=='NOT_AUTHORIZED'
edges=[json.loads(row) for row in (root/'registry/edges/edges.jsonl').read_text().splitlines()]
for project in projects:
    assert any(e['from_entity_id']==research['repository_id'] and e['to_entity_id']==project['project_id'] and e['relation_type']=='PRESENTS_RESEARCH_METADATA' for e in edges)
print(f'A7 research identity/routing and unprovisioned A9 boundary: PASS ({len(projects)} projects)')
