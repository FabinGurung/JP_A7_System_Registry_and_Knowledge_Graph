-- A7 relational contract v1.0.0
-- FORMAL MODEL ONLY. A live PostgreSQL/Neon runtime is intentionally deferred.
-- Canonical writable records remain JSON + JSONL unless a later A7 decision explicitly changes authority.

CREATE TABLE a7_systems (
    entity_id TEXT PRIMARY KEY,
    namespace TEXT NOT NULL UNIQUE,
    canonical_label TEXT NOT NULL,
    status TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE a7_repositories (
    repository_id TEXT PRIMARY KEY,
    provider TEXT NOT NULL DEFAULT 'github',
    provider_object_id TEXT NOT NULL,
    repository_full_name TEXT NOT NULL,
    current_slug TEXT NOT NULL,
    default_branch TEXT NOT NULL,
    visibility TEXT NOT NULL CHECK (visibility IN ('public','private','internal')),
    system_role TEXT NOT NULL,
    UNIQUE (provider, provider_object_id)
);

CREATE TABLE a7_projects (
    project_id TEXT PRIMARY KEY,
    canonical_label TEXT NOT NULL,
    status TEXT NOT NULL,
    company_entity_id TEXT
);

CREATE TABLE a7_entities (
    entity_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    canonical_label TEXT NOT NULL,
    status TEXT NOT NULL
);

CREATE TABLE a7_aliases (
    alias_id TEXT PRIMARY KEY,
    target_entity_id TEXT NOT NULL,
    alias TEXT NOT NULL,
    alias_type TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    observed_at TIMESTAMPTZ,
    UNIQUE (target_entity_id, alias, alias_type)
);

CREATE TABLE a7_source_references (
    source_ref_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    provider_object_id TEXT NOT NULL,
    source_url TEXT,
    revision TEXT,
    access_class TEXT NOT NULL CHECK (access_class IN ('PUBLIC','INTERNAL','RESTRICTED','UNKNOWN')),
    observed_at TIMESTAMPTZ NOT NULL,
    UNIQUE (provider, provider_object_id, entity_id)
);

CREATE TABLE a7_edges (
    edge_id TEXT PRIMARY KEY,
    from_entity_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    to_entity_id TEXT NOT NULL,
    direction TEXT NOT NULL CHECK (direction IN ('DIRECTED','UNDIRECTED')),
    status TEXT NOT NULL,
    observed_at TIMESTAMPTZ,
    UNIQUE (from_entity_id, relation_type, to_entity_id)
);

CREATE TABLE a7_authority_assignments (
    fact_class TEXT PRIMARY KEY,
    authority_system_id TEXT,
    writable_store TEXT NOT NULL,
    rule TEXT NOT NULL
);

CREATE TABLE a7_mutation_events (
    event_id TEXT PRIMARY KEY,
    sequence_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    status TEXT NOT NULL,
    occurred_at TIMESTAMPTZ NOT NULL,
    pre_commit_sha TEXT,
    post_commit_sha TEXT,
    working_branch TEXT,
    note TEXT
);

-- Referential rules are represented here as the intended relational contract.
-- Cross-file validation in the current file-based runtime is enforced by CI scripts.
ALTER TABLE a7_aliases
    ADD CONSTRAINT fk_alias_target
    FOREIGN KEY (target_entity_id) REFERENCES a7_entities(entity_id);

ALTER TABLE a7_source_references
    ADD CONSTRAINT fk_source_entity
    FOREIGN KEY (entity_id) REFERENCES a7_entities(entity_id);

ALTER TABLE a7_edges
    ADD CONSTRAINT fk_edge_from
    FOREIGN KEY (from_entity_id) REFERENCES a7_entities(entity_id);

ALTER TABLE a7_edges
    ADD CONSTRAINT fk_edge_to
    FOREIGN KEY (to_entity_id) REFERENCES a7_entities(entity_id);
