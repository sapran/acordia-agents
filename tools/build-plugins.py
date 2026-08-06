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
"""

from __future__ import annotations

import argparse
import filecmp
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
VERSION = "2.4.0"
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
# derived from the `metadata.acordia` block each source already declares —
# analysts name the orchestrator in `leg`, operators in `role` — rather than
# from a filename table, which would be a second source of the same fact.
ORCHESTRATOR_COLOR = "cyan"
SPECIALIST_COLOR = "blue"

DEEP_HEADINGS = ("## Your defining spine (deep)", "## Your specialist depth (deep)")

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

    The analyst pillar declares the distinction in `metadata.acordia.leg`, the
    operators pillar in `metadata.acordia.role`; either naming `orchestrator`
    is the primary. Anything else — including a source with no `acordia` block
    at all — is a specialist.
    """
    metadata = meta.get("metadata")
    acordia = metadata.get("acordia") if isinstance(metadata, dict) else None
    if not isinstance(acordia, dict):
        return SPECIALIST_COLOR
    if "orchestrator" in (acordia.get("leg"), acordia.get("role")):
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


def read_agent(source: Path) -> tuple[dict, str, dict, str, list[str]]:
    """Parse one opencode agent file into the signals both emitters read."""
    meta, body = split_frontmatter(source.read_text(encoding="utf-8"), source)

    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        raise TranslationError(f"{source}: missing `description` (the harness would skip this file)")

    mode = meta.get("mode")
    if mode not in ("primary", "subagent"):
        raise TranslationError(f"{source}: unrecognised mode {mode!r}")

    permission = meta.get("permission") or {}
    if not isinstance(permission, dict):
        raise TranslationError(f"{source}: `permission` is not a mapping")

    spawns = allowed_spawns(permission_entry(permission, "task"))
    if mode == "primary" and not spawns:
        raise TranslationError(f"{source}: primary agent names no dispatchable agents")

    body = rewrite_body(body, source)

    # Not consumed downstream — parsed so a broken `(deep)` heading fails the
    # build, which is what the operator roster spec relies on.
    deep_skills(body, source)

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
        length = len(description) if isinstance(description, str) else "absent"
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


def translate(source: Path, *, plugin: str) -> str:
    """Emit the omp task-agent form of one opencode agent file."""
    meta, body, permission, mode, spawns = read_agent(source)

    tools = list(BASE_TOOLS)
    edit_posture = write_posture(permission_entry(permission, "edit"))
    # A path-scoped exception still denies by default ("*": deny) — that
    # default is what the source author reaches for to keep an agent
    # read-only-by-default, so only an outright `allow` earns the tool. The
    # exception is still surfaced honestly in `write_note` below.
    if edit_posture == "allowed":
        tools += ["edit", "write"]

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
            "source declares `.acordia/reports/**` as its report sink; that sink is a "
            "prompt-level convention no harness enforces — every analyst carries "
            "`bash: allow`, an open write channel at any path — and omp additionally "
            "cannot deny `write` while `tools.xdev` is on, so this agent can write anywhere"
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


def translate_claude(source: Path) -> str:
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
    meta, body, permission, mode, spawns = read_agent(source)

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
                    translate(source, plugin=plugin)
                    if harness == "omp"
                    else translate_claude(source)
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


def relative_files(root: Path) -> set[Path]:
    files: set[Path] = set()
    for top in GENERATED_PATHS:
        base = root / top
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                files.add(path.relative_to(root))
    return files


# Paths whose contents reach an installed user. `tools/` is excluded on
# purpose: changing the generator without changing its output reaches nobody,
# and when it does change output, the drift comparison below catches it
# independently. `docs/` and `openspec/` reach no installed user at all.
VERSIONED_SOURCES = ("analysts", "operators", "commands/acordia")

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
            text=True,
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
    """Refuse a source change that carries no version bump.

    Absence of evidence never fails: no git, no base branch, or an unparseable
    version skips the gate. A missed bump is a silent no-op the next release
    corrects, while a wedged `--check` costs trust in every gate it carries.
    """
    base = None
    for ref in BASE_REFS:
        if git_output(repo_root, "rev-parse", "--verify", "--quiet", ref) is None:
            continue
        merge_base = git_output(repo_root, "merge-base", "HEAD", ref)
        if merge_base and merge_base.strip():
            base = merge_base.strip()
            break

    if base is None:
        print("build-plugins: version gate skipped (no comparison base)", file=sys.stderr)
        return []

    changed = git_output(repo_root, "diff", "--name-only", base, "--", *VERSIONED_SOURCES)
    if changed is None:
        print("build-plugins: version gate skipped (git could not diff)", file=sys.stderr)
        return []

    sources = [line for line in changed.splitlines() if line.strip()]
    if not sources:
        return []

    was = base_version(repo_root, base)
    now = semver(VERSION)
    if was is None or now is None:
        print("build-plugins: version gate skipped (unparseable version)", file=sys.stderr)
        return []

    if now > was:
        return []

    def dotted(parts: tuple[int, int, int]) -> str:
        return ".".join(str(part) for part in parts)

    problems = [
        f"  source changed since {base[:9]} but VERSION did not move "
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="build to a tempdir and diff against the committed tree without "
        "writing anything; exit non-zero on any drift",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    try:
        if args.check:
            return check(repo_root)

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
