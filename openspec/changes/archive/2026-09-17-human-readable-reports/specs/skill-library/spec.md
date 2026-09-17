## ADDED Requirements

### Requirement: Reports are readable and evidence-traceable for human analysts

`briefing-reporting` SHALL state the repository's reader-facing practice for every finished written report. It SHALL require an acronym or initialism to be written as its full term followed by the shortened form on its first reader-visible authored use, including a heading, summary, caption or table cell. The explanation SHALL use the report's language, retaining an official or source-language full form where translation would obscure identity and adding a plain-language explanation. Quoted evidence, code, URLs, paths and literal identifiers remain byte-for-byte evidence; necessary terms are explained beside them. An unknown or ambiguous expansion SHALL be marked as unestablished or qualified rather than invented.

It SHALL require each finished report to retain a report-language chapter titled `Acronyms and abbreviations` (`Сокращения и аббревиатуры` in Russian), after substantive findings and hand-off and before any source annex where no specialist layout fixes another point. The chapter SHALL use `Acronym | Full form | Meaning in this report`, contain every term used as a term once per meaning including headings and tables, be alphabetised for lookup, exclude incidental uppercase machine literals, and say `None used.` when empty. A bounded status or dispatch hand-back is not a finished report and need not contain an artificial chapter, but still expands terms and references its evidence.

It SHALL prefer labelled tables for structured comparison, inventories, coverage, and acronym definitions when items share attributes, while retaining judgment, causal reasoning and requested action in prose where clearer. It SHALL not require a table for one straightforward finding or redesign a specialist layout that already requires tables.

It SHALL require an evidence-backed claim to carry a usable local reference: a source URL, a document or artefact path relative to an identified evidence root or supplied bundle plus a page, section, line or offset where available, or an issuer-qualified document, entity, case or record locator. An inline numbered citation is valid only when it resolves to a complete locator elsewhere in the same report; an unconnected bibliography is not. A paragraph or row may share a reference only where support is unambiguous. Inferences SHALL remain labelled and cite their supporting observations. A quotation is optional, and a citation does not substitute for checking the supporting passage. When the source or anchor is unavailable, the product SHALL label that limitation rather than inventing a reference or presenting the claim as verified.

The credential-sweep layout SHALL place its acronym chapter after Hand-off and before its footer, support genuine non-Aleph source anchors and escaped local source-root-relative path locators, and preserve its disclosure, full-identifier, passive-verification and no-target-contact rules. Its self-check SHALL distinguish short Aleph entity identifiers from ordinary source URLs, local locators and href-less anchors without echoing a malformed evidence URL.

#### Scenario: First use in a heading or table is expanded

- **WHEN** a finished report first uses an acronym or initialism in a heading, summary, caption or table cell
- **THEN** that authored occurrence states the full term followed by the shortened form, or marks its expansion unestablished or ambiguous, rather than deferring explanation only to the glossary

#### Scenario: A finished report has a complete glossary

- **WHEN** a finished report uses terms in prose, headings or tables
- **THEN** its dedicated report-language acronym chapter lists each used term once per meaning with its full form and a short meaning in the report language, ordered for lookup and without unused padding or machine-literal noise

#### Scenario: An acronym-free finished report keeps its chapter

- **WHEN** a finished report uses no acronyms or abbreviations as terms
- **THEN** it retains its dedicated chapter with the statement `None used.` rather than inventing an entry or omitting the chapter

#### Scenario: An expansion cannot be established

- **WHEN** evidence contains an acronym whose full form is not established or whose meaning remains ambiguous
- **THEN** the report labels that uncertainty at first use and in the glossary, qualifying distinct meanings where known and never guessing an expansion

#### Scenario: Tables serve comparison without replacing reasoning

- **WHEN** a report compares several systems, options or findings across common attributes
- **THEN** it uses a labelled table for that comparison and retains the judgement, causal reasoning and requested action in prose; one straightforward finding remains clear narrative rather than an artificial table

#### Scenario: Evidence maps beside the claim

- **WHEN** a report states an evidence-backed fact or premise
- **THEN** it carries an adjacent source URL, source-root-relative path with available anchor, issuer-qualified locator, or resolving report citation, and it labels a missing source or precise anchor rather than inventing a link

#### Scenario: Inference and unsupported assertion remain distinct

- **WHEN** a report draws a conclusion from observations or cannot support a claimed fact
- **THEN** it labels the conclusion as inference and maps its supporting observations, or labels the support limitation instead of presenting the assertion as verified

#### Scenario: A citation needs no quotation

- **WHEN** a report accurately paraphrases an evidence-backed observation
- **THEN** it may use a usable reference without reproducing a quotation

#### Scenario: The specialist layout supports local source references and chapter order

- **WHEN** the credential-sweep HTML layout is used for a finished report
- **THEN** it places `Acronyms and abbreviations` after Hand-off and before the footer, uses the existing grid table or an explicit no-terms message, keeps Aleph links only for genuine Aleph evidence, and permits a source-root-relative escaped local path plus locator without manufacturing an `href`

#### Scenario: A bounded hand-back remains a hand-back

- **WHEN** an analyst returns a bounded status or dispatch hand-back rather than a finished report
- **THEN** it expands any reader-facing terms and maps its evidence, but does not add a report chapter merely to imitate a finished product