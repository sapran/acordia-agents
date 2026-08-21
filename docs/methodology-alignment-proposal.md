# Methodology alignment — proposal

**Status: proposal, not a change.** Nothing here is implemented. Select from §5 and §6 and the
selected items become an OpenSpec change.

Written from the library, not from memory. Every claim below traces to a passage in §2; the
document ids make each read reproducible.

---

## 1. Source register

| Key | Work | Document id |
|---|---|---|
| **ACORDIA** | Styran, *Rethinking Exploitation in Cyber War: Reassessing the Role of Software Exploits in Wartime Cyber Operations* (also CyCon 2026 proceedings, pp. 281–290) | `17fec536` / `649a6776` |
| **Monte** | Monte, *Network Attacks & Exploitation: A Framework* (Wiley, 2015) | `c159a333` |
| **Smeets** | Smeets, *No Shortcuts: Why States Struggle to Develop a Military Cyber-Force* | `57dc935b` |
| **CPT** | Fischerkeller, Goldman & Harknett, *Cyber Persistence Theory* | `3f1094f2` |
| **Campaigning** | *Cyber Persistence and Campaigning: The Logic and Art of Securing Cyberspace* | `df9da37a` |
| **Rovner** | Rovner, *Theory of sabotage*, *Etudes Françaises de Renseignement et de Cyber* 1:1 (2023) | `d59c3c45` |
| **Sand** | Rovner, Cormac & Maschmeyer, *Sand in the gears: Sabotage in world politics*, *European Journal of International Security* (2025), doi `10.1017/eis.2025.10025` | `c3c79710` |
| **Lindsay** | Lindsay, *Age of Deception: Cybersecurity as Secret Statecraft* | `9bbce0da` |

*Sand in the gears* was not in the library. It is CC-BY open access; it has been ingested from the
publisher and is now searchable under the id above. Its §"Sabotage as a distinct phenomenon" supersedes
Rovner's earlier solo *Theory of sabotage*, which it builds on and cites — both are kept because the
2023 paper carries the target-bureaucracy propositions the 2025 article compresses.

---

## 2. Passages — select the ones the prose is written from

### Scaffold — ACORDIA

**[A1]** Seven pillars, two tiers. Core, *exercised during operations*: **Access** — achieving a
foothold through any viable method; **Control** — sustaining presence, privilege, and operational
security; **Analysis** — real-time decision support and target understanding. Supporting, *enabling
operations without conducting them*: **Organization**, **Research**, **Development**,
**Infrastructure**. (p. 20)

**[A2]** "Control determines whether initial access translates into operational capability. Most
control functions rely on non-exploit methods — credential reuse, administrative tools, native
protocols." (p. 21)

**[A3]** "Overinvestment in supporting functions (particularly exploit research and development) at
the expense of core functions (particularly analysis) produces capability without effectiveness. The
empirical finding that operators often possess access but cannot exploit it effectively reflects
precisely this imbalance." (p. 23)

**[A4]** "The contingency principle is that exploits should be employed selectively, not reflexively."
Appropriate against hardened perimeters with no alternatives, under time pressure, or for privilege
escalation on well-configured systems; to be avoided when detection risk exceeds value, stability
matters, zero-days warrant preservation, or alternatives exist. (p. 23)

**[A5]** Infrastructure is three domains requiring *isolation from each other*: control (C2, staging,
exfiltration), preparatory (labs, target simulation), organizational (secure comms, data management,
analytics). Research is separated from Development because "discovering a capability and engineering
it into deployable form require different skills, timelines, and structures." (p. 22)

> The paper defines pillars and resource allocation. **It does not define roles or specialisations.**
> Those come from Monte, which the paper cites at exactly the point where Analysis is defined.

### Conduct — Monte

**[M1]** Three tiers of durability: **first principles** (Access, Humanity, Economy) → **principles**
(Knowledge, Awareness, Innovation, Precaution, Operational Security, Program Security) → **themes**
(Diversity, Stealth, Redundancy). "Themes make poor stand-alone goals without principles and context.
Stealth, for example, has no meaning unless one defines from what and for what purpose." (pp. 32–34)

**[M2]** First principles, verbatim: "There is always someone with legitimate access and a means to
use it." / "Ambitions always exceed available resources… There is a priority, cost, and benefit to
every action and to every outcome." (p. 32)

**[M3]** **Five operational objectives**: strategic collection, directed collection, non-kinetic CNA,
strategic access, positional access. "An operation falls into one or more of these categories at any
given point in time. Operations, though, are not static. An operation may begin as firmly fixed in
one category, but change over time or with a change of circumstances." (p. 25)

**[M4]** **Life cycle**: "targeting, initial access, persistence, expansion, exfiltration, and
detection… Although it is often useful to think of the stages as discreet steps, one leading to
another, this is inaccurate. Each stage often remains ongoing throughout the entire operation. The
true life cycle of an operation is more like Figure 2.2 — a tangled mess." (p. 38)

**[M5]** **Six expertise types** under Economy — the actual role taxonomy: targeting capabilities
(all-source intelligence, linguists, subject-matter experts), exploitation, networking, software
development, operational expertise, operational analysis. Three of the six "must be learned outside
of standard programs" / "not taught". (pp. 57–60)

**[M6]** **Attacker structure — form follows function.** Six functional teams derived from the life
cycle: Targeting (drives the operation, gives the orders), Door-kicking (initial access), Rapid
analysis (persistence and immediate expansion), Networking (long-term expansion and exfiltration),
Maintenance (sustainment), Infrastructure. Supported by up to four teams: general-purpose and
tactical vulnerability discovery, tactical and general-purpose software development. (pp. 61–62)

**[M7]** The three conclusions that follow, verbatim (p. 63):
> - Attackers are composed of specialists with depth of skill.
> - Coordinating specialties requires some level of organizational complexity.
> - **The communication between units is a potential weak point.** Given the Attacker is human, the
>   different tempos, risk tolerances, tools, expertise, and leadership of the units will inevitably
>   lead to miscommunication and potential mistakes.

**[M8]** "Operational analysis is leveraged to direct each step and every movement of the Attacker in
every stage of the life cycle… Analysts must synthesize information from disparate sources across
disciplines to answer urgent questions… they must not only analyze the information they have, but
also determine what they are lacking." (p. 60)

### Bedrock

**[S1]** Smeets: "Causing any type of cyber effect, against any system or computer network, at an
unspecified point in time, lacking strategic purpose, is easy. Causing a precise cyber effect, at a
designated point in time, with no — or little — undesired consequences, and with a strategic purpose,
is hard." (p. 16)

**[S2]** Smeets: organisations have capabilities independent of the people in them — "one could take
two sets of identically capable people and put them to work in two different organizations, and what
they accomplish would likely be significantly different." (p. 115, quoting Christensen)

**[C1]** CPT: the cyber fait accompli is "a limited unilateral gain at a target's expense where that
gain is retained when the target is unaware of the loss or is unable or unwilling to respond… the
setting of security conditions in one's favor." (p. 47)

**[C2]** CPT: the environment is one of **strategic exploitation**, not war, coercion or deterrence;
states pursue **initiative persistence** through continuous non-violent campaigns. (pp. 13, 99)

**[C3]** Campaigning, ch. 7 — three ways cyber relates to a shooting war. **Substitutes**: broad
scholarly consensus that substituting cyber for kinetic is unlikely to be strategically impactful.
**Complements**: effects no other capability can provide, contributing indirectly to violence.
**Supports**: employed in tandem with non-cyber capabilities — "they increase the power, precision,
range, or resilience of conventional means" (Ukrainian fire control, ISR, battle-damage assessment,
deep strike). (pp. 151–156)

**[C4]** Campaigning: the **response-options mindset** — developing cyber capabilities and shelving
them until a trigger — is the legacy error. Campaigning continuously sets and structures the
conditions before the crisis exists. (p. 149)

**[R1]** Rovner (2023): sabotage operations "weaponize friction, reduce efficiency, and cause
frustration to accumulate." Stuxnet did not cause catastrophic breakdown; it "slowly manipulated the
timing of centrifuge operations, increasing materials fatigue and confusing Iranian engineers." (p. 6)

**[R2]** Rovner (2023), proposition 1: "The effects of sabotage depend on the bureaucratic
characteristics of the target. Sabotage is more likely to increase friction against organizations with
inflexible standard operating procedures… Success is also more likely when target organizations lack
redundant systems." Resilience "comes from a combination of diverse processes, backup capabilities, and
personnel ready to use them." (p. 11)

**[R3]** Rovner (2023), proposition 2: the practical *and psychological* effects depend on bureaucratic
**culture**. An organisation whose norms discourage reporting suffers larger practical effects; one
whose norms demand immediate disclosure resists them but is more vulnerable to blame-shifting and
morale damage. (pp. 11–12)

**[G1]** Sand — the definition: "sabotage is the weaponization of friction to degrade the performance
of systems from within. This inherently relies on clandestine intrusion but deliberately leaves open
levels of acknowledgement and violence." (p. 13)

**[G2]** Sand, Table 1, *Key Attributes of the Dark Arts* — five terms that are routinely conflated
and are not the same thing (p. 12):

> | | |
> |---|---|
> | Clandestine operations | Secret; victims cannot see anything amiss |
> | Covert operations | Hinges on non-acknowledgement; victims cannot attribute responsibility |
> | Espionage | Clandestine intrusions to steal information |
> | Subversion | Generative; hinges on intrusions to manipulate behaviour from within |
> | Sabotage | Destructive or subtractive; the weaponization of friction to degrade performance from within |

**[G3]** Sand — the distinction that does the work: "Whereas subversion manipulates behaviour, sabotage
degrades performance… Subversion is generative, seeking to alter what the machine produces or even
change the machine altogether. Sabotage does not change the behaviour of targets, but rather subtracts
capability by degrading their performance. It is degenerative." The same means codes differently by
logic: disinformation "is sabotage if it degrades the information ecosystem but subversive if it
generatively influences opinion." (p. 13)

**[G4]** Sand — sabotage and espionage pull against each other on the same access: "spies are
temperamentally averse to exploiting their presence to disrupt enemy operations. Sabotage risks this
kind of compromise… Because sabotage heightens the risk of discovery, agents have good reasons to lay
low." But they can also compound — sabotage "can enable espionage if the goal is to learn more about
how adversaries behave under stress", and friction "can alienate disgruntled bureaucrats" into new
sources. (p. 10)

**[G5]** Sand — the trade-offs. From the covert-action literature, secrecy against scale: "Operations
large enough to make a difference strategically face a high risk of being discovered and neutralized
before producing an effect, while those small enough to stay hidden are likely to fall short of
producing a strategically relevant impact." And by adoption: "Maschmeyer discovered a trilemma between
speed, intensity, and volatility in subversion operations that we argue is shared by sabotage
operations as well." (p. 12)

**[G6]** Sand — the central strategic finding: sabotage "is limited as a stand-alone tool, but rather
works to enhance and enable other policy instruments… degrading performance creates space for other
policy tools." Five categories where it enables and enhances: adversarial diplomacy,
counterproliferation, counterterrorism and counterinsurgency, deterrence, and conventional war. (pp. 3,
13–18)

**[G7]** Sand on war: sabotage injects friction "into command and control (C2) systems… into
intelligence networks, making it harder for enemies to maintain battlespace awareness; and into the
routines of large armed bureaucracies". "The logic of wartime sabotage requires thinking about conflict
as a contest of bureaucratic efficiency, not just a test of strength." (pp. 17–18)

**[G8]** Sand on timing — the corrective to a warfighting framing: "sabotage is more likely to succeed
during peacetime than in a deep crisis or conflict. Friction accumulates slowly… states in crises are
likely to take pre-emptive steps to harden communications, create alternative and redundant networks…
Saboteurs will have a difficult time achieving their goals against alert defenders." (p. 17)

**[G9]** Sand — the humbling claim for a cyber distribution: "when damage and destruction are the aim,
traditional sabotage likely remains the more potent threat." Israel chose explosives over cyber at
Natanz in 2021 — the same facility Stuxnet hit — and the recent European campaign "overwhelmingly
involves traditional rather than cyber means". (pp. 9, 18)

**[L1]** Lindsay: intelligence performance is the interaction of **vulnerable institutions**
(connectivity × vulnerability → exposed / disconnected / secure) and **clandestine organization**
(capacity × discretion → sophisticated / dependent / noisy / incapable). "There are more logical ways
for the attacker to fail than succeed." (ch. 2)

**[L2]** Lindsay: "A popular generalization about cybersecurity is that cyberspace makes offense easy.
Sometimes it does. But offense may fail even in extremely vulnerable environments if attackers are
incompetent… Any generalization about the ease of attack is at least conditional on the proficiency
of the attacker." (ch. 2)

**[L3]** Lindsay: the unglamorous half — "the administrative scutwork of anarchy". Recruit, train and
coordinate; discover and master vulnerabilities; develop and test tradecraft; build corporate memory;
establish control and logistics; plan, rehearse, execute. (ch. 2)

---

## 3. Diagnosis

The distribution is **half a methodology**, and the halves do not compose.

**D1 — The Analysis pillar already implements the framework; the Operations pillar does not.**
`docs/roles/operational-analyst.md` is a genuine derivation: it opens by naming Analysis as the
ACORDIA core pillar, quotes Monte p. 60 in full as its load-bearing claim, and cites the practitioner
canon throughout. `docs/roles/operator.md` is provenance for a verbatim port — it records where the
text came from, and nothing about why those four agents are the right four. The Operations pillar has
no derivation at all.

**D2 — "Operations" is not an ACORDIA pillar, and its agent boundaries come from a service catalogue.**
The framework's operational tier is Access, Control and Analysis [A1]. The shipped pillar is
`web-application`, `mobile-application`, `cloud-security`, `internal-network` — a commercial pentest
service-line taxonomy, organised by *target surface*. That is the exploit-and-surface framing the
paper was written to argue against [A3, A4]. The repository's own name is currently carried by a
structure that traces to the framework in one pillar out of two.

**D3 — The two orchestrators cannot be in the same operation.** `cyber-analyst` is described as "the
primary brain for an offensive operation" running an end-neutral effect-or-collection loop.
`cyber-operator` is described as running "an authorized penetration test or red-team engagement",
routing "recon-through-exploitation phases". They do not share an objective concept, a life cycle, or
a state file. The distribution ships two products with one badge.

**D4 — No operational objective exists anywhere in the harness.** Monte's five categories [M3] are
what make an operation an operation rather than a sequence of techniques, and objective *drift* is the
normal case, not the exception. Nothing asks what the operation is for, and nothing notices when the
answer changes. The analyst grid comes closest — it declares the end "dual", effect or collection —
but that collapse **drops strategic access and positional access entirely**, which is precisely
ACORDIA's central claim: access is the core primitive, and access held for later use is an objective
in its own right [A1, M3].

**D5 — Labour is divided by surface where both sources divide it by function.** Monte derives six
teams from the six life-cycle stages and treats surface expertise as the *support* axis [M4, M6]. The
repo has only the support axis. This is not merely doctrinal: it is why there is no agent that owns
persistence, no agent that owns sustainment, and no agent that owns infrastructure — the three
functions with the longest time horizon.

**D6 — Monte names one weak point in the whole model, and a subagent harness maximises it.** "The
communication between units is a potential weak point… different tempos, risk tolerances, tools,
expertise, and leadership… will inevitably lead to miscommunication and potential mistakes" [M7]. A
dispatched subagent's context is destroyed on return; the handoff *is* the operation. `operation-journal`
carries state — files, severity, confidence, chaining — but there is no contract for what a dispatching
agent must state and what a returning agent must return. This is the highest-value gap in the
repository and it is cheap to close.

**D7 — Economy is the unrepresented first principle.** "Ambitions always exceed available resources…
there is a priority, cost, and benefit to every action and to every outcome" [M2], and the
characteristic failure is capability without effectiveness [A3]. No prompt weighs cost against
benefit, and none applies the exploit contingency principle [A4]. Operational Security and Program
Security are Monte principles 5 and 6; the current `## Guardrails` section is an *integrity* posture
(do not modify the evidence), which is a different thing entirely.

**D8 — The bedrock is absent, and most of it should stay absent.** Only a few pieces earn a place in
procedure rather than framing, and each attaches to one seat. The largest is the sabotage material.
Table 1 [G2] is a working taxonomy of *operating logics* — espionage, subversion, sabotage — that the
harness lacks entirely, and [G3] supplies the rule for coding which one a given action is: the same
means is sabotage if it degrades performance and subversion if it manipulates behaviour. This sits
directly on top of D4 rather than replacing it, because Monte's five categories name what an operation
is *for* while Table 1 names *by what logic it acts*, and neither substitutes for the other. Beneath
that: Rovner's target-bureaucracy and target-culture conditionals [R2, R3], which make sabotage a
modelled property of the target rather than a technical effect; the espionage-versus-sabotage tension
on shared access [G4], which is a better-sourced statement of the effect-versus-collection conflict the
analyst grid already tries to express through a practitioner blog post; and Lindsay's two-factor read
[L1, L2] as a feasibility and self-assessment check. CPT [C1, C2, C4], Smeets [S1] and the
substitute / complement / support triad [C3] belong in framing, not procedure.

**D9 — One finding argues against the distribution's own medium, and should be carried anyway.** "When
damage and destruction are the aim, traditional sabotage likely remains the more potent threat" [G9] —
Israel chose explosives over cyber at Natanz in 2021, the same facility Stuxnet hit. A framework built
on the claim that exploits are one method among many [A4] has no principled way to refuse the next
claim up: cyber is one means among many. Stating it costs nothing and is the difference between
doctrine and marketing. Its operational form is the timing caveat [G8]: friction accumulates slowly,
so sabotage works better against defenders who are not yet alert than against a hardened adversary in
crisis — which is an argument *for* persistent campaigning [C4], not against it.

---

## 4. Design position

Two axes, not one. Monte's own model has both: functional teams derived from life-cycle stages, and
support teams derived from expertise [M6]. **The repo already has the support axis and is missing the
functional axis.** So the fix is additive at the orchestrator, not a teardown of the port:

- The four surface specialists stay exactly as they are — they are Monte's support teams, and they are
  provenance-locked.
- The **orchestrator** carries the functional axis: an objective, a life cycle, a stage, and a handoff.
- Doctrine that must always apply goes in prompts (a few lines). Doctrine that is *consulted* goes in
  skills, description-selected, per pillar — each pillar's seat needs different text, so this is two
  distinct skills, not one duplicated.

---

## 5. Proposed changes

Each is separately acceptable. Bump column is the version consequence.

| # | Change | Touches | Bump |
|---|---|---|---|
| **P1** | **Name the framework and the scope decision in `CLAUDE.md`.** A short section: seven pillars, two tiers [A1]; this repo ships Analysis in full and the Access + Control core through the Operations pillar; the four supporting pillars are deliberately out of scope. An unnamed omission reads as an oversight; a named one is a decision. | `CLAUDE.md` | none |
| **P2** | **Give the Operations pillar a derivation.** `docs/roles/operator.md` gains a derivation section above the provenance: how the four surface specialists map onto Monte's support teams [M6], and the explicit divergence — this pillar's agents are surface-scoped by inheritance while the framework's functions are Access and Control. Records the difference instead of leaving it undocumented. | `docs/roles/operator.md` | none |
| **P3** | **Rewrite the `cyber-operator` prompt around objective → life cycle → stage.** It stops being "runs a pentest" and becomes "runs an operation against a named objective through Monte's life cycle, dispatching surface specialists as support" [M3, M4, M6]. One prompt. The four specialists are untouched. | `acordia-operators/agents/cyber-operator.md`, its wrapper | MINOR |
| **P4** | **Make the operational objective a required, first-class field — two declarations, not one.** Monte's five categories with the drift rule [M3], naming what the operation is *for*; and the operating logic from Table 1 [G2, G3] — espionage, subversion or sabotage — naming how it acts. `.acordia/ops/scope.md` gains both; both orchestrators must name both before acting; a new per-pillar doctrine skill carries the two taxonomies, the drift semantics, and the secrecy-versus-scale trade-off [G5]. | `operation-journal`, 2 new skills, 2 prompts, both grids | MINOR |
| **P5** | **Write the handoff contract.** Extends `operation-journal` (authored here, not ported — free to extend) and its analyst counterpart. Dispatch states: objective, stage, tempo, risk tolerance, what is already known, what must not be touched. Return states: what was done, what was learned, confidence, **exposure incurred**, and what was deliberately not done. Closes D6 [M7]. | `operation-journal` + analyst equivalent, all 9 prompts get one line | MINOR |
| **P6** | **Restore the third end to the analyst grid.** The end is not dual but threefold — effect, collection, **access held for later use** — with Monte's five categories named underneath [M3]. Grid moves first, then the affected skills and the `cyber-analyst` end-neutral loop. | `docs/roles/operational-analyst.md`, ~3 skills, 1 prompt | MINOR |
| **P7** | **Economy and OPSEC as prompt doctrine.** Three or four lines per orchestrator: priority/cost/benefit on every action [M2]; the exploit contingency principle, stated as the conditions for and against [A4]; minimise exposure, minimise recognition, control reaction [M1]. Not an essay — the shortest form that changes behaviour. | 2 prompts | MINOR |
| **P8** | **Bedrock insertions, each at one seat.** Rovner's target-bureaucracy and target-culture conditionals into `target-analyst`'s target model [R2, R3] — the change that makes sabotage a modelled property of the target, and that gives `target-analyst` a reason to model the target's procedures, redundancy and reporting culture rather than only its systems. The espionage-versus-sabotage tension on shared access [G4] into the analyst spine, replacing the weaker sourcing already carrying that claim. Lindsay's two-factor feasibility and self-assessment into `overwatch-analyst` [L1, L2]. Framing only, in the two orchestrators' openings: Smeets's precision constraint [S1], CPT's initiative and fait-accompli logic [C1, C2, C4], the enabling role of sabotage alongside the substitute / complement / support triad [C3, G6, G7], and the peacetime-over-crisis timing caveat [G8]. | 4 prompts, 1–2 skills | MINOR |
| **P9** | **A fifth OpenSpec capability: `doctrinal-provenance`.** Every methodological claim in a prompt, grid row or doctrine skill traces to a named work and section, recorded in a source register at `docs/roles/sources.md`. Mechanically identical to the existing grid bijection, extended to the literature — the analyst grid already does this informally, so the spec formalises a practice rather than inventing one. Optionally `check-acordia.sh` gains a fifth check: every `metadata.source` resolves in the register. | `openspec/specs/doctrinal-provenance/spec.md`, `docs/roles/sources.md`, `~/ai/checks/check-acordia.sh` | none |
| **P10** | **The literature-first rule** (§6). | `CLAUDE.md`, `.claude/commands/opsx/propose.md`, managed skill `acordia-agents-change` | none |

**Rejected, with reasons.** A third `acordia-doctrine` skills-only plugin — a prompt cannot name a
slug outside its own pillar without breaking the slug-resolution invariant, so the binding would be
description-only and weaker than what we have. Renaming `acordia-operators` — MAJOR bump, breaks every
install, buys a word. Adding pillars for the supporting tier — Organization, Research, Development and
Infrastructure are capability-*building*, and an agent distribution is the wrong shape for them; P1
names the omission instead.

---

## 6. The literature-first rule — proposed prose

For `CLAUDE.md`, as step 0 of the OpenSpec workflow:

> ### Literature first — before any change is proposed
>
> No change to an agent prompt, a skill body, a competency grid or a doctrine section starts in an
> editor. It starts in the library.
>
> Before writing `proposal.md` — before writing any prose that will ship — search the lib.ai library
> for what the canon already says about the thing being changed, and bring the passages back. Not a
> summary of them: the passages, quoted, with author, work and page, and the document id so the read
> is reproducible. Present them as a numbered list and stop. The selection is mine; the prose is then
> written from what was selected.
>
> Prose authored before that selection is prose authored from memory, and memory is where this
> repository's characteristic bug comes from — content that no source ever said, with nothing
> recording the difference.
>
> The rule holds when the change looks obvious and when the answer is already known. Being sure is the
> failure mode: the canon is older and more specific than recall of it.
>
> Search the two primary frameworks first — Styran on ACORDIA for what is in scope, Monte for how the
> work is actually divided and conducted — then the bedrock for the question at hand: Smeets on
> capability, Fischerkeller / Goldman / Harknett on persistence and campaigning, Rovner, Cormac and
> Maschmeyer on sabotage as weaponized friction, Lindsay on deception and intelligence performance.
>
> If the library holds nothing on the point, say so and name what was searched. An empty result is a
> finding, not a licence to invent.

The rule in `CLAUDE.md` alone is weakly enforced — it is read only when someone reads the file. The
same requirement goes into `.claude/commands/opsx/propose.md`, which is where a change actually
begins, and one line into the managed `acordia-agents-change` skill.

---

## 7. Sequencing

P1, P2, P9 and P10 first — they are documentation and specification, cost no version bump, and P9 is
what makes everything after it checkable. Then P4, P5 and P6 as one change, because the objective, the
handoff and the third end are the same idea seen from three seats. Then P3, P7 and P8 as the prompt
wave. Grid before artifacts throughout, in the same change, per the standing rule.

---

## 8. Selection — decided 2026-08-21

Thirty of thirty-four passages selected, walked through in four tranches. This section is
normative for the prose authored in change `analysis-only` §4: an agent prompt, a grid paragraph or a
doctrine skill is written from these and no others. A passage not listed here was considered and
rejected, which is a different thing from not having been read.

### Standing rules — every analyst prompt

| Passage | What it obliges |
|---|---|
| **M2** | Economy. Priority, cost and benefit weighed on every action; nothing is free. |
| **M7** | The handoff is the weak point. Supplies the dispatch/return contract in §4 of the tasks. |
| **M8** | Analysis directs every step, and every return names what is *not* known. |

### Doctrine — consulted, not always-on

| Passage | Seat |
|---|---|
| **A4** | Exploit contingency — selectively, not reflexively, with the conditions both ways. |
| **G9** | Cyber is often not the most potent means. Carried deliberately against interest. |
| **G5** | Secrecy against scale, and the speed/intensity/volatility trilemma. |

### The two axes — `cyber-analyst`, and the grid

**Objective — what an operation is for:** **M3** (five categories and objective drift), **M4** (the
life cycle, including that the real one is a tangled mess), **A1** (seven pillars, two tiers, as scope
framing).

**Operating logic — by what logic it acts:** **G2** (clandestine / covert / espionage / subversion /
sabotage), **G3** (the coding rule that makes G2 applicable), **G1** (sabotage defined).

### Per leg

| Agent | Passages |
|---|---|
| `mission-analyst` | **R2** target bureaucratic characteristics · **R3** bureaucratic culture · **L1** vulnerable institutions half |
| `terrain-analyst` | **A2** control turns access into capability, mostly without exploits |
| `overwatch-analyst` | **L2** ease of attack is conditional on attacker proficiency · **L1** clandestine-organization half |
| `collection-analyst` | **M5** linguists and subject-matter experts · **L3** corporate memory · **G4** espionage and sabotage compete for the same access |

`L1` is one passage serving two seats: the target read at `mission-analyst`, the self-assessment at
`overwatch-analyst`.

### Lead framing — `cyber-analyst` opening

**A3** capability without effectiveness · **S1** precision at a designated time is the hard part ·
**C2** strategic exploitation and initiative persistence · **C4** the response-options mindset is the
legacy error · **C1** the cyber fait accompli · **C3** substitutes / complements / supports ·
**G6** sabotage as enabler rather than stand-alone · **G7** war as a contest of bureaucratic
efficiency · **G8** peacetime beats crisis.

### Kept over the recommendation to drop

**A5** — the three isolated infrastructure domains, and Research separated from Development. Retained
although both supporting pillars are out of scope. Its usable reading for a single-pillar analysis
distribution is the *isolation* principle applied to the analyst's own working surfaces: collected
material, working notes and the finished product are three separate things and must not contaminate
each other. That is already the shape of the `## Guardrails` posture and the `.acordia/` layout, so
A5 becomes its citation rather than new scope.

### Rejected

**M1** principles and themes — the one usable line (stealth needs a named observer) survives as a
sentence, not a section. **R1** friction accumulates — restates G1. **M6** the six attacker teams —
already spent in `design.md` justifying the roster; describes an organisation the reader does not
have. **S2** organisations have capabilities independent of their people — true, and no seat acts on
it.

### The seam, filled

**C4 was restored** after the walkthrough, to close the gap it left with G8. G8 says friction
accumulates slowly and works poorly against an alert defender in crisis; on its own that reads as
timing advice. C4 names the response-options mindset — build a capability, shelve it, wait for a
trigger — as the legacy error, which is the argument G8's timing point actually rests on. C2 carries
initiative persistence at the strategic level and C4 now carries its operational half, so the lead's
framing states the persistence case at both levels rather than leaving G8 to imply it.
