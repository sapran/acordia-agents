#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Build the ACORDIA plugin marketplace trees from the opencode-native source.

The files under `<pillar>/agents/`, `<pillar>/skills/`, and `commands/acordia/`
are the source of truth for every harness. Neither omp nor Claude Code will
load the opencode agent files as they stand: both read `tools` off a fixed
`<plugin-root>/agents/` path, but Claude Code expects capitalised Claude tool
names while omp expects lowercase omp names and additionally needs `spawns`
for the orchestrators' delegation allowlists. One `agents/*.md` therefore
cannot serve both, so this script materialises two plugin trees from the one
source — one Claude-shaped, one omp-shaped — each listed by its own
marketplace catalog at the repository root.

Everything under `plugins/`, `.claude-plugin/`, and `.omp-plugin/` is generated
build output. It is committed, because a marketplace install clones the
repository and the trees have to exist in git — but it is never edited by hand.
`tools/build-plugins.py --check` is the drift gate.

Usage:
  tools/build-plugins.py            # regenerate the trees in place
  tools/build-plugins.py --check    # build to a tempdir and diff; exit 1 on drift
  tools/build-plugins.py --doctor   # report install skew, shadowing, and prompt hygiene
  tools/build-plugins.py --doctor --strict   # same, but exit 1 on an install-state finding
"""

from __future__ import annotations

import argparse
import filecmp
import itertools
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# BUMP THIS ON EVERY CHANGE THAT REACHES A USER. It is the only update signal
# either plugin harness has: omp's upgrade path compares this string against the
# installed one and skips when they match, so an unbumped version means an
# edited prompt never reaches anyone who already installed the plugin.
#
#   MINOR — any change to an agent prompt, a skill body, or a command wrapper
#   MAJOR — a serious change: the roster, a pillar, or the shape of the
#           distribution itself
#
# Real semver, because a hand-maintained version is monotonic and both
# harnesses then compare it correctly by precedence. Verified against omp
# 17.1.8: a newer semver upgrades and an older one is skipped. Do NOT hang a
# hash or build metadata off it — `1.0.0+aaa` and `1.0.0+bbb` compare EQUAL and
# would never upgrade.
VERSION = "2.5.0"
MARKETPLACE_NAME = "acordia"
OWNER = {"name": "ACORDIA"}
REPOSITORY = "https://github.com/sapran/acordia-agents"

# This script is the single source for plugin identity. A pillar maps to
# exactly one plugin so the read-only analysis pillar can be installed without
# the write-capable offensive one.
PLUGINS = {
    "acordia-analysts": {
        "pillar": "analysts",
        "description": (
            "ACORDIA Analysis — four read-only decision-support agents and a "
            "43-skill analytic library."
        ),
        "category": "security",
        "keywords": ["security", "analysis", "intelligence", "acordia"],
    },
    "acordia-operators": {
        "pillar": "operators",
        "description": (
            "ACORDIA Operations — five write-capable offensive-security agents "
            "and a 30-skill technique library."
        ),
        "category": "security",
        "keywords": ["security", "offensive-security", "pentest", "acordia"],
    },
}

HARNESSES = ("claude", "omp")

# Tools always available regardless of source permissions. `edit`/`write`,
# `browser`, and `task` are appended conditionally in `translate()`, mirroring
# the source `permission` map so a write-capable pillar translates as
# faithfully as a read-only one. omp appends `yield` itself when a `tools`
# list is present; naming it keeps the generated file honest.
BASE_TOOLS = ["read", "grep", "glob", "bash", "web_search", "todo"]

# opencode's `list` tool has no counterpart in either target harness — in omp a
# directory path handed to `read` enumerates it. This is the legacy analyst
# Tool-discipline paragraph: a byte-exact fallback for prompts still carrying
# that wording. The current analyst prompts name no `list` tool, so the rewrite
# is a no-op for them; the post-rewrite assertion below is what actually
# guarantees no `list` token survives into a generated prompt.
TOOL_DISCIPLINE_SRC = (
    "Use native tools for the filesystem: `read` for contents, `grep` for content "
    "search, `glob` for path/name search, `list` for directories. Reach for `bash` "
    "only when no native tool fits — running analysis scripts, chaining transforms, "
    "invoking real tooling. Do not shell out to cat/head/tail/less/grep/find/ls to "
    "inspect files; native tools are cheaper and return structured results."
)

TOOL_DISCIPLINE_OMP = (
    "Use native tools for the filesystem: `read` for contents (a directory path "
    "lists its entries), `grep` for content search, `glob` for path/name search. "
    "Reach for `bash` only when no native tool fits — running analysis scripts, "
    "chaining transforms, invoking real tooling. Do not shell out to "
    "cat/head/tail/less/grep/find/ls to inspect files; native tools are cheaper "
    "and return structured results."
)

# The same nonexistent tool also appears as an inline token in prose. Unlike the
# paragraph above this one is not present in every file, so it is best-effort —
# the post-rewrite assertion below is what actually guarantees no `list` survives.
INLINE_LIST_SRC = "`read`/`grep`/`glob`/`list`"
INLINE_LIST_OMP = "`read`/`grep`/`glob`"

# omp renders every agent in one flat picker shared with its own built-ins and
# the user's own agents, so the pillar needs a visual signal the way the
# `ACORDIA <pillar> — ` description tag carries the textual one. The value is
# derived from `metadata.acordia.role`, which every source declares and
# `read_agent()` gates, rather than from a filename table, which would be a
# second source of the same fact.
ORCHESTRATOR_COLOR = "cyan"
SPECIALIST_COLOR = "blue"

DEEP_HEADINGS = ("## Your defining spine (deep)", "## Your specialist depth (deep)")

# The `·`-separated slug lines an agent prompt uses to name its skill set. The
# heading above them differs per pillar and has changed shape before, so a line
# is recognised by its content — bare tokens joined by ` · ` — and a newly
# worded heading cannot smuggle an unchecked skill list past the resolution
# gate in `read_agent()`.
#
# Deliberately looser than the kebab-case slug contract itself: matching only
# well-formed slugs would make a line carrying one mistyped slug stop looking
# like a skill line at all, and the whole list would go unchecked. A malformed
# token is caught by the resolution gate instead, which names it.
SKILL_LINE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(?: · [A-Za-z0-9][A-Za-z0-9._-]*)+$")

# `metadata.acordia.role` is the single declaration of an agent's standing. It
# must agree with `mode`, because the harnesses read the mode and the picker
# colour reads the role; a disagreement means one of the two lies.
ACORDIA_ROLES = ("orchestrator", "specialist")

# The destructive/RCE bash denies every write-capable source carries verbatim.
# The list stays in the five `operators/agents/*.md` frontmatters, because
# opencode is the only harness that enforces it and it enforces it from the
# source file. But five hand-synced copies drift, and one edited frontmatter
# leaves the bypass open in the other four; this generator is the only place
# that ever sees all five files at once, so equality is asserted here.
OPERATOR_BASH_DENIES = (
    "*DROP TABLE*",
    "*drop table*",
    "*DROP DATABASE*",
    "*drop database*",
    "*DROP SCHEMA*",
    "*drop schema*",
    "*TRUNCATE TABLE*",
    "*truncate table*",
    "*INTO OUTFILE*",
    "*into outfile*",
    "*INTO DUMPFILE*",
    "*into dumpfile*",
    "*xp_cmdshell*",
    "*sp_OACreate*",
    "*sys_exec*",
    "*sys_eval*",
    "*COPY * TO PROGRAM*",
    "*copy * to program*",
    "*--os-shell*",
    "*--os-cmd*",
    "*--os-pwn*",
    "*--file-write*",
    "*--reg-add*",
    "*--reg-del*",
)

FRONTMATTER_FENCE = "---"

# Every command wrapper opens its body by naming the agent it hands the brief
# to. Leaf wrappers say "Dispatch the `x` agent"; the three orchestrator
# wrappers say "Hand the work below to the `x` agent", because a primary agent
# may have to be switched to rather than dispatched. Both shapes are matched
# here; anything else is a build failure rather than a guess.
COMMAND_AGENT_RE = re.compile(
    r"(?:Dispatch|Hand the work below to) the `([a-z0-9-]+)` agent"
)


class TranslationError(Exception):
    """A source file cannot be faithfully translated."""


def split_frontmatter(text: str, source: Path) -> tuple[dict, str]:
    if not text.startswith(FRONTMATTER_FENCE + "\n"):
        raise TranslationError(f"{source}: no YAML frontmatter")
    end = text.find("\n" + FRONTMATTER_FENCE + "\n", len(FRONTMATTER_FENCE))
    if end == -1:
        raise TranslationError(f"{source}: unterminated YAML frontmatter")
    raw = text[len(FRONTMATTER_FENCE) + 1 : end + 1]
    body = text[end + len(FRONTMATTER_FENCE) + 2 :]
    # A raw ScannerError escapes `main()`'s handler as a traceback that buries
    # the offending path in a stack. Every other failure here names its source
    # file; a parse failure has to as well, or the author cannot tell which of
    # the 73 skills broke.
    try:
        meta = yaml.safe_load(raw)
    except yaml.YAMLError as err:
        detail = str(err).replace("\n", " ")
        raise TranslationError(f"{source}: invalid YAML frontmatter — {detail}") from err
    if not isinstance(meta, dict):
        raise TranslationError(f"{source}: frontmatter is not a mapping")
    return meta, body


def permission_entry(permission: dict, key: str):
    """opencode permissions are either a scalar verdict or a path->verdict map."""
    return permission.get(key)


def allowed_spawns(entry) -> list[str]:
    """Names allowed by a `permission.task` map, ignoring the `"*": deny` floor."""
    if not isinstance(entry, dict):
        return []
    return [name for name, verdict in entry.items() if name != "*" and verdict == "allow"]


def write_posture(entry) -> str:
    """Classify `permission.edit`: outright allow, scoped exception, or denial."""
    if entry == "allow":
        return "allowed"
    if isinstance(entry, dict) and any(name != "*" and verdict == "allow" for name, verdict in entry.items()):
        return "scoped"
    return "denied"


def has_bash_denies(entry) -> bool:
    """True when `permission.bash` is a path/pattern map carrying `deny` rules.

    Neither omp's nor Claude Code's `bash`/`Bash` tool has a per-command
    equivalent — those denies become prompt-level guardrails rather than
    enforced ones.
    """
    return isinstance(entry, dict) and any(verdict == "deny" for verdict in entry.values())


def agent_color(meta: dict) -> str:
    """Orchestrators read apart from their specialists in a flat agent picker.

    Both pillars declare the distinction in one place, `metadata.acordia.role`;
    the gate in `read_agent()` is what guarantees the key is present and agrees
    with `mode`. Anything else is a specialist.
    """
    metadata = meta.get("metadata")
    acordia = metadata.get("acordia") if isinstance(metadata, dict) else None
    if isinstance(acordia, dict) and acordia.get("role") == "orchestrator":
        return ORCHESTRATOR_COLOR
    return SPECIALIST_COLOR


def deep_skills(body: str, source: Path) -> list[str]:
    # The `(deep)` heading shape is normative in the operator roster spec, so
    # it is still parsed on every build and a broken heading still fails the
    # build — even though no emitter consumes the result any more (plugin
    # agents ship with `autoloadSkills` unset, unconditionally).
    #
    # The skill list is the line directly under the heading. If a future edit
    # puts a blank line there, an empty result must abort rather than silently
    # yielding nothing.
    for line in iter_heading_values(body, DEEP_HEADINGS):
        skills = [part.strip() for part in line.split("·") if part.strip()]
        if not skills:
            raise TranslationError(
                f"{source}: the line under the `(deep)` heading names no skills; "
                "the prompt changed shape and the extraction must be revisited"
            )
        return skills
    raise TranslationError(f"{source}: no `(deep)` skill heading found")


def iter_heading_values(body: str, headings: tuple[str, ...]):
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.strip() in headings and index + 1 < len(lines):
            yield lines[index + 1]


def named_skills(body: str) -> list[str]:
    """Every skill slug the prompt names, deduplicated, in first-seen order.

    `deep_skills()` reads one heading and is about prompt shape; this reads
    every skill line in the body, so a slug named under any heading — the five
    in use today or one written next month — is still resolved against the
    pillar's skill directory.
    """
    named: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if SKILL_LINE_RE.match(stripped):
            named += [part.strip() for part in stripped.split("·")]
    return list(dict.fromkeys(named))


def check_bash_denies(entry, source: Path) -> None:
    """A write-capable source must carry the canonical deny set, exactly.

    Set equality, not containment: a pattern present here and nowhere else is
    as much a sync failure as a missing one, and either way the author has to
    decide which of the two lists is right.
    """
    denies = (
        {pattern for pattern, verdict in entry.items() if verdict == "deny"}
        if isinstance(entry, dict)
        else set()
    )
    canonical = set(OPERATOR_BASH_DENIES)
    missing = sorted(canonical - denies)
    extra = sorted(denies - canonical)
    if missing:
        raise TranslationError(
            f"{source}: write-capable agent does not deny {missing[0]!r} "
            f"({len(missing)} of the {len(canonical)} canonical bash denies absent); "
            "the deny set must equal OPERATOR_BASH_DENIES in tools/build-plugins.py"
        )
    if extra:
        raise TranslationError(
            f"{source}: bash deny {extra[0]!r} is not in the canonical set; add it to "
            "OPERATOR_BASH_DENIES and to every write-capable source, or drop it here"
        )


def repo_relative(source: Path) -> str:
    """Provenance should name the artifact, not whichever worktree built it."""
    resolved = source.resolve()
    for parent in resolved.parents:
        if (parent / ".git").exists():
            return str(resolved.relative_to(parent))
    return str(source)


def rewrite_body(body: str, source: Path) -> str:
    """Strip references to opencode's `list` tool, which neither target has."""
    # This paragraph is byte-identical across all four analyst files, but it
    # is an analyst-pillar convention, not a repository-wide one — its absence
    # elsewhere is not an error, it just means nothing needs rewriting here.
    if TOOL_DISCIPLINE_SRC in body:
        body = body.replace(TOOL_DISCIPLINE_SRC, TOOL_DISCIPLINE_OMP)
    body = body.replace(INLINE_LIST_SRC, INLINE_LIST_OMP)

    if "`list`" in body:
        raise TranslationError(
            f"{source}: prompt still names a `list` tool after rewriting; "
            "neither harness has such a tool — add a rewrite rule for the new wording"
        )
    return body


def read_agent(source: Path, *, skills: set[str]) -> tuple[dict, str, dict, str, list[str]]:
    """Parse one opencode agent file into the signals both emitters read.

    `skills` is the slug set of this agent's own pillar, discovered once in
    `build()`: the resolution gate below checks every named skill against it
    rather than re-globbing the skill tree per agent.
    """
    meta, body = split_frontmatter(source.read_text(encoding="utf-8"), source)
    pillar = source.parent.parent.name

    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        raise TranslationError(f"{source}: missing `description` (the harness would skip this file)")

    mode = meta.get("mode")
    if mode not in ("primary", "subagent"):
        raise TranslationError(f"{source}: unrecognised mode {mode!r}")

    permission = meta.get("permission") or {}
    if not isinstance(permission, dict):
        raise TranslationError(f"{source}: `permission` is not a mapping")

    # One `metadata.acordia` schema across both pillars. The pillar is read off
    # the path rather than trusted from the file, so a source copied into the
    # wrong pillar — which would ship under the wrong plugin and inherit the
    # wrong posture — fails here instead of installing.
    metadata = meta.get("metadata")
    acordia = metadata.get("acordia") if isinstance(metadata, dict) else None
    if not isinstance(acordia, dict):
        raise TranslationError(
            f"{source}: `metadata.acordia` is missing or not a mapping; every agent "
            "must declare `pillar` and `role` there"
        )
    if acordia.get("pillar") != pillar:
        raise TranslationError(
            f"{source}: `metadata.acordia.pillar` is {acordia.get('pillar')!r} but the "
            f"file lives in {pillar}/agents — the declared pillar must match the source tree"
        )
    role = acordia.get("role")
    if role not in ACORDIA_ROLES:
        raise TranslationError(
            f"{source}: `metadata.acordia.role` is {role!r}; expected one of "
            + ", ".join(f"`{name}`" for name in ACORDIA_ROLES)
        )
    if (role == "orchestrator") != (mode == "primary"):
        raise TranslationError(
            f"{source}: `mode: {mode}` and `metadata.acordia.role: {role}` disagree — "
            "the orchestrator is the primary agent and every specialist is a subagent"
        )
    if "leg" in acordia:
        raise TranslationError(
            f"{source}: `metadata.acordia.leg` is a removed key — the agent's identity is "
            "its filename and its standing is `role`; delete `leg` from this source"
        )

    spawns = allowed_spawns(permission_entry(permission, "task"))
    if mode == "primary" and not spawns:
        raise TranslationError(f"{source}: primary agent names no dispatchable agents")

    if write_posture(permission_entry(permission, "edit")) == "allowed":
        check_bash_denies(permission_entry(permission, "bash"), source)

    body = rewrite_body(body, source)

    # Not consumed downstream — parsed so a broken `(deep)` heading fails the
    # build, which is what the operator roster spec relies on.
    deep_skills(body, source)

    # A prompt that names a skill the pillar does not ship is a dead pointer:
    # both harnesses resolve skills by slug, so the agent is told to reach for
    # something no install contains.
    for slug in named_skills(body):
        if slug not in skills:
            raise TranslationError(
                f"{source}: names skill `{slug}`, which has no "
                f"{pillar}/skills/{slug}/SKILL.md in its own pillar"
            )

    return meta, body, permission, mode, spawns


# The contract below is not this gate's invention: `analyst-skill-library`
# states it (opencode frontmatter contract, slug-equals-name) and
# `operator-skill-library` states the rest (frontmatter reduction, signing
# triple removed). Both were stated and never executed, which is how a skill
# with unparseable YAML reached both committed plugin trees. `--check` cannot
# catch that: it compares staged bytes against committed bytes, so a defect
# present in both compares equal. Only parsing the source finds it.
SKILL_NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SKILL_KEYS = {"name", "description", "metadata"}
SKILL_SIGNING_KEYS = ("sha256", "signature", "signed_by")


def read_skill(source: Path) -> dict:
    """Validate one skill's frontmatter; raise rather than package a broken file."""
    meta, _ = split_frontmatter(source.read_text(encoding="utf-8"), source)

    name = meta.get("name")
    if not isinstance(name, str) or not SKILL_NAME_RE.match(name) or len(name) > 64:
        raise TranslationError(
            f"{source}: `name` must be kebab-case and at most 64 characters, got {name!r}"
        )
    if name != source.parent.name:
        raise TranslationError(
            f"{source}: `name` {name!r} does not match its folder slug "
            f"{source.parent.name!r} — the harness discovers by folder and binds by name"
        )

    description = meta.get("description")
    if not isinstance(description, str) or not 1 <= len(description) <= 1024:
        length = len(description) if isinstance(description, str) else repr(description)
        raise TranslationError(
            f"{source}: `description` must be 1–1024 characters, got {length} "
            "(both harnesses select skills by description match)"
        )

    signing = [key for key in SKILL_SIGNING_KEYS if key in meta]
    if signing:
        raise TranslationError(
            f"{source}: frontmatter carries {', '.join(signing)} — a stale hash makes "
            "CyberStrike drop the skill as tampered while the other harnesses ignore it"
        )

    unknown = sorted(set(meta) - SKILL_KEYS)
    if unknown:
        raise TranslationError(
            f"{source}: unknown frontmatter key(s) {', '.join(unknown)}; "
            "the contract allows only `name`, `description`, and `metadata`"
        )

    return meta


def translate(source: Path, *, plugin: str, skills: set[str]) -> str:
    """Emit the omp task-agent form of one opencode agent file."""
    meta, body, permission, mode, spawns = read_agent(source, skills=skills)

    tools = list(BASE_TOOLS)
    edit_posture = write_posture(permission_entry(permission, "edit"))
    # One semantics for a path-scoped exception, shared with the Claude
    # emitter: `write` but not `edit`. The scoped posture exists so the two
    # reporting analysts can produce their reports, and withholding the write
    # tool from omp while Claude Code kept it meant the identical source posture
    # yielded opposite capability per harness.
    if edit_posture == "allowed":
        tools += ["edit", "write"]
    elif edit_posture == "scoped":
        tools.append("write")

    if permission_entry(permission, "browser") == "allow":
        tools.append("browser")

    if spawns:
        # omp reads delegation off `spawns`; `task` must be in the allowlist for
        # the tool to exist at all.
        tools.append("task")

    tools.append("yield")

    # Verified against omp 17.1.8: omitting `write` from the allowlist does not
    # remove it. `read` and `write` are omp's XDEV_TRANSPORT_TOOLS — the channel
    # every `xd://` device is driven through — so they are present whenever
    # `tools.xdev` is on, which is the default. `edit` and `task` ARE removed by
    # omission; `write` is the one hole, and it is stamped here rather than
    # papered over.
    if edit_posture == "allowed":
        write_note = (
            "source granted write access; the allowlist carries `edit` and `write`"
        )
    elif edit_posture == "scoped":
        write_note = (
            "source scopes `edit` to `.acordia/reports/**` as a report sink; the "
            "allowlist carries `write` (not `edit`) so the agent can produce those "
            "reports, and the sink itself is a prompt-level convention no harness "
            "enforces — `bash: allow` is an open write channel at any path"
        )
    else:
        write_note = (
            "source granted no write access; omp still exposes `write` as an "
            "`xd://` transport tool while `tools.xdev` is on, so read-only is "
            "prompt-level for writes and enforced only for `edit`"
        )

    out: dict = {
        "name": source.stem,
        "description": meta["description"],
        "color": agent_color(meta),
        "tools": tools,
    }
    if spawns:
        out["spawns"] = spawns

    metadata = dict(meta.get("metadata") or {})
    metadata["generated"] = {
        "by": "tools/build-plugins.py",
        "from": repo_relative(source),
        "harness": "omp",
        "plugin": plugin,
        "write_access": write_note,
    }
    if has_bash_denies(permission_entry(permission, "bash")):
        metadata["generated"]["bash_denies"] = (
            "omp has no per-command bash equivalent; the source's per-pattern "
            "denies are prompt-level guardrails under omp, not enforced ones"
        )
    out["metadata"] = metadata

    frontmatter = yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=10**6)
    header = (
        "# Generated from the opencode source named in `metadata.generated.from`.\n"
        "# Do not edit — edit the source and rebuild with tools/build-plugins.py.\n"
    )
    return f"{FRONTMATTER_FENCE}\n{header}{frontmatter}{FRONTMATTER_FENCE}\n{body}"


def translate_claude(source: Path, *, skills: set[str]) -> str:
    """Emit the Claude Code plugin-agent form of one opencode agent file.

    Claude Code plugin agents accept a fixed, short key set — `hooks`,
    `mcpServers`, `permissionMode`, and `metadata` are silently ignored for
    security — so the provenance that omp carries in `metadata.generated` is
    emitted as YAML comments instead.

    The posture is expressed as `disallowedTools`, not `tools`: an allowlist
    would have to enumerate Claude's whole tool vocabulary and would silently
    strip tools this repository never audited (`Skill`, `NotebookEdit`,
    `WebFetch`), whereas a denylist expresses exactly what the source
    `permission` map encodes and nothing more.
    """
    meta, body, permission, mode, spawns = read_agent(source, skills=skills)

    edit_posture = write_posture(permission_entry(permission, "edit"))
    disallowed: list[str] = []
    if edit_posture == "denied":
        disallowed += ["Edit", "Write", "NotebookEdit"]
    elif edit_posture == "scoped":
        # The source declares `.acordia/reports/**` as a report sink. That sink is a
        # prompt-level convention no harness enforces — `bash: allow` is an open
        # write channel everywhere — and denying `Write` outright would leave the
        # reporting agents unable to produce the reports their prompts require.
        # Grant `Write`, record the convention.
        disallowed += ["Edit", "NotebookEdit"]
    if not spawns:
        disallowed.append("Task")

    notes = [
        f"# Generated from {repo_relative(source)} by tools/build-plugins.py. Do not edit.",
    ]
    if spawns:
        notes.append(
            "# Claude Code plugin agents cannot express a spawn allowlist; the prompt names the\n"
            "# agents this one dispatches."
        )
    if edit_posture == "scoped":
        notes.append(
            "# Source declares `.acordia/reports/**` as its report sink. That sink is a\n"
            "# prompt-level convention no harness enforces: `bash` is an open write channel."
        )
    if permission_entry(permission, "browser") == "allow":
        notes.append(
            "# Source granted the `browser` tool; Claude Code plugin agents cannot add a tool\n"
            "# the harness does not ship, so browser-driven steps in the prompt fall back to\n"
            "# scripted HTTP here. omp carries the tool."
        )
    if has_bash_denies(permission_entry(permission, "bash")):
        notes.append(
            "# Source denied specific bash patterns; Claude Code plugin agents cannot express\n"
            "# per-command bash rules, so those denies are prompt-level here."
        )

    out: dict = {
        "name": source.stem,
        "description": meta["description"],
        "color": agent_color(meta),
    }
    if disallowed:
        out["disallowedTools"] = ", ".join(disallowed)

    frontmatter = yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=10**6)
    header = "\n".join(notes) + "\n"
    return f"{FRONTMATTER_FENCE}\n{header}{frontmatter}{FRONTMATTER_FENCE}\n{body}"


def command_agent(wrapper: Path, body: str) -> str:
    match = COMMAND_AGENT_RE.search(body)
    if not match:
        raise TranslationError(
            f"{wrapper}: body names no agent — a wrapper must open by dispatching "
            "or handing the brief to an agent, so the plugin it belongs to can be resolved"
        )
    return match.group(1)


def render_command(wrapper: Path) -> tuple[str, str]:
    """Return `(agent name, rewritten wrapper)` for one command source.

    The handle is now `<plugin>:<file stem>`, prefixed by the harness itself, so
    a frontmatter `name` would fight the prefix and is dropped. `category` is
    not a key in either plugin schema and is dropped too. Everything else —
    `description`, `argument-hint`, any trailing alias comment, and the whole
    body with its `$ARGUMENTS` placeholder — is preserved verbatim.
    """
    text = wrapper.read_text(encoding="utf-8")
    meta, body = split_frontmatter(text, wrapper)

    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        raise TranslationError(f"{wrapper}: missing `description`")

    raw = text[len(FRONTMATTER_FENCE) + 1 : text.find("\n" + FRONTMATTER_FENCE + "\n", len(FRONTMATTER_FENCE)) + 1]
    comments = [line for line in raw.splitlines() if line.lstrip().startswith("#")]

    out: dict = {"description": description}
    hint = meta.get("argument-hint")
    if hint is not None:
        out["argument-hint"] = hint

    frontmatter = yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=10**6)
    if comments:
        frontmatter += "\n".join(comments) + "\n"
    return command_agent(wrapper, body), f"{FRONTMATTER_FENCE}\n{frontmatter}{FRONTMATTER_FENCE}\n{body}"


def plugin_manifest(name: str) -> str:
    spec = PLUGINS[name]
    manifest = {
        "name": name,
        "version": VERSION,
        "description": spec["description"],
        "author": OWNER,
        "repository": REPOSITORY,
        "keywords": spec["keywords"],
    }
    return json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"


def marketplace(harness: str) -> str:
    catalog = {
        "name": MARKETPLACE_NAME,
        "owner": OWNER,
        "metadata": {
            "description": "ACORDIA analysis and operations agents, skills, and commands."
        },
        "plugins": [
            {
                "name": name,
                "source": f"./plugins/{harness}/{name}",
                "version": VERSION,
                "description": spec["description"],
                "category": spec["category"],
                "keywords": spec["keywords"],
            }
            for name, spec in PLUGINS.items()
        ],
    }
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def build(repo_root: Path, dest_root: Path) -> None:
    """Materialise every generated artifact under `dest_root`."""
    agent_owner: dict[str, str] = {}

    for plugin, spec in PLUGINS.items():
        pillar = repo_root / spec["pillar"]
        agents = sorted((pillar / "agents").glob("*.md"))
        if not agents:
            raise TranslationError(f"{pillar}/agents: no agent files found")

        # Parsed, not merely copied. Runs before anything is written for this
        # pillar so a malformed skill cannot reach a staged tree, let alone the
        # committed one.
        skills = sorted((pillar / "skills").glob("*/SKILL.md"))
        if not skills:
            raise TranslationError(f"{pillar}/skills: no skill files found")
        for source in skills:
            read_skill(source)
        # Handed to `read_agent()` so every skill an agent prompt names is
        # resolved against the pillar that actually ships it, without the
        # per-agent reglob a helper-side lookup would cost.
        skill_slugs = {source.parent.name for source in skills}

        for harness in HARNESSES:
            root = dest_root / "plugins" / harness / plugin
            (root / "agents").mkdir(parents=True, exist_ok=True)
            (root / ".claude-plugin").mkdir(parents=True, exist_ok=True)
            # Claude Code requires the manifest; omp reads a plugin manifest
            # only to resolve a version and otherwise falls back to the source
            # SHA, so shipping it in both trees is harmless and pins the
            # version. No `commands`/`agents`/`skills` path keys: the defaults
            # are exactly what both trees use, and Claude Code's overrides
            # supplement rather than replace, so a redundant entry risks
            # double-loading.
            (root / ".claude-plugin" / "plugin.json").write_text(
                plugin_manifest(plugin), encoding="utf-8"
            )

            for source in agents:
                rendered = (
                    translate(source, plugin=plugin, skills=skill_slugs)
                    if harness == "omp"
                    else translate_claude(source, skills=skill_slugs)
                )
                (root / "agents" / source.name).write_text(rendered, encoding="utf-8")

            # Skills are valid unchanged in Claude Code, omp, and opencode —
            # `name` + `description` frontmatter only — so both trees get a
            # verbatim copy, `references/` subdirectories included.
            shutil.copytree(pillar / "skills", root / "skills")

        for source in agents:
            agent_owner[source.stem] = plugin

    wrappers = sorted((repo_root / "commands" / "acordia").glob("*.md"))
    if not wrappers:
        raise TranslationError("commands/acordia: no command wrappers found")
    for wrapper in wrappers:
        agent, rendered = render_command(wrapper)
        plugin = agent_owner.get(agent)
        if plugin is None:
            raise TranslationError(
                f"{wrapper}: names agent `{agent}`, which belongs to no pillar"
            )
        for harness in HARNESSES:
            # Flat, never nested: omp's plugin command provider scans
            # `<plugin-root>/commands/*.md` non-recursively, so a subdirectory
            # would be invisible to omp. The namespace comes from the plugin
            # name in both harnesses.
            dest = dest_root / "plugins" / harness / plugin / "commands"
            dest.mkdir(parents=True, exist_ok=True)
            (dest / wrapper.name).write_text(rendered, encoding="utf-8")

    # The other half of the bijection `acordia-command-namespace` mandates:
    # every agent must have a canonical wrapper whose stem is its own. The loop
    # above enforces the forward direction — a wrapper naming a live agent —
    # and nothing enforced this one, so adding an agent could silently ship a
    # roster with no handle for it.
    stems = {wrapper.stem for wrapper in wrappers}
    missing = sorted(set(agent_owner) - stems)
    if missing:
        raise TranslationError(
            "commands/acordia: no canonical wrapper for "
            + ", ".join(f"`{name}`" for name in missing)
            + " — every agent needs one wrapper named for it"
        )

    # omp prefers `.omp-plugin/` and falls back to `.claude-plugin/` only when
    # the former is absent, so shipping both catalogs is the documented way to
    # hand each harness its own tree from one checkout.
    for dirname, harness in ((".claude-plugin", "claude"), (".omp-plugin", "omp")):
        catalog_dir = dest_root / dirname
        catalog_dir.mkdir(parents=True, exist_ok=True)
        (catalog_dir / "marketplace.json").write_text(marketplace(harness), encoding="utf-8")


GENERATED_PATHS = ("plugins", ".claude-plugin", ".omp-plugin")

# The drift gate is about generator correctness, not about macOS: a Finder
# artifact in a generated tree is not output this script ever claimed to own.
IGNORED_FILENAMES = {".DS_Store"}


def relative_files(root: Path) -> set[Path]:
    files: set[Path] = set()
    for top in GENERATED_PATHS:
        base = root / top
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.name in IGNORED_FILENAMES:
                continue
            if path.is_file():
                files.add(path.relative_to(root))
    return files


# The version guards what actually reaches an installed user: the generated
# trees. Gating on the sources (`analysts/`, `operators/`, `commands/acordia/`)
# would miss a generator change that alters output without touching a source
# file, and the drift comparison does not backstop that — it compares built
# bytes against committed bytes, and both carry the new output once the author
# rebuilds. A generator refactor that produces identical output leaves these
# paths untouched and correctly demands no bump.
VERSIONED_SOURCES = GENERATED_PATHS

# Tried in order. `develop` is the integration branch; `origin/HEAD` points at
# `main`. The base is a merge base rather than HEAD so the obligation is one
# bump per release, not one per commit.
BASE_REFS = ("origin/develop", "origin/main", "develop", "main")


def git_output(repo_root: Path, *args: str) -> str | None:
    """Run one git command, or return None if git cannot answer."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            encoding="utf-8",
            errors="replace",
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout


def semver(text: str) -> tuple[int, int, int] | None:
    """Parse a strict MAJOR.MINOR.PATCH. Compared as integers: "2.10.0" sorts
    above "2.9.0" numerically and below it lexicographically."""
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", text.strip())
    return tuple(int(part) for part in match.groups()) if match else None


def base_version(repo_root: Path, base: str) -> tuple[int, int, int] | None:
    """The VERSION declared in this file as of `base`."""
    blob = git_output(repo_root, "show", f"{base}:tools/build-plugins.py")
    if blob is None:
        return None
    match = re.search(r'^VERSION = "([^"]+)"', blob, re.M)
    return semver(match.group(1)) if match else None


def version_gate(repo_root: Path) -> list[str]:
    """Refuse a generated-output change that carries no version bump.

    Absence of evidence never fails: no git, no base branch, or an unparseable
    version skips the gate. A missed bump is a silent no-op the next release
    corrects, while a wedged `--check` costs trust in every gate it carries.
    """
    tip = base = None
    for ref in BASE_REFS:
        if git_output(repo_root, "rev-parse", "--verify", "--quiet", ref) is None:
            continue
        merge_base = git_output(repo_root, "merge-base", "HEAD", ref)
        if merge_base and merge_base.strip():
            tip, base = ref, merge_base.strip()
            break

    if base is None:
        print("build-plugins: version gate skipped (no comparison base)", file=sys.stderr)
        return []

    # Diff the generated surface against the merge base — everything this branch
    # changed — and add files git has never been told about, so a new skill's
    # freshly generated output is not invisible to `git diff`.
    changed = git_output(repo_root, "diff", "--name-only", base, "--", *VERSIONED_SOURCES)
    if changed is None:
        print("build-plugins: version gate skipped (git could not diff)", file=sys.stderr)
        return []
    untracked = git_output(
        repo_root, "ls-files", "--others", "--exclude-standard", "--", *VERSIONED_SOURCES
    )

    sources = sorted(
        {line for line in (changed + "\n" + (untracked or "")).splitlines() if line.strip()}
    )
    if not sources:
        return []

    # The obligation is relative to what is already published, so read the base
    # version from the integration branch's tip, not the fork point: two
    # branches forking at the same version must not both ship it, and a branch
    # that later merges the integration branch must not regress below it.
    was = base_version(repo_root, tip)
    now = semver(VERSION)
    if was is None or now is None:
        print("build-plugins: version gate skipped (unparseable version)", file=sys.stderr)
        return []

    if now > was:
        return []

    def dotted(parts: tuple[int, int, int]) -> str:
        return ".".join(str(part) for part in parts)

    problems = [
        f"  generated output changed but VERSION did not move past {tip} "
        f"({dotted(was)} -> {dotted(now)}):"
    ]
    problems += [f"    {path}" for path in sources]
    problems.append("  bump VERSION in tools/build-plugins.py and rebuild")
    return problems


def check(repo_root: Path) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        build(repo_root, staged)

        want = relative_files(staged)
        have = relative_files(repo_root)

        problems: list[str] = []
        for path in sorted(want - have):
            problems.append(f"  missing:  {path}")
        for path in sorted(have - want):
            problems.append(f"  extra:    {path}")
        for path in sorted(want & have):
            if not filecmp.cmp(staged / path, repo_root / path, shallow=False):
                problems.append(f"  differs:  {path}")

    version_problems = version_gate(repo_root)

    if problems:
        print("build-plugins: committed tree does not match the generator", file=sys.stderr)
        print("\n".join(problems), file=sys.stderr)
        print("run tools/build-plugins.py and commit the result", file=sys.stderr)
    if version_problems:
        print("build-plugins: the version bump obligation is unmet", file=sys.stderr)
        print("\n".join(version_problems), file=sys.stderr)
    if problems or version_problems:
        return 1
    return 0


# `--doctor` reports what `--check` structurally cannot see. `--check` compares
# built bytes against committed bytes; none of the failures below leave a trace
# there — an install frozen on an old version, a native file shadowing the
# plugin copy, a prompt the harness will truncate, a skill nothing points at.
INSTALL_REGISTRIES = (
    ("omp", Path.home() / ".omp" / "plugins" / "installed_plugins.json"),
    ("claude", Path.home() / ".claude" / "plugins" / "installed_plugins.json"),
)

# omp resolves an agent or skill name against the user's own `~/.omp/agent/`
# tree before it reaches plugin roots, first wins. A copy there does not
# conflict loudly — it silently freezes that user on whatever it contains.
OMP_NATIVE_AGENTS = Path.home() / ".omp" / "agent" / "agents"
OMP_NATIVE_SKILLS = Path.home() / ".omp" / "agent" / "skills"

# 10k characters is the ceiling omp's own agent-authoring guidance states; the
# warning threshold is where a prompt stops being read as a whole.
DOCTOR_PROMPT_CEILING = 10_000
DOCTOR_PROMPT_WARN = 6_000

# Both harnesses select a skill by matching its description, so two descriptions
# that read alike make the choice between them arbitrary.
DOCTOR_DESCRIPTION_OVERLAP = 0.30
DOCTOR_STOPWORDS = frozenset(
    "a an and are as at be but by can for from has have how in into is it its more not of on "
    "one or other over than that the their them then there these they this to use used using "
    "was what when where which while who why will with you your".split()
)

# Duplication between a prompt and a skill it names is command-level, not
# line-level: the prompt re-types the skill's commands inside backticks, in its
# own prose and its own table cells, so no line comparison — normalised or not
# — sees any of it. The unit is therefore the backticked code span. 12
# characters is long enough to be a command rather than a flag or a filename.
CODE_SPAN_RE = re.compile(r"`([^`\n]{12,})`")
DOCTOR_SPAN_MIN = 12


def pillar_inventory(repo_root: Path) -> dict[str, dict]:
    """Read every source fact the doctor sections share, once.

    Deliberately separate from `build()`: the doctor reads the sources without
    translating them, so a prompt that would fail a build gate still gets
    reported on rather than aborting the whole report.
    """
    inventory: dict[str, dict] = {}
    for spec in PLUGINS.values():
        base = repo_root / spec["pillar"]
        agents: dict[str, dict] = {}
        for source in sorted((base / "agents").glob("*.md")):
            _, body = split_frontmatter(source.read_text(encoding="utf-8"), source)
            agents[source.stem] = {"body": body, "skills": named_skills(body)}
        skills: dict[str, dict] = {}
        for source in sorted((base / "skills").glob("*/SKILL.md")):
            meta, body = split_frontmatter(source.read_text(encoding="utf-8"), source)
            description = meta.get("description")
            skills[source.parent.name] = {
                "description": description if isinstance(description, str) else "",
                "body": body,
            }
        inventory[spec["pillar"]] = {"agents": agents, "skills": skills}
    return inventory


def installed_versions(registry: Path) -> dict[str, list[str]] | None:
    """ACORDIA plugin -> the version recorded for each install scope.

    None means the registry is absent or unreadable, which is the normal state
    of a harness the user never installed into — not a finding.
    """
    try:
        data = json.loads(registry.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    plugins = data.get("plugins")
    if not isinstance(plugins, dict):
        return None
    versions: dict[str, list[str]] = {}
    for key, entries in plugins.items():
        # The registry key is `<plugin>@<marketplace>`.
        name = key.split("@", 1)[0]
        if name not in PLUGINS or not isinstance(entries, list):
            continue
        versions.setdefault(name, []).extend(
            str(entry.get("version")) for entry in entries if isinstance(entry, dict)
        )
    return versions


def doctor_install_state() -> tuple[list[str], int]:
    lines: list[str] = []
    findings = 0
    installed: set[str] = set()
    for harness, registry in INSTALL_REGISTRIES:
        versions = installed_versions(registry)
        if versions is None:
            lines.append(f"  {harness}: no readable registry at {registry} — nothing installed here")
            continue
        if not versions:
            lines.append(f"  {harness}: registry present, no acordia plugin installed")
            continue
        for name in sorted(versions):
            installed.add(name)
            for version in sorted(set(versions[name])):
                if version == VERSION:
                    lines.append(f"  {harness}: {name} {version} — current")
                else:
                    findings += 1
                    lines.append(
                        f"  {harness}: {name} {version} — SKEW, this tree builds {VERSION}"
                    )
    for name in sorted(set(PLUGINS) - installed):
        findings += 1
        lines.append(f"  {name}: installed in neither registry — this pillar is running nowhere")
    return lines, findings


def directory_names(base: Path) -> set[str]:
    """Every entry name and stem in `base`, broken symlinks included.

    omp resolves the name, not the target, so a dangling symlink shadows just
    as effectively as a real file.
    """
    try:
        entries = list(base.iterdir())
    except OSError:
        return set()
    names: set[str] = set()
    for entry in entries:
        names.add(entry.name)
        names.add(entry.stem)
    return names


def doctor_shadowing(inventory: dict[str, dict]) -> tuple[list[str], int]:
    native_agents = directory_names(OMP_NATIVE_AGENTS)
    native_skills = directory_names(OMP_NATIVE_SKILLS)

    lines: list[str] = []
    for pillar, data in inventory.items():
        for name in sorted(data["agents"]):
            if name in native_agents:
                lines.append(
                    f"  {OMP_NATIVE_AGENTS}/{name}.md shadows the {pillar} agent `{name}` — "
                    "omp loads the native copy and never reads the plugin one"
                )
        for slug in sorted(data["skills"]):
            if slug in native_skills:
                lines.append(
                    f"  {OMP_NATIVE_SKILLS}/{slug} shadows the {pillar} skill `{slug}` — "
                    "omp loads the native copy and never reads the plugin one"
                )
    findings = len(lines)
    if not findings:
        lines.append("  none: no ACORDIA agent or skill name exists under ~/.omp/agent/")
    return lines, findings


def doctor_prompt_size(inventory: dict[str, dict]) -> list[str]:
    rows: list[tuple[int, str]] = []
    for pillar, data in inventory.items():
        for name, agent in data["agents"].items():
            size = len(agent["body"])
            if size > DOCTOR_PROMPT_CEILING:
                flag = "OVER CEILING"
            elif size > DOCTOR_PROMPT_WARN:
                flag = "warn"
            else:
                flag = "ok"
            rows.append((size, f"  {size:>6} chars  {flag:<12}  {pillar}/{name}"))
    return [row for _, row in sorted(rows, reverse=True)]


def doctor_orphan_skills(inventory: dict[str, dict]) -> list[str]:
    lines: list[str] = []
    for pillar, data in inventory.items():
        named = {slug for agent in data["agents"].values() for slug in agent["skills"]}
        orphans = sorted(set(data["skills"]) - named)
        lines.append(
            f"  {pillar}: {len(orphans)} of {len(data['skills'])} skills named on no agent skill line"
        )
        lines += [f"    {slug}" for slug in orphans]
    lines.append(
        "  informational: a skill may be reached from prose or by description match instead"
    )
    return lines


def content_words(text: str) -> set[str]:
    """Description words that carry meaning, for the overlap score below."""
    return {
        word
        for word in re.findall(r"[a-z0-9]+", text.lower())
        if len(word) > 2 and word not in DOCTOR_STOPWORDS
    }


def doctor_description_proximity(inventory: dict[str, dict]) -> list[str]:
    lines: list[str] = []
    for pillar, data in inventory.items():
        words = {slug: content_words(skill["description"]) for slug, skill in data["skills"].items()}
        pairs: list[tuple[float, str, str]] = []
        for left, right in itertools.combinations(sorted(words), 2):
            union = words[left] | words[right]
            if not union:
                continue
            score = len(words[left] & words[right]) / len(union)
            if score >= DOCTOR_DESCRIPTION_OVERLAP:
                pairs.append((score, left, right))
        lines.append(
            f"  {pillar}: {len(pairs)} description pair(s) at Jaccard >= "
            f"{DOCTOR_DESCRIPTION_OVERLAP:.2f}"
        )
        lines += [
            f"    {score:.2f}  {left} <-> {right}" for score, left, right in sorted(pairs, reverse=True)
        ]
    return lines


def code_spans(text: str) -> set[str]:
    """Normalised backticked spans: the command-level unit both sides restate."""
    spans: set[str] = set()
    for raw in CODE_SPAN_RE.findall(text):
        span = " ".join(raw.split()).lower()
        if len(span) >= DOCTOR_SPAN_MIN:
            spans.add(span)
    return spans


def technique_spans(spans: set[str], vocabulary: set[str]) -> set[str]:
    """Drop the spans that are repository vocabulary rather than technique.

    A prompt naming a skill or a sibling agent in backticks, or pointing at
    `.acordia/reports/`, is doing its job — and the skill it names says the same
    words, so an unfiltered count makes the four analysts read as duplicators
    on nothing but their own cross-references.
    """
    return {
        span
        for span in spans
        if span not in vocabulary
        and not (" " not in span and (span.startswith((".", "/")) or span.endswith("/")))
    }


def doctor_duplication(inventory: dict[str, dict]) -> list[str]:
    # A high count means the prompt restates a skill it already names — the
    # prompt is carrying content the skill owns. The inverse is the other
    # finding and this metric cannot show it: commands a prompt carries that
    # appear in NO skill it names are a gap in the skill library, so a low
    # ratio is not a clean bill of health.
    vocabulary = {
        name.lower()
        for data in inventory.values()
        for group in ("agents", "skills")
        for name in data[group]
    }

    lines: list[str] = []
    for pillar, data in inventory.items():
        skill_spans = {slug: code_spans(skill["body"]) for slug, skill in data["skills"].items()}
        for name, agent in sorted(data["agents"].items()):
            # The denominator is every span the prompt carries; the excluded
            # ones simply cannot score, and saying how many were set aside keeps
            # the ratio readable against a hand count of the same file.
            carried = code_spans(agent["body"])
            spans = technique_spans(carried, vocabulary)
            owners: dict[str, int] = {}
            hits: set[str] = set()
            for slug in agent["skills"]:
                shared = spans & skill_spans.get(slug, set())
                if shared:
                    owners[slug] = len(shared)
                    hits |= shared
            excluded = len(carried) - len(spans)
            aside = f" ({excluded} vocabulary/path span(s) excluded from matching)" if excluded else ""
            lines.append(
                f"  {pillar}/{name}: {len(hits)} of {len(carried)} code spans also appear "
                f"in a skill it names{aside}"
            )
            worst = sorted(owners.items(), key=lambda item: (-item[1], item[0]))[:3]
            lines += [f"    {count:>4} restated from {slug}" for slug, count in worst]
    lines.append(
        "  informational: a high count means the prompt restates a skill it names; commands "
        "the prompt carries that appear in no named skill are the opposite finding, a gap in "
        "the skill library, which this metric cannot show"
    )
    return lines


def doctor(repo_root: Path, *, strict: bool) -> int:
    """Report the failures `--check` is blind to, and never gate on content.

    Only the install-state and shadowing sections can fail a `--strict` run.
    Sections 3-6 describe content the redesign phase owns; making them fatal
    would wedge every build until work that has not started is finished.
    """
    inventory = pillar_inventory(repo_root)

    install_lines, install_findings = doctor_install_state()
    shadow_lines, shadow_findings = doctor_shadowing(inventory)

    for title, lines in (
        (f"1. install-state skew (this tree builds {VERSION})", install_lines),
        ("2. native shadowing of plugin agents and skills", shadow_lines),
        ("3. prompt size", doctor_prompt_size(inventory)),
        ("4. orphan skills", doctor_orphan_skills(inventory)),
        ("5. description proximity", doctor_description_proximity(inventory)),
        (
            "6. prompt/skill duplication (command-level: backticked code spans, not prose "
            "lines — a low score is not an absence of restated prose)",
            doctor_duplication(inventory),
        ),
    ):
        print(f"\n{title}")
        print("\n".join(lines))

    findings = install_findings + shadow_findings
    print(f"\ninstall-state and shadowing findings: {findings}")
    if findings and strict:
        print("build-plugins: --doctor --strict fails on an install-state finding", file=sys.stderr)
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="build to a tempdir and diff against the committed tree without "
        "writing anything; exit non-zero on any drift",
    )
    parser.add_argument(
        "--doctor",
        action="store_true",
        help="report install-state skew, native shadowing, and prompt hygiene without "
        "building anything; exits 0 because it is a report, not a gate",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="with --doctor, exit non-zero on an install-state or shadowing finding",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    try:
        if args.check:
            return check(repo_root)
        if args.doctor:
            return doctor(repo_root, strict=args.strict)

        # Build into a tempdir first, then swap. A failed build must not leave
        # the committed tree deleted or half-written — it is the artifact a
        # marketplace install clones, so a partial one is worse than a stale
        # one. The swap also wipes each generated path wholesale, so a renamed
        # skill, agent, or wrapper cannot leave an orphan behind.
        with tempfile.TemporaryDirectory(dir=repo_root) as tmp:
            staged = Path(tmp)
            build(repo_root, staged)
            for top in GENERATED_PATHS:
                shutil.rmtree(repo_root / top, ignore_errors=True)
                shutil.move(str(staged / top), str(repo_root / top))
    except TranslationError as err:
        print(f"build-plugins: {err}", file=sys.stderr)
        return 1

    for plugin in PLUGINS:
        for harness in HARNESSES:
            root = repo_root / "plugins" / harness / plugin
            print(
                f"  built {harness}/{plugin}: "
                f"{len(list((root / 'agents').glob('*.md')))} agents, "
                f"{len(list((root / 'skills').iterdir()))} skills, "
                f"{len(list((root / 'commands').glob('*.md')))} commands"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
