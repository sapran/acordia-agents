#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml>=6"]
# ///
"""Translate opencode agent files into omp task-agent files.

The opencode files under `<pillar>/agents/` are the source of truth for both
harnesses. omp will not load them: it discovers task agents only from
`.omp/agents` and `~/.omp/agent/agents`, and its frontmatter contract differs
(a required `name`, a `tools` allowlist instead of a `permission` map, no
modes, no path-scoped permissions). This script performs that translation.

Output is build artifact. Never edit it; regenerate it.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

# Tools every analyst gets. `edit`/`write` are absent by design: that is the
# translation of opencode's `edit: deny`. omp appends `yield` itself when a
# `tools` list is present; naming it keeps the generated file honest.
BASE_TOOLS = ["read", "grep", "glob", "bash", "web_search", "todo", "yield"]

# opencode's `list` tool has no omp counterpart — in omp a directory path
# handed to `read` enumerates it. This paragraph is byte-identical across all
# four analyst files, so an exact match is a safe contract; a miss means the
# prompts changed shape and the translation must be revisited rather than
# quietly shipping a prompt that names a nonexistent tool.
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

DEEP_HEADINGS = ("## Your defining spine (deep)", "## Your specialist depth (deep)")

FRONTMATTER_FENCE = "---"


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
    meta = yaml.safe_load(raw)
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


def has_scoped_write(entry) -> bool:
    """True when `permission.edit` denies globally but allows some path."""
    if not isinstance(entry, dict):
        return False
    return any(name != "*" and verdict == "allow" for name, verdict in entry.items())


def deep_skills(body: str, source: Path) -> list[str]:
    for line in iter_heading_values(body, DEEP_HEADINGS):
        return [part.strip() for part in line.split("·") if part.strip()]
    raise TranslationError(f"{source}: no `(deep)` skill heading found for autoload")


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


def translate(source: Path, *, autoload: str) -> str:
    meta, body = split_frontmatter(source.read_text(encoding="utf-8"), source)

    name = source.stem
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        raise TranslationError(f"{source}: missing `description` (omp would skip this file)")

    mode = meta.get("mode")
    if mode not in ("primary", "subagent"):
        raise TranslationError(f"{source}: unrecognised mode {mode!r}")

    permission = meta.get("permission") or {}
    if not isinstance(permission, dict):
        raise TranslationError(f"{source}: `permission` is not a mapping")

    tools = list(BASE_TOOLS)
    spawns = allowed_spawns(permission_entry(permission, "task"))

    if mode == "primary":
        if not spawns:
            raise TranslationError(f"{source}: primary agent names no dispatchable agents")
        # omp reads delegation off `spawns`; `task` must be in the allowlist for
        # the tool to exist at all.
        tools.insert(tools.index("yield"), "task")

    scoped_write = has_scoped_write(permission_entry(permission, "edit"))

    if TOOL_DISCIPLINE_SRC not in body:
        raise TranslationError(
            f"{source}: expected Tool-discipline paragraph not found; "
            "the prompt changed shape and the omp rewrite must be revisited"
        )
    body = body.replace(TOOL_DISCIPLINE_SRC, TOOL_DISCIPLINE_OMP)
    body = body.replace(INLINE_LIST_SRC, INLINE_LIST_OMP)

    if "`list`" in body:
        raise TranslationError(
            f"{source}: prompt still names a `list` tool after rewriting; "
            "omp has no such tool — add a rewrite rule for the new wording"
        )

    # Verified against omp 17.1.8: omitting `write` from the allowlist does not
    # remove it. `read` and `write` are omp's XDEV_TRANSPORT_TOOLS — the channel
    # every `xd://` device is driven through — so they are present whenever
    # `tools.xdev` is on, which is the default. `edit` and `task` ARE removed by
    # omission; `write` is the one hole, and it is stamped here rather than
    # papered over.
    if scoped_write:
        write_note = (
            "source scoped writes to `.acordia/reports/**`; omp cannot express a "
            "path-scoped permission and cannot deny `write` at all while "
            "`tools.xdev` is on, so this agent can write anywhere"
        )
    else:
        write_note = (
            "source granted no write access; omp still exposes `write` as an "
            "`xd://` transport tool while `tools.xdev` is on, so read-only is "
            "prompt-level for writes and enforced only for `edit`"
        )

    out: dict = {"name": name, "description": description, "tools": tools}
    if spawns and mode == "primary":
        out["spawns"] = spawns
    if autoload == "deep":
        out["autoloadSkills"] = deep_skills(body, source)

    metadata = dict(meta.get("metadata") or {})
    metadata["generated"] = {
        "by": "tools/translate-omp.py",
        "from": repo_relative(source),
        "harness": "omp",
        "write_access": write_note,
    }
    out["metadata"] = metadata

    frontmatter = yaml.safe_dump(out, sort_keys=False, allow_unicode=True, width=10**6)
    header = (
        "# Generated from the opencode source named in `metadata.generated.from`.\n"
        "# Do not edit — edit the source and reinstall.\n"
    )
    return f"{FRONTMATTER_FENCE}\n{header}{frontmatter}{FRONTMATTER_FENCE}\n{body}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", nargs="+", type=Path, help="opencode agent .md files")
    parser.add_argument("--out", required=True, type=Path, help="output directory")
    parser.add_argument(
        "--autoload",
        choices=("none", "deep"),
        default="none",
        help="inject the prompt's `(deep)` skill bodies at subagent start",
    )
    args = parser.parse_args()

    translated: list[tuple[Path, str]] = []
    for source in args.sources:
        try:
            translated.append((args.out / source.name, translate(source, autoload=args.autoload)))
        except TranslationError as err:
            print(f"translate-omp: {err}", file=sys.stderr)
            return 1

    args.out.mkdir(parents=True, exist_ok=True)
    for path, content in translated:
        path.write_text(content, encoding="utf-8")
        print(f"  translated: {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
