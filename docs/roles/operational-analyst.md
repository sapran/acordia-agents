# The Operational Analyst

## A competency map for the Analysis pillar of ACORDIA

**Version 1.2 · 21 August 2026**

*Offensive framing, written in operator's terms rather than staff doctrine. "Analysis" here is the ACORDIA core pillar — real-time decision support and target understanding — given a human shape: the role, its specialisations, and the skills that make it up. The load-bearing claim is Monte's: analysis directs each step of an operation, and it is analytical judgement, far more than any exploit, that separates operations that land from operations that stall. v1.2 makes two things explicit that earlier versions got wrong. The operation's end is **threefold**, not dual — an **effect** (break, deny, manipulate), **intelligence** (collect), or **access** held because it may become useful later — and beside it sits a second axis, the **operating logic** by which the operation acts: espionage, sabotage or subversion. The analyst's job is end-neutral across all three ends, but never end-agnostic, because they compete for the same access and pull in different directions.*

## The general role: the operational analyst

The operational analyst turns what the operation can see into what it should do. They build and hold an understanding of the target — not only how its systems, users and administrators behave, but what the target is *for*: its objectives, the processes that carry them, and therefore what it most depends on. They notice when that picture shifts. And they carry the running judgement on which method to use, when to move, how much risk each option holds, and — once an action is taken — whether it achieved the operation's end and what to do next.

Because the end is threefold, so is the judgement of success: for an effects operation the question is whether the target actually broke or changed; for a collection operation whether the take is real and worth having; for an access operation whether the foothold is established, durable and unnoticed. The same access frequently serves more than one, and the line is thin — as one practitioner-lawyer reading has it, "the only difference between … operations intended to collect intelligence and those designed to deliver cyber effects is the intent" (Maurer, *Cyber Mercenaries*, p. 77). Effects and collection compete for the same access and tempo and pull in opposite directions — effects want timing, collection wants patience and discretion (grugq, *Cyber Warfare: A Simple Framework*, p. 2). The scholarly statement of the same tension is sharper: spies are "temperamentally averse to exploiting their presence to disrupt enemy operations," because disruption raises the discovery risk that collection depends on (Rovner, Cormac & Maschmeyer, *Sand in the gears*, p. 10).

The work has a particular shape. The analyst is as often starved of information as drowning in it, and a large part of the job is naming what they do not yet know and going to get it. They pull together scraps from unrelated sources — technical telemetry alongside the non-technical — to answer urgent, concrete questions. Monte's is the canonical example, and it is worth quoting in full because it shows how far past the wiring the work reaches:

> "an operational question might be, 'If and when will the target upgrade?' This simple question is crucial for sustaining an operation. Answering it may require understanding the target's finances, their access to new equipment, their update history, or even the temperament of the system administrators." — Monte, *Network Attacks & Exploitation*, p. 60

Read that list again: finances, procurement, history, the people. None of it is on the wire. This is the **business analysis** half of the craft — understanding the target as an organisation, not just as a network — and it is what tells the analyst which of ten thousand systems actually matters. Its structured forms are well established: a crown-jewels analysis that describes the target "from the perspective of mission objectives … and technical assets" and weighs "the impact that the loss or reduced functionality of these systems would have" (*Cyber Commanders' Handbook 2*, p. 45), and mission-thread analysis, which traces a business process end-to-end — "the what," the steps of the work — before mapping down to the systems that carry it, "the how" (Karagosian, *Cyber Defense Review*, p. 44; Corbari et al., *Mission Thread Analysis*, p. 6). Defenders run these on their own missions; offensively you run them on the target, to learn what it is trying to do and therefore what is worth hitting or holding. Every operational analyst carries this at a working level; the deep method lives with the Target & Network specialist.

This is why analysis belongs among the core activities of an operation rather than off to one side as support. Underfeed it and you get capability without effect — operators holding access they cannot turn into outcomes. It is also the least teachable part of the craft: it rests on years of mixed technical and non-technical experience and does not compress into a syllabus.

Before any specialisation, then, every operational analyst carries the same analytic spine: reasoning under uncertainty and overload; a working grasp of what the target is *for* and what it most depends on; disciplined hypothesis testing; a standing check on their own assumptions; a working immunity to deception (the analyst is themselves a target); calibrated confidence; the judgement that turns all of it into a recommended course of action at the tempo of the operation; and the end-neutral loop that asks, after each move, whether the operation's end was met and what follows. On top of that spine sits a baseline of technical literacy — enough fluency in traffic, hosts, logs and scripting to read the raw material. Deep technical command is where the specialisations begin.

## The four specialisations

An operational analyst becomes a specialist not by reasoning differently — the spine is shared — but by the technical substrate they command deeply enough to take apart from the inside. Each of the four answers a different question and demands a different toolkit. **That criterion is the test a leg has to pass**, and v1.1 shipped one that failed it.

*(v1.0 carried an Effects & Assessment analyst. It was dissolved in v1.1: every source that justified it came from military assessment doctrine — measures of effectiveness, battle-damage assessment, the commander's end-state — and none from the practitioner canon this map is written in. In practitioner terms, assessment is the spine's end-neutral loop, and its technical reads redistributed to the legs.)*

*(v1.2 dissolves a second, the Fusion analyst, on the criterion above. Its own description gave it away — "where the others go deep, the fusion analyst goes wide" — which is the negation of the property that makes a leg a leg, and the grid agreed: six deep marks against twelve and thirteen, five of them unique. It also contradicted the lead, which already claimed to hold the picture. Its work went three ways, recorded under "How the pieces fit". In the same version Target & Network split, because its own description conceded it was "two halves" and those halves are different substrates.)*

### Mission Analyst

*"What is this target for, what does it depend on, how does it behave — and would degrading it actually be felt?"*

The target as an **organisation**. The crown-jewels and mission-thread work above, which establishes what the target is trying to do and therefore what matters — because a map of everything is only prioritisable once you know what is worth prioritising. Pattern-of-life and change-cycle forecasting, which are questions about people and procurement more than about packets. The non-technical context — finance, geopolitics, the human terrain — that the old Fusion leg held and that belongs here, beside the mission model it explains.

And the read that decides whether a disruptive action is worth taking: **friction susceptibility**. Sabotage is the weaponization of friction to degrade performance from within, and how much degradation a target actually suffers depends on its bureaucratic characteristics — the rigidity of its standard operating procedures, whether it holds redundant systems *and* people trained to switch to them — and on its culture, because an organisation whose norms discourage reporting suffers larger practical effects while one that discloses immediately resists those and is exposed instead to blame-shifting and lost trust (Rovner, *Theory of sabotage*, p. 11; Rovner, Cormac & Maschmeyer, *Sand in the gears*, pp. 7–8). This analyst therefore owns the organisational half of *did it land*: whether the mission changed, not whether the host did.

### Terrain Analyst

*"What is the estate made of, where can we move, what does the trust allow — and did the system change?"*

The terrain itself: networks, protocols, routing and architecture; identity and directory systems and the trust between them; cloud control planes; web and application stacks; the mapping of vulnerability and attack surface; with working command of host internals and, where the target demands it, operational-technology environments. Attackers work in fog from the moment of access, so the defining competence is envisioning plausible layouts, configurations and traps from fragments — and marking which of the map is observed and which inferred.

Attack surface is a part of this seat, not the point of it. Control — turning a foothold into capability — relies mostly on non-exploit methods: credential reuse, administrative tooling, native protocols (Styran, *Rethinking Exploitation in Cyber War*, p. 21). This analyst owns the technical half of *did it land*: whether the system actually changed, as distinct from whether the payload ran.

### Overwatch Analyst

*"Will this be seen, is it being seen right now, and is our operation still clean?"*

Two registers. The **static** read is how the defence detects in principle: endpoint telemetry and the internals of detection tooling; network sensors and traffic; log and artefact capture; cloud and identity logging; and the evasion that follows from knowing all of it. The **live** register is **overwatch** — reading data pulled from the defender's own security operations, plus external signals, to predict whether they are onto the operation and when they will be. (The term is yours: the ODC "Trigger Overwatch" pattern is its defensive twin, and the OPM "advanced monitoring phase," where responders quietly watched the intruder before the "Big Bang," is the same logic run from the blue side.)

Overwatch feeds the Control decision — go quiet, move, or pull out — but does not take it. Control is a different ACORDIA pillar and this distribution does not ship it, so the boundary is that this analyst produces the *analysis* that decides, and a human operator acts. The seat also carries the honest self-read, because ease of attack is never a property of the target alone: an operation fails in a permissive environment if it is clumsy, and succeeds against a hard one if it is careful (Lindsay, *Age of Deception*, ch. 2). Reading the environment without reading your own capacity and discretion is half a judgement.

### Collection Analyst

*"Is the take real, what does it say in its own domain — and what do we already know?"*

What was actually left when Fusion dissolved. Access is not comprehension: a complete, authentic take in a subject nobody on the operation reads is worth almost nothing, and worse than nothing read confidently and wrongly. Monte puts linguists and subject-matter experts under targeting capabilities for exactly this reason — stealing from a bank needs the language and a grasp of how the transactions work, even with full access to the network (p. 57). So this seat holds the value and quality of the take, its interpretation in its own domain and language, the data-handling muscle to work it at volume, and the operation's **carried memory** — the corporate memory that analysts build and that dies with a dispatched context unless someone writes it down (Lindsay, ch. 2).

It does **not** hold the picture. Correlating far enough to judge the material is its work; assembling the operating picture is the lead's, for the reason the Fusion leg no longer exists.

## How the pieces fit

The model is a shared spine with four legs. The spine is analytic and belongs to everyone; it carries the end-neutral loop that judges whether an operation achieved its end. The legs are technical and separate the specialists.

**The end is threefold, not dual.** v1.1 said an operation exists to create an effect or to collect intelligence. That drops the two objectives that are neither: **strategic access**, held because it may become useful, and **positional access**, on a target of no interest that reaches one that is (Monte, pp. 25–29). Since ACORDIA's central claim is that access rather than the exploit is the core primitive, a map that recognises only effect and collection contradicts the framework it compiles from. The judgement of success is correspondingly threefold: did the system and the mission change, is the take real and worth having, or is the access established and quiet.

Beside the objective sits a second axis the map previously lacked: **the operating logic**. Espionage steals information, sabotage degrades performance from within, subversion manipulates behaviour — sabotage is degenerative where subversion is generative, so the same means codes differently depending on which is intended (Rovner, Cormac & Maschmeyer, pp. 12–13). Clandestine (unseen) and covert (unattributed) are likewise different requirements and conflating them produces incoherent OPSEC. The objective says what the operation is for; the logic says how it acts; neither substitutes for the other.

When the fourth leg dissolved in v1.1, the *judgement* went up into the spine and the technical reads went to the legs. When Fusion dissolved in v1.2, its five unique competencies went three ways: **multi-source fusion** and **maintaining the operating picture** to the lead, because handing a fused picture back across a dispatch boundary strips the detail that made it a judgement — and inter-unit communication is the weak point of any specialist structure (Monte, p. 63); **non-technical context integration** to Mission, beside the model it explains; **take value** and **data-integration tooling** to Collection. Three rows were added in the same version so that Mission and Collection are real seats rather than renamed ones.

Read the four legs side by side and their signatures are distinct: Mission commands the organisational terrain and nothing else; Terrain commands the widest span of technical substrates; Overwatch concentrates in the sensing stack and runs live overwatch; Collection is shallow-but-wide by design, and is a leg anyway because the handling of collected material is itself a depth. Two deep skills — reverse-engineering and operational-technology — belong to no single leg and attach to whichever one needs them for a given operation.

A junior analyst is the spine plus one leg run competently. A senior analyst is the same spine grown comb-shaped across several. What does not change with seniority is the spine — acquired first, shared by all, and the part that cannot be taught quickly.

---

## Appendix — skills at a glance

Reference grid for the map above. **●** deep / defining · **○** working knowledge or draws on it · blank = not central. Read **●** in *Core* as the general analytic spine, **○** in *Core* as the technical or analytic baseline every analyst carries, **●** in a leg as that specialist, and *Core ○ + a leg ●* as a skill that is both baseline-for-all and deep-for-one. Legs: **Mission** the target as an organisation · **Terrain** the technical terrain · **Def** defender & detection · **Coll** collection.

`Core` is `cyber-analyst`'s own column, and it carries two things. A `●` in the *Analytic spine* or
*Cross-cutting technical* sections is the **shared spine** — the twelve every analyst carries, named
in every leg's prompt. A `●` in `Core` anywhere else is the lead's alone: `multi-source-fusion` and
`maintaining-operating-picture` are held by the lead precisely because handing the fused picture
across a dispatch boundary is what retired the Fusion leg.

**Row id** is the row's stable identity. It is minted once, it does not change when the row is reworded, re-marked or moved between sections, and it is never reused after a row is retired. Each grid-row skill cites it as `metadata.acordia.row`. It replaces the line-number anchors carried up to 4.2.0, which resolved silently to the wrong row whenever an edit shifted a line.

| Skill | Row id | Core | Mission | Terrain | Def | Coll |
|---|---|:--:|:--:|:--:|:--:|:--:|
| *Analytic spine* | | | | | | |
| Reasoning under uncertainty & overload | `reasoning-under-uncertainty` | ● |  |  |  |  |
| Naming the gaps | `naming-the-gaps` | ● |  |  |  | ○ |
| Hypothesis testing (competing hypotheses) | `hypothesis-testing` | ● |  |  | ○ |  |
| Key-assumptions check & debiasing | `key-assumptions-check` | ● |  |  |  |  |
| Deception detection / anti-manipulation | `deception-detection` | ● |  |  | ● |  |
| Calibrated confidence | `calibrated-confidence` | ● |  |  |  | ○ |
| Method / timing / risk decision | `method-timing-risk-decision` | ● | ○ | ○ | ○ | ○ |
| Outcome judgement — end achieved (effect, intel, or access held), did the system actually change, & what now | `outcome-judgement` | ● | ● | ● |  | ○ |
| Gain/loss calculus & feedback into re-planning | `gain-loss-calculus` | ● |  |  |  |  |
| Briefing & written reporting | `briefing-reporting` | ● |  |  |  | ○ |
| Human–automation teaming | `human-automation-teaming` | ● |  |  |  |  |
| *The target as an organisation* | | | | | | |
| Target business/mission analysis (crown-jewels / mission-thread) | `target-mission-analysis` | ○ | ● |  |  |  |
| Pattern-of-life / behavioural baselining | `pattern-of-life-baselining` | ○ | ● | ○ |  |  |
| Change-cycle forecasting ("when will they patch?") | `change-cycle-forecasting` |  | ● | ○ |  |  |
| Non-technical context integration (finance, geopolitics, human) | `nontechnical-context-integration` |  | ● |  |  |  |
| Target friction susceptibility — SOP rigidity, redundancy, reporting culture | `target-friction-susceptibility` |  | ● |  |  |  |
| *The technical terrain* | | | | | | |
| Packet & traffic analysis (pcap/netflow) | `packet-traffic-analysis` | ○ |  | ● | ● |  |
| Protocol, routing & network architecture | `protocol-routing-architecture` |  |  | ● | ○ |  |
| OS & host internals (Win/Lin/macOS) | `os-host-internals` | ○ |  | ● | ● |  |
| Web/API, app-logic & auth-flow analysis | `web-api-authflow-analysis` |  |  | ● | ○ |  |
| Cloud control-plane & service analysis | `cloud-controlplane-analysis` |  |  | ● | ○ | ○ |
| Identity & directory (AD/Entra) & trust | `identity-directory-trust` |  |  | ● | ○ |  |
| Vulnerability & attack-surface mapping | `vuln-attacksurface-mapping` | ○ |  | ● | ○ |  |
| *Reading the defender & our own footprint* | | | | | | |
| Detection-capability analysis (how blue sees) | `detection-capability-analysis` | ○ |  |  | ● |  |
| Endpoint telemetry & EDR internals | `endpoint-telemetry-edr` |  |  | ○ | ● |  |
| Cloud & identity log analysis | `cloud-identity-log-analysis` |  |  | ○ | ● | ○ |
| Evasion & anti-analysis reasoning | `evasion-antianalysis` |  |  | ○ | ● |  |
| Own-footprint / emitted-indicator analysis | `own-footprint-analysis` |  |  |  | ● |  |
| Overwatch — live "are we detected?" from exfiltrated defender data | `overwatch` | ○ |  |  | ● |  |
| C2 / beacon / exfil-signal analysis | `c2-beacon-exfil-analysis` |  |  |  | ● | ○ |
| Implant/payload behaviour & reverse-engineering | `implant-payload-re` |  |  | ○ | ● |  |
| Disk & memory forensics | `disk-memory-forensics` |  |  | ○ | ● |  |
| *Holding the picture* | | | | | | |
| Multi-source fusion & correlation | `multi-source-fusion` | ● |  |  |  | ○ |
| Maintaining the operating picture | `maintaining-operating-picture` | ● |  |  |  | ○ |
| *Working the take* | | | | | | |
| Assessing value/quality of the collected take | `assessing-take-value` | ○ |  |  |  | ● |
| Domain & language interpretation of the take | `take-domain-interpretation` |  | ○ |  |  | ● |
| Operational memory — what the operation knows, carried forward | `operational-memory` | ○ |  |  |  | ● |
| Data integration & correlation tooling | `data-integration-tooling` | ○ |  |  |  | ● |
| *Cross-cutting technical* | | | | | | |
| Log / artefact interpretation | `log-artefact-interpretation` | ○ | ○ | ● | ● | ● |
| Analytic tooling & scripting | `analytic-tooling-scripting` | ● | ○ | ○ | ○ | ○ |
| Operational-technology / embedded (attach as needed) | `ot-embedded` |  |  | ○ | ○ |  |

---

## Grounded in

The conceptual spine is the **Analysis** pillar of ACORDIA (Styran), which names real-time decision support and target understanding as a core operational activity in its own right; the practitioner definition of the work is Monte's *operational analysis*. The **threefold end** — effect, collection, or access held for later use — is Monte's five operational objectives read down to their kinds, with the effect/collection tension drawn from Smeets, grugq (twice), Maurer and, in its sharpest form, Rovner, Cormac & Maschmeyer. The **operating-logic axis** — espionage, sabotage, subversion, and clandestine versus covert — is theirs. **Friction susceptibility** is Rovner's *Theory of sabotage* and the same authors' *Sand in the gears*. The **business/mission analysis** craft is grounded in crown-jewels and Cyber Mission Stack modelling (*Cyber Commanders' Handbook 2*) and Mission Thread Analysis (Karagosian; Corbari et al.). **Overwatch** takes its name and shape from the author's own ODC and the mirror-image blue-side monitoring in the OPM breach report; its self-assessment half is Lindsay. The **collection** leg rests on Monte's targeting capabilities and Lindsay's corporate memory. The retirement of the Fusion leg rests on Monte's warning about communication between units. Every work named here is registered in [`sources.md`](sources.md).

### Sources (library)

- Styran, V., *Rethinking Exploitation in Cyber War* (ACORDIA framework; Analysis pillar), pp. 20–24.
- Monte, M., *Network Attacks & Exploitation: A Framework* (operational analysis), p. 60.
- Smeets, M., *No Shortcuts: Why States Struggle to Develop a Military Cyber-Force* (PETIO; effects vs espionage), pp. 17, 32, 97, 105, 121.
- grugq, *Cyber Warfare: A Simple Framework for Understanding Its Role in Armed Conflict* (espionage vs effects), p. 2.
- grugq, *Strategic Adaptation: Russian CYBER@WAR in Ukraine* (effects vs espionage; collection more useful), p. 34.
- Maurer, T., *Cyber Mercenaries: The State, Hackers, and Power* (collect vs effect = intent), p. 77.
- Hickey, Magurno, Pastor, Rodrigues & Štrucl, *Cyber Commanders' Handbook 2* (crown-jewels & Cyber Mission Stack, p. 45; terrain analysis, p. 43; offensive/defensive skill lists, pp. 66, 70; assessment doctrine, p. 86).
- Karagosian, D. S., *The Cyber Defense Review* (Mission Thread Analysis), p. 44; Corbari, Khatod, Popiak & Sinclair, *Mission Thread Analysis: Establishing a Common Framework*, p. 6.
- Styran, V., *The Offense Death Cycle* (overwatch; Cyber Defense Operator), pp. 9, 17.
- U.S. House Committee on Oversight & Government Reform, *The OPM Data Breach* (advanced monitoring / blue-side overwatch), p. 65.
- Minárik et al., *CyCon 2019: Silent Battle*, pp. 114, 117; Orye & Maennel, *Recommendations for Enhancing the Results of Cyber Effects*, pp. 2, 5; JP 3-12, p. 81 — assessment doctrine (basis for the removed fourth leg).
- Hutchins, Cloppert & Amin, *Intelligence-Driven Computer Network Defense… Kill Chains*, pp. 2, 5; Lindsay, J. R., *Information Technology and Military Power*, pp. 166, 179.
- Heuer, R., *Psychology of Intelligence Analysis*, pp. 150–151; Pherson & Heuer, *Structured Analytic Techniques for Intelligence Analysis*, pp. 47, 69, 77, 87.
- Rovner, J., *Theory of sabotage* (weaponized friction; target bureaucratic characteristics and culture), pp. 6, 11–12.
- Rovner, J., Cormac, R. & Maschmeyer, L., *Sand in the gears: Sabotage in world politics* (the definition; the espionage/subversion/sabotage taxonomy and coding rule; secrecy against scale; espionage-sabotage tension), pp. 10, 12–13.
- Lindsay, J. R., *Age of Deception: Cybersecurity as Secret Statecraft* (vulnerable institutions × clandestine organization; corporate memory), ch. 2.

## Agent naming and grid anchors

*The Operational Analyst* remains the role name in the ACORDIA framework this map compiles from. The
shipped lead agent is `cyber-analyst` (wrapper `/cyber-analyst`, short handle `/analyst`), named in
4.0.0 so that no lead agent shares a word with the pillar it leads. The role in this document and the
file on disk are deliberately not spelled the same way; a grid row describes a competency, not an
agent.

**Line anchors are retired as of 5.0.0.** Skills previously carried
`source: docs/roles/operational-analyst.md#L<n>`, which meant nothing could be inserted above the
grid — and which failed silently rather than loudly, because a shifted line still resolves, just to
the wrong row. Each row now carries a stable id in its own `Row id` column, cited by the skill as
`metadata.acordia.row`, and the `source` is the bare path. Rows may be reworded, re-marked, moved
between sections or added above without touching a single skill.

**The legs and their agents, as of 5.0.0.** The four grid leg columns map one-to-one onto the four
leg agents: **Mission** → `mission-analyst`, **Terrain** → `terrain-analyst`, **Def** →
`overwatch-analyst`, **Coll** → `collection-analyst`, with **Core** → `cyber-analyst`. The earlier
**T&N** column split into Mission and Terrain, and the **Fus** column was retired and redistributed;
both moves are recorded under "How the pieces fit". `overwatch-analyst` keeps its name from the live
register that defines it — overwatch, reading the defender's own security operations to judge whether
they are onto the operation.
