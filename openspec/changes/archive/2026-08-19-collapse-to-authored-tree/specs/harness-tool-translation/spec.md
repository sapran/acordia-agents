## REMOVED Requirements

### Requirement: No shipped artifact names a tool the harness lacks

**Reason**: The capability is deleted because nothing translates any more, but the invariant is kept.

**Migration**: `agent-roster` carries it for prompts and `skill-library` for skill bodies.

### Requirement: The `.acordia/ops/` operation journal

**Reason**: Moved. The journal is a prompt-level contract, not a translation rule.

**Migration**: `agent-roster` requires the journal-discipline section in every operator prompt; `docs/agents-skills-extension-workbook.md` §8 keeps the layout.

### Requirement: Fixed substitution table for CyberStrike platform tools

**Reason**: The substitutions are applied and permanent; a table specifying how to apply them once has no remaining mechanism.

**Migration**: `skill-library` requires that no body names a CyberStrike platform tool, and `docs/agents-skills-extension-workbook.md` §8 keeps the table for a future port.

### Requirement: Substitution table is documented once and referenced

**Reason**: Same reason: the rule governed a translation step that no longer exists.

**Migration**: The table remains documented once in `docs/agents-skills-extension-workbook.md` §8.
