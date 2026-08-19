# The Operational Analyst
### A competency map for the Analysis pillar of ACORDIA

**Version 1.1 · 21 July 2026**

*Offensive framing, written in operator's terms rather than staff doctrine. "Analysis" here is the ACORDIA core pillar — real-time decision support and target understanding — given a human shape: the role, its specialisations, and the skills that make it up. The load-bearing claim is Monte's: analysis directs each step of an operation, and it is analytical judgement, far more than any exploit, that separates operations that land from operations that stall. One thing this version makes explicit that v1.0 left implicit: the operation's end is dual. An operation exists to create an **effect** — break, deny, or manipulate — or to **collect intelligence**, and the same access often serves either; the analyst's job is end-neutral, driving toward and judging the achievement of whichever end is in play.*

## The general role: the operational analyst

The operational analyst turns what the operation can see into what it should do. They build and hold an understanding of the target — not only how its systems, users and administrators behave, but what the target is *for*: its objectives, the processes that carry them, and therefore what it most depends on. They notice when that picture shifts. And they carry the running judgement on which method to use, when to move, how much risk each option holds, and — once an action is taken — whether it achieved the operation's end and what to do next.

That last clause is new in this version. Because the end is dual, so is the judgement of success: for an effects operation the question is whether the target actually broke or changed; for a collection operation it is whether the take is real and worth having. The same access frequently serves both, and the line between them is thin — as one practitioner-lawyer reading has it, "the only difference between … operations intended to collect intelligence and those designed to deliver cyber effects is the intent" (Maurer, *Cyber Mercenaries*, p. 77). Effects and collection compete for the same access and tempo and pull in opposite directions — effects want timing, collection wants patience and discretion (grugq, *Cyber Warfare: A Simple Framework*, p. 2) — and in the wartime Ukrainian record the collection end is frequently the more useful of the two (grugq, *Strategic Adaptation: Russian CYBER@WAR in Ukraine*, p. 34; cf. Smeets, *No Shortcuts*, p. 32, on how effect operations "cannot always be clearly delineated from espionage"). The analyst holds no separate seat for judging this; closing the loop — did we get there, what now — is simply the analytic job, running continuously.

The work has a particular shape. The analyst is as often starved of information as drowning in it, and a large part of the job is naming what they do not yet know and going to get it. They pull together scraps from unrelated sources — technical telemetry alongside the non-technical — to answer urgent, concrete questions. Monte's is the canonical example, and it is worth quoting in full because it shows how far past the wiring the work reaches:

> "an operational question might be, 'If and when will the target upgrade?' This simple question is crucial for sustaining an operation. Answering it may require understanding the target's finances, their access to new equipment, their update history, or even the temperament of the system administrators." — Monte, *Network Attacks & Exploitation*, p. 60

Read that list again: finances, procurement, history, the people. None of it is on the wire. This is the **business analysis** half of the craft — understanding the target as an organisation, not just as a network — and it is what tells the analyst which of ten thousand systems actually matters. Its structured forms are well established: a crown-jewels analysis that describes the target "from the perspective of mission objectives … and technical assets" and weighs "the impact that the loss or reduced functionality of these systems would have" (*Cyber Commanders' Handbook 2*, p. 45), and mission-thread analysis, which traces a business process end-to-end — "the what," the steps of the work — before mapping down to the systems that carry it, "the how" (Karagosian, *Cyber Defense Review*, p. 44; Corbari et al., *Mission Thread Analysis*, p. 6). Defenders run these on their own missions; offensively you run them on the target, to learn what it is trying to do and therefore what is worth hitting or holding. Every operational analyst carries this at a working level; the deep method lives with the Target & Network specialist.

This is why analysis belongs among the core activities of an operation rather than off to one side as support. Underfeed it and you get capability without effect — operators holding access they cannot turn into outcomes. It is also the least teachable part of the craft: it rests on years of mixed technical and non-technical experience and does not compress into a syllabus.

Before any specialisation, then, every operational analyst carries the same analytic spine: reasoning under uncertainty and overload; a working grasp of what the target is *for* and what it most depends on; disciplined hypothesis testing; a standing check on their own assumptions; a working immunity to deception (the analyst is themselves a target); calibrated confidence; the judgement that turns all of it into a recommended course of action at the tempo of the operation; and the end-neutral loop that asks, after each move, whether the operation's end was met and what follows. On top of that spine sits a baseline of technical literacy — enough fluency in traffic, hosts, logs and scripting to read the raw material. Deep technical command is where the specialisations begin.

## The three specialisations

An operational analyst becomes a specialist not by reasoning differently — the spine is shared — but by the technical substrate they command deeply enough to take apart from the inside. Each of the three answers a different question and demands a different toolkit.

*(v1.0 carried a fourth, an Effects & Assessment analyst. It has been dissolved. Every source that justified it came from military assessment doctrine — measures of effectiveness, battle-damage assessment, the commander's end-state — and none from the practitioner canon this map is written in. In practitioner terms, assessment is the spine's end-neutral loop, and its technical reads redistribute to the three legs below, noted where they land.)*

### Target & Network Analyst

*"What is the target for, what does it depend on, where can we move, when will it change — and did our action land on it?"*

Two halves. The **business/mission half** comes first: the crown-jewels and mission-thread work above, which establishes what the target is trying to do and therefore what matters — because a map of everything is only prioritisable once you know what is worth prioritising. The **technical half** is the terrain itself: networks, protocols, routing and architecture; identity and directory systems and the trust between them; cloud control planes; web and application stacks; the mapping of vulnerability and attack surface; with working command of host internals and, where the target demands it, operational-technology environments. Because this analyst owns the target model, they also own **effect-on-target verification** — the read of whether the target system actually changed after an action, which is the effects half of "did it land."

### Defender & Detection Analyst

*"Will this be seen, is it being seen right now, and is our operation still clean?"*

Two registers. The **static** read is how the defence detects in principle: endpoint telemetry and the internals of detection tooling; network sensors and traffic; log and artefact capture; cloud and identity logging; and the evasion that follows from knowing all of it. The **live** register is **overwatch** — reading data pulled from the defender's own security operations, plus external signals, to predict whether they are onto the operation and when they will be. (The term is yours: the ODC "Trigger Overwatch" pattern is its defensive twin, and the OPM "advanced monitoring phase," where responders quietly watched the intruder before the "Big Bang," is the same logic run from the blue side.) Overwatch feeds the Control decision — go quiet, move, or pull out. This leg also holds the operation's own footprint, its command-and-control and exfiltration signals, implant and payload behaviour, and the forensics of self-detection — the "are we seen" half of "did it land," absorbed from the old assessment role.

### Fusion Analyst

*"What does all of it, together, mean — and how good is what we have?"*

Where the others go deep, the fusion analyst goes wide: consolidating every strand — the operation's own take, collection, open sources, and the non-technical context of the target — into a single coherent picture, and keeping it current. Breadth practised as a discipline: enough working command of every substrate to speak each specialist's language, paired with real data-handling muscle. And for the collection end specifically, this is where the take is judged — **assessing the value and quality of what has been collected**, which is the collection half of "did it land."

## How the pieces fit

The model is a shared spine with three legs. The spine is analytic and belongs to everyone; it now explicitly carries the end-neutral loop that judges whether an operation — effects or collection — achieved its end. The legs are technical and separate the specialists.

When the old fourth leg dissolved, its work did not vanish; it went where it belonged. The *judgement* — did we get there, what now — went up into the spine. The *effect-on-target read* went to Target & Network, who own the target model. The *are-we-seen read* — footprint, overwatch, command-and-control and exfiltration signals — went to Defender & Detection. The *value-of-the-take read* went to Fusion. What was a separate seat in doctrine turns out, in practitioner terms, to be three technical reads feeding one analytic judgement.

Read the three legs side by side and their signatures are distinct: Target & Network commands the widest span of substrates and, uniquely, the business terrain that makes them matter; Defender & Detection concentrates in the sensing stack and runs live overwatch; Fusion is shallow-but-wide with deep data tooling. Two deep skills — reverse-engineering and operational-technology — belong to no single leg and attach to whichever one needs them for a given operation.

A junior analyst is the spine plus one leg run competently. A senior analyst is the same spine grown comb-shaped across several, and the fusion breadth on top. What does not change with seniority is the spine — acquired first, shared by all, and the part that cannot be taught quickly.

---

## Appendix — skills at a glance

Reference grid for the map above. **●** deep / defining · **○** working knowledge or draws on it · blank = not central. Read **●** in *Core* as the general analytic spine, **○** in *Core* as the technical or analytic baseline every analyst carries, **●** in a leg as that specialist, and *Core ○ + a leg ●* as a skill that is both baseline-for-all and deep-for-one. Legs: **T&N** Target & Network · **Def** Defender & Detection · **Fus** Fusion.

| Skill | Core | T&N | Def | Fus |
|---|:--:|:--:|:--:|:--:|
| *Analytic spine* | | | | |
| Reasoning under uncertainty & overload | ● | | | |
| Naming the gaps | ● | | | ○ |
| Hypothesis testing (competing hypotheses) | ● | | ○ | |
| Key-assumptions check & debiasing | ● | | | |
| Deception detection / anti-manipulation | ● | | ● | |
| Calibrated confidence | ● | | | ○ |
| Method / timing / risk decision | ● | ○ | ○ | ○ |
| Outcome judgement — end achieved (effect or intel), did the system actually change, & what now | ● | ● | | ○ |
| Gain/loss calculus & feedback into re-planning | ● | | | |
| Briefing & written reporting | ● | | | ○ |
| Human–automation teaming | ● | | | |
| *Target understanding — business + technical* | | | | |
| Target business/mission analysis (crown-jewels / mission-thread) | ○ | ● | | |
| Pattern-of-life / behavioural baselining | ○ | ● | | |
| Change-cycle forecasting ("when will they patch?") | | ● | | |
| Packet & traffic analysis (pcap/netflow) | ○ | ● | ● | |
| Protocol, routing & network architecture | | ● | ○ | |
| OS & host internals (Win/Lin/macOS) | ○ | ● | ● | |
| Web/API, app-logic & auth-flow analysis | | ● | ○ | |
| Cloud control-plane & service analysis | | ● | ○ | ○ |
| Identity & directory (AD/Entra) & trust | | ● | ○ | |
| Vulnerability & attack-surface mapping | ○ | ● | ○ | |
| *Reading the defender & our own footprint* | | | | |
| Detection-capability analysis (how blue sees) | ○ | | ● | |
| Endpoint telemetry & EDR internals | | ○ | ● | |
| Cloud & identity log analysis | | ○ | ● | ○ |
| Evasion & anti-analysis reasoning | | ○ | ● | |
| Own-footprint / emitted-indicator analysis | | | ● | |
| Overwatch — live "are we detected?" from exfiltrated defender data | ○ | | ● | |
| C2 / beacon / exfil-signal analysis | | | ● | ○ |
| Implant/payload behaviour & reverse-engineering | | ○ | ● | |
| Disk & memory forensics | | ○ | ● | |
| *Pulling it together* | | | | |
| Multi-source fusion & correlation | ○ | | | ● |
| Non-technical context integration (finance, geopolitics, human) | | | | ● |
| Maintaining the operating picture | ○ | | | ● |
| Assessing value/quality of the collected take | ○ | | | ● |
| Data integration & correlation tooling | ○ | | | ● |
| *Cross-cutting technical* | | | | |
| Log / artefact interpretation | ○ | ● | ● | ● |
| Analytic tooling & scripting | ● | ○ | ○ | ○ |
| Operational-technology / embedded (attach as needed) | | ○ | ○ | |

---

## Grounded in

The conceptual spine is the **Analysis** pillar of ACORDIA (Styran), which names real-time decision support and target understanding as a core operational activity in its own right; the practitioner definition of the work is Monte's *operational analysis*. The **dual end** — effects or collection, sharing the same access and differing mainly in intent — is drawn from Smeets, grugq (twice), and Maurer. The **business/mission analysis** craft is grounded in crown-jewels and Cyber Mission Stack modelling (*Cyber Commanders' Handbook 2*) and Mission Thread Analysis (Karagosian; Corbari et al.). **Overwatch** takes its name and shape from the author's own ODC and the mirror-image blue-side monitoring in the OPM breach report. The dissolved fourth leg was grounded entirely in assessment doctrine (Minárik et al.; Orye & Maennel; *Cyber Commanders' Handbook 2* §5.4; JP 3-12) — retained here only to explain why it was removed. The reasoning discipline of the spine rests on the analytic-tradecraft canon (Heuer; Pherson & Heuer); the technical substrate inventory that seeds the legs comes from the offensive and defensive skill lists in the *Cyber Commanders' Handbook 2*; and the find-and-understand loop and campaign-analysis framing come from Lindsay and from Hutchins, Cloppert & Amin.

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