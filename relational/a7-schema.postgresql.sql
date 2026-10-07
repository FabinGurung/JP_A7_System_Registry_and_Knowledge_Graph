-- A7 relational contract v7.0.0
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


-- Phase 3 GitHub inventory contract v1.0.0
CREATE TABLE a7_github_branches (
    branch_record_id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL,
    provider_repository_id TEXT NOT NULL,
    branch_name TEXT NOT NULL,
    head_sha TEXT NOT NULL,
    is_default BOOLEAN NOT NULL,
    is_pages_production_source BOOLEAN NOT NULL,
    protected BOOLEAN NOT NULL,
    branch_class TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    UNIQUE (repository_id, branch_name)
);

CREATE TABLE a7_github_workflows (
    workflow_id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL,
    workflow_path TEXT NOT NULL,
    workflow_sha TEXT NOT NULL,
    workflow_name TEXT NOT NULL,
    workflow_role TEXT NOT NULL,
    deploy_pages_capable BOOLEAN NOT NULL,
    pages_write BOOLEAN NOT NULL,
    production_status TEXT NOT NULL,
    latest_successful_run_id BIGINT
);

CREATE TABLE a7_github_pages (
    pages_record_id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL UNIQUE,
    has_pages BOOLEAN NOT NULL,
    public_site_url TEXT,
    deployment_mode TEXT NOT NULL,
    production_trigger_branch TEXT,
    content_source_ref TEXT,
    workflow_path TEXT,
    workflow_sha TEXT,
    latest_successful_run_id BIGINT,
    latest_successful_run_sha TEXT,
    latest_successful_run_at TIMESTAMPTZ,
    owner_invariant_status TEXT NOT NULL,
    default_branch_matches_trigger BOOLEAN
);

CREATE TABLE a7_repository_role_candidates (
    role_candidate_id TEXT PRIMARY KEY,
    repository_id TEXT NOT NULL UNIQUE,
    candidate_role TEXT NOT NULL,
    confidence TEXT NOT NULL,
    binding_status TEXT NOT NULL,
    evidence_json JSONB NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL
);

ALTER TABLE a7_github_branches
    ADD CONSTRAINT fk_github_branch_repo
    FOREIGN KEY (repository_id) REFERENCES a7_repositories(repository_id);

ALTER TABLE a7_github_workflows
    ADD CONSTRAINT fk_github_workflow_repo
    FOREIGN KEY (repository_id) REFERENCES a7_repositories(repository_id);

ALTER TABLE a7_github_pages
    ADD CONSTRAINT fk_github_pages_repo
    FOREIGN KEY (repository_id) REFERENCES a7_repositories(repository_id);

ALTER TABLE a7_repository_role_candidates
    ADD CONSTRAINT fk_repo_role_candidate
    FOREIGN KEY (repository_id) REFERENCES a7_repositories(repository_id);


-- Phase 4 Google Drive topology contract v1.0.0
CREATE TABLE a7_google_drive_nodes (
    entity_id TEXT PRIMARY KEY,
    canonical_label TEXT NOT NULL,
    semantic_role TEXT NOT NULL,
    provider_object_id TEXT,
    parent_entity_id TEXT,
    access_class TEXT NOT NULL,
    public_safe_metadata BOOLEAN NOT NULL,
    public_projection BOOLEAN NOT NULL,
    status TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE a7_google_drive_anchors (
    anchor_id TEXT PRIMARY KEY,
    canonical_label TEXT NOT NULL,
    semantic_role TEXT NOT NULL,
    provider_object_id TEXT NOT NULL UNIQUE,
    access_class TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE a7_google_drive_inventory_coverage (
    inventory_id TEXT PRIMARY KEY,
    sequence_id TEXT NOT NULL,
    root_entity_id TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    mode TEXT NOT NULL,
    coverage_json JSONB NOT NULL
);


-- Phase 6 specialist module binding / ownership boundary contract v1.0.0
CREATE TABLE a7_modules (
    module_id TEXT PRIMARY KEY,
    canonical_label TEXT NOT NULL,
    module_role TEXT NOT NULL UNIQUE,
    module_class TEXT NOT NULL,
    module_group TEXT NOT NULL,
    platform_level TEXT NOT NULL CHECK (platform_level = 'PEER_SPECIALIST_MODULE'),
    repository_id TEXT NOT NULL UNIQUE,
    provider_repository_id TEXT NOT NULL,
    canonical_working_ref TEXT NOT NULL,
    observed_ref_sha TEXT NOT NULL,
    status TEXT NOT NULL,
    ownership_profile_id TEXT NOT NULL UNIQUE
);

CREATE TABLE a7_module_ownership_profiles (
    ownership_profile_id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL UNIQUE,
    owns_fact_classes_json JSONB NOT NULL,
    owns_capabilities_json JSONB NOT NULL,
    must_not_own_fact_classes_json JSONB NOT NULL,
    boundary_rule TEXT NOT NULL
);

ALTER TABLE a7_modules
    ADD CONSTRAINT fk_a7_module_repo
    FOREIGN KEY (repository_id) REFERENCES a7_repositories(repository_id);

ALTER TABLE a7_module_ownership_profiles
    ADD CONSTRAINT fk_a7_module_ownership
    FOREIGN KEY (module_id) REFERENCES a7_modules(module_id);


-- Phase 7 cross-repository module manifest contract v1.0.0
CREATE TABLE a7_module_manifest_observations (
    observation_id TEXT PRIMARY KEY,
    module_id TEXT NOT NULL UNIQUE,
    repository_id TEXT NOT NULL UNIQUE,
    provider_repository_id TEXT NOT NULL,
    default_branch TEXT NOT NULL,
    pre_sha TEXT NOT NULL,
    post_sha TEXT NOT NULL,
    manifest_path TEXT NOT NULL CHECK (manifest_path = 'A7_MODULE.json'),
    manifest_blob_sha TEXT NOT NULL,
    pull_request BIGINT NOT NULL,
    entrypoint_count INTEGER NOT NULL CHECK (entrypoint_count > 0),
    post_snapshot_branch TEXT NOT NULL,
    provider_readback TEXT NOT NULL CHECK (provider_readback = 'PASS'),
    validation_json JSONB NOT NULL
);

ALTER TABLE a7_module_manifest_observations
    ADD CONSTRAINT fk_a7_manifest_module
    FOREIGN KEY (module_id) REFERENCES a7_modules(module_id);

ALTER TABLE a7_module_manifest_observations
    ADD CONSTRAINT fk_a7_manifest_repo
    FOREIGN KEY (repository_id) REFERENCES a7_repositories(repository_id);

-- Phase 10 deterministic project-module routing contract v1.0.0
CREATE TABLE a7_project_semantic_identities (
    project_id TEXT PRIMARY KEY,
    source_repository_id TEXT NOT NULL,
    source_record_key TEXT NOT NULL UNIQUE,
    observed_source_blob_sha TEXT NOT NULL,
    observed_provider_head_sha TEXT NOT NULL
);

CREATE TABLE a7_execution_profiles (
    execution_profile_id TEXT PRIMARY KEY,
    profile_role TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL
);

CREATE TABLE a7_execution_profile_routes (
    route_id TEXT PRIMARY KEY,
    execution_profile_id TEXT NOT NULL,
    fact_class TEXT NOT NULL,
    authority_id TEXT NOT NULL,
    module_id TEXT NOT NULL,
    route_role TEXT NOT NULL,
    project_instance_assertion TEXT NOT NULL CHECK (project_instance_assertion = 'NOT_ASSERTED_BY_A7'),
    UNIQUE (execution_profile_id, fact_class),
    FOREIGN KEY (execution_profile_id) REFERENCES a7_execution_profiles(execution_profile_id),
    FOREIGN KEY (module_id) REFERENCES a7_modules(module_id)
);

CREATE TABLE a7_project_execution_bindings (
    project_id TEXT PRIMARY KEY,
    execution_profile_id TEXT NOT NULL,
    binding_status TEXT NOT NULL CHECK (binding_status = 'ACTIVE_ROUTING'),
    project_specific_module_instances TEXT NOT NULL CHECK (project_specific_module_instances = 'NOT_ASSERTED_BY_A7'),
    FOREIGN KEY (project_id) REFERENCES a7_project_semantic_identities(project_id),
    FOREIGN KEY (execution_profile_id) REFERENCES a7_execution_profiles(execution_profile_id)
);
