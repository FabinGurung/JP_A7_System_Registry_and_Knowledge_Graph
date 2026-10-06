-- A7 relational contract v2.0.0
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

CREATE TABLE a7_fact_classes (
    fact_class_id TEXT PRIMARY KEY,
    fact_class TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    default_materiality TEXT NOT NULL CHECK (default_materiality IN ('LOW','MATERIAL','SAFETY_CRITICAL')),
    timestamp_strategy TEXT NOT NULL,
    requires_explicit_authority BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE a7_authority_assignments (
    authority_id TEXT PRIMARY KEY,
    fact_class TEXT NOT NULL,
    scope_type TEXT NOT NULL,
    scope_id TEXT NOT NULL,
    owner_kind TEXT NOT NULL,
    owner_ref TEXT NOT NULL,
    writable_store TEXT NOT NULL,
    source_role TEXT NOT NULL,
    resolution_strategy TEXT NOT NULL,
    timestamp_strategy TEXT NOT NULL,
    materiality TEXT NOT NULL CHECK (materiality IN ('LOW','MATERIAL','SAFETY_CRITICAL')),
    rule TEXT NOT NULL,
    UNIQUE (fact_class, scope_type, scope_id)
);

CREATE TABLE a7_claims (
    claim_id TEXT PRIMARY KEY,
    entity_id TEXT,
    fact_class TEXT NOT NULL,
    claim_role TEXT NOT NULL CHECK (claim_role IN ('DECLARED_AUTHORITY','VERIFIED_HUMAN_QA_RESOLUTION','EVIDENCE','PROJECTION','UNKNOWN')),
    source_ref_id TEXT,
    provider TEXT,
    value_json JSONB NOT NULL,
    observed_at TIMESTAMPTZ,
    effective_at TIMESTAMPTZ,
    authority_id TEXT
);

CREATE TABLE a7_conflicts (
    conflict_id TEXT PRIMARY KEY,
    entity_id TEXT,
    fact_class TEXT NOT NULL,
    conflict_type TEXT NOT NULL,
    materiality TEXT NOT NULL,
    status TEXT NOT NULL,
    opened_at TIMESTAMPTZ NOT NULL,
    resolution_outcome TEXT,
    notes TEXT
);

CREATE TABLE a7_qa_cases (
    qa_case_id TEXT PRIMARY KEY,
    entity_id TEXT,
    project_id TEXT,
    fact_class TEXT NOT NULL,
    conflict_type TEXT NOT NULL,
    status TEXT NOT NULL,
    question TEXT NOT NULL,
    conversation_or_evidence_url TEXT,
    opened_at TIMESTAMPTZ NOT NULL,
    resolved_at TIMESTAMPTZ,
    resolution_source_ref_id TEXT,
    resolution_json JSONB
);

CREATE TABLE a7_provider_policies (
    provider TEXT PRIMARY KEY,
    policy_id TEXT NOT NULL UNIQUE,
    version TEXT NOT NULL,
    default_claim_role TEXT NOT NULL,
    public_projection_default TEXT NOT NULL,
    policy_json JSONB NOT NULL
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

ALTER TABLE a7_authority_assignments
    ADD CONSTRAINT fk_authority_fact_class
    FOREIGN KEY (fact_class) REFERENCES a7_fact_classes(fact_class);

ALTER TABLE a7_claims
    ADD CONSTRAINT fk_claim_fact_class
    FOREIGN KEY (fact_class) REFERENCES a7_fact_classes(fact_class);

ALTER TABLE a7_claims
    ADD CONSTRAINT fk_claim_source_ref
    FOREIGN KEY (source_ref_id) REFERENCES a7_source_references(source_ref_id);

ALTER TABLE a7_qa_cases
    ADD CONSTRAINT fk_qa_resolution_source_ref
    FOREIGN KEY (resolution_source_ref_id) REFERENCES a7_source_references(source_ref_id);
