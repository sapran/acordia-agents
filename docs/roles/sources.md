# Sources

The literature register for this distribution, required by the `doctrinal-provenance` capability.

**This is the only place a work is introduced.** A doctrinal claim in a competency-grid paragraph, an
agent prompt or a skill body cites a **key** from the first column, optionally with a section — never
a bare author name and never a citation invented at the point of use. A skill whose body rests on a
specific work carries `metadata.acordia.doctrine_source` naming the same key.

Technique detail does not belong here. A procedure, an artefact format, a protocol quirk or a triage
rule traces to its **grid row** through `metadata.acordia.row`, not to the literature. The register is
for claims about how operations work, not for how a tool behaves.

The **id** column is the lib.ai library document id — an 8-character prefix, enough for
`library_get_document` and `library_search`. A work with no id is not in the library; the note says
where the text is. An absent work may still be cited, but the citation cannot be verified by reading,
so prefer a registered one where both say the same thing.

## Primary frameworks

| Key | Work | id |
|---|---|---|
| `ACORDIA` | Styran, V., *Rethinking Exploitation in Cyber War: Reassessing the Role of Software Exploits in Wartime Cyber Operations* — the seven pillars, the core/supporting tiers, the Analysis pillar, the exploit contingency principle. Also published in the CyCon 2026 proceedings (`649a6776`), pp. 281–290. | `17fec536` |
| `Monte` | Monte, M., *Network Attacks & Exploitation: A Framework* (Wiley, 2015) — first principles, the six principles, the five operational objectives, the life cycle, the expertise taxonomy, attacker structure. | `c159a333` |

## Theory

| Key | Work | id |
|---|---|---|
| `Smeets` | Smeets, M., *No Shortcuts: Why States Struggle to Develop a Military Cyber-Force* — PETIO; the precision constraint. | `57dc935b` |
| `CPT` | Fischerkeller, M., Goldman, E. & Harknett, R., *Cyber Persistence Theory* — strategic exploitation, initiative persistence, the cyber fait accompli. | `3f1094f2` |
| `Campaigning` | *Cyber Persistence and Campaigning: The Logic and Art of Securing Cyberspace* — the campaigning framework; substitutes, complements and supports; the response-options mindset. | `df9da37a` |
| `Rovner` | Rovner, J., *Theory of sabotage*, *Etudes Françaises de Renseignement et de Cyber* 1:1 (2023) — sabotage as weaponized friction; the target-bureaucracy and target-culture propositions. | `d59c3c45` |
| `Sand` | Rovner, J., Cormac, R. & Maschmeyer, L., *Sand in the gears: Sabotage in world politics*, *EJIS* (2025), doi `10.1017/eis.2025.10025` — the definition; the espionage / subversion / sabotage taxonomy and its coding rule; clandestine versus covert; secrecy against scale; sabotage as enabler. CC-BY. | `c3c79710` |
| `Lindsay` | Lindsay, J. R., *Age of Deception: Cybersecurity as Secret Statecraft* — vulnerable institutions × clandestine organization; corporate memory. | `9bbce0da` |
| `Lindsay-ITMP` | Lindsay, J. R., *Information Technology and Military Power*. | `c31cadf6` |
| `ODC` | Styran, V., *The Offense Death Cycle: Proactive Environmental Control* — the source of the overwatch pattern's defensive twin. | `7fcc3ead` |

## Practitioner and doctrinal

| Key | Work | id |
|---|---|---|
| `grugq-Framework` | grugq, *Cyber Warfare: A Simple Framework for Understanding Its Role in Armed Conflict* — espionage versus effects. | `def55cae` |
| `grugq-Ukraine` | grugq, *Strategic Adaptation: Russian CYBER@WAR in Ukraine*. | `f6e11957` |
| `Maurer` | Maurer, T., *Cyber Mercenaries: The State, Hackers, and Power* — collect versus effect as a difference of intent. | `3f0e2ca5` |
| `CCH2` | Hickey, Magurno, Pastor, Rodrigues & Štrucl, *Cyber Commanders' Handbook 2* — crown jewels, the Cyber Mission Stack, terrain analysis. | `e5531a89` |
| `MTA` | Corbari, Khatod, Popiak & Sinclair, *Mission Thread Analysis: Establishing a Common Framework*. | `7031680f` |
| `OPM` | U.S. House Committee on Oversight & Government Reform, *The OPM Data Breach* — the advanced-monitoring phase, blue-side overwatch. | `caa10064` |
| `SilentBattle` | Minárik et al., *CyCon 2019: Silent Battle*. | `d3a10c32` |
| `Orye-Maennel` | Orye, E. & Maennel, O., *Recommendations for Enhancing the Results of Cyber Effects*. | `a96aa545` |
| `KillChain` | Hutchins, Cloppert & Amin, *Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains*. | `75c09042` |

## Analytic tradecraft

| Key | Work | id |
|---|---|---|
| `Heuer` | Heuer, R. J., *Psychology of Intelligence Analysis* (CIA, 1999). | `5d880095` |
| `SAT` | Pherson, R. & Heuer, R. J., *Structured Analytic Techniques for Intelligence Analysis*. | `7bc0dcc4` |

## Registered but absent from the library

Cited in this repository's history and retained for traceability. Not verifiable by reading here.

| Key | Work | Where to obtain |
|---|---|---|
| `Karagosian` | Karagosian, D. S., mission-thread analysis article in *The Cyber Defense Review*, p. 44. | Army Cyber Institute, *The Cyber Defense Review* — open access. |
| `JP3-12` | U.S. Joint Chiefs of Staff, *Joint Publication 3-12, Cyberspace Operations*, p. 81. | Published doctrine, jcs.mil. |

## Gaps — searched and not found

Recorded so a later reader knows the search happened and returned nothing, rather than assuming the
point was never checked. An empty result is a finding; it is not a licence to fill the space from
recall.

- **A practitioner account of collection-analyst tradecraft as a distinct seat.** Searched for
  processing-and-exploitation, take triage and linguist/SME staffing as an offensive-operations role.
  The library supports the *competence* (`Monte` targeting capabilities, p. 57; `Lindsay` ch. 2 on
  corporate memory) but holds no source that constitutes it as a named seat. The `collection-analyst`
  leg is therefore this repository's own synthesis over those two, and is marked as such rather than
  attributed.
- **An empirical base rate for objective drift.** `Monte` states that operations move between
  objective categories and that this is normal (p. 25), but gives no frequency, and nothing else in
  the library measures it. The grid claims drift happens, not how often.
