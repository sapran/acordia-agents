## REMOVED Requirements

### Requirement: One skill per competency-grid row

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: opencode-native location, plain slugs

**Reason**: Replaced. The install location is no longer an opencode path: a skill lives in its pillar's authored tree and is installed by the harness's own plugin system.

**Migration**: `skill-library`'s location requirement states the pillar-relative path and keeps the slug-equals-name rule unchanged.

### Requirement: opencode frontmatter contract

**Reason**: Replaced by one frontmatter contract covering both pillars, stated against the harnesses that remain.

**Migration**: Read `skill-library`'s frontmatter requirement; the field limits (`name` 1-64, `description` 1-1024, optional `metadata`) are unchanged.

### Requirement: Triggering-quality descriptions

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Cross-cutting deep skills are ordinary skills

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Credential-extraction sections in credential-adjacent skills

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: `credential-harvest-triage` skill exists

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: `analyst-loop` skill exists

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Method contract for evidence-reading skills

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Procedural skills MAY co-locate reference files

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: `exhaustive-data-processing` skill exists

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: `aleph-entity-graph` skill exists

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.
