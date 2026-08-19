## REMOVED Requirements

### Requirement: Thirty operator skills cloned from CyberStrike

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Folder slug equals frontmatter name

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Frontmatter reduced to the opencode contract

**Reason**: Replaced by one frontmatter contract covering both pillars, stated against the harnesses that remain.

**Migration**: Read `skill-library`'s frontmatter requirement; the field limits (`name` 1-64, `description` 1-1024, optional `metadata`) are unchanged.

### Requirement: Provenance recorded in metadata

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Triggering-quality descriptions

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Bodies carry no tool the harness lacks

**Reason**: Subsumed by `skill-library`, with the substitution rule inlined because the `harness-tool-translation` capability it referenced is deleted.

**Migration**: Read `skill-library`'s no-unavailable-tool requirement: a former `attack_script` step is a standard tool invocation or an explicit inline command.

### Requirement: Bodies otherwise preserve upstream methodology

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.

### Requirement: Corpus skills are not published

**Reason**: Subsumed by the new `skill-library` capability, which specifies both pillars' libraries in one place.

**Migration**: Read the equivalent requirement in `skill-library`; the behaviour it protects is unchanged.
