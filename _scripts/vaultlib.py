"""Shared helpers for vault maintenance scripts (_scripts/vault-*.py).

Stdlib-only on purpose: must run on Linux and on Windows Git Bash with a bare
Python 3 install. Frontmatter is edited *textually* (only the targeted key is
rewritten) so untouched fields keep their exact formatting.

Policy source: _meta/conventions.md (esp. §1 frontmatter, §3 tags, §5 scripts).
"""

from __future__ import annotations

import re
from pathlib import Path

# Directories under the vault root that hold real notes. The ideas bank lives
# at campaigns/ideas/ (inside campaigns/ so graph view of that folder shows all
# content), so campaigns/ covers everything.
CONTENT_DIRS = ("campaigns",)

# Frontmatter type values in use; a tag equal to one of these is a deprecated
# "type-name tag" and must never be applied (see _meta/conventions.md §3).
TYPE_NAMES = {
    "npc", "character", "location", "plot-hook", "faction", "item", "lore",
    "session", "encounter", "campaign-index", "meta", "index", "plan",
}

WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]\[]+)\]\]")


def vault_root() -> Path:
    """The vault is the parent of the _scripts/ directory this file lives in."""
    return Path(__file__).resolve().parent.parent


def iter_notes(vault: Path, scope: Path | None = None):
    """Yield every content .md note (sorted), optionally restricted to scope."""
    roots = [scope] if scope else [vault / d for d in CONTENT_DIRS]
    for root in roots:
        if not root.is_dir():
            continue
        yield from sorted(p for p in root.rglob("*.md")
                          if p.is_file() and ".obsidian" not in p.parts)


# ---------------------------------------------------------------- frontmatter

def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Split into (frontmatter_inner, rest). rest includes the closing '---\\n'
    onward when frontmatter exists, so `fm_open + fm + rest` reassembles the
    file byte-for-byte. Returns (None, text) when there is no frontmatter."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    return text[4 : end + 1], text[end + 1 :]


def join_frontmatter(fm: str, rest: str) -> str:
    return "---\n" + fm + rest


def _strip_yaml_scalar(raw: str) -> str:
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        raw = raw[1:-1]
    return raw.strip()


def get_list_field(fm: str, key: str) -> list[str] | None:
    """Read a frontmatter field as a list of strings.

    Handles inline (`key: [a, b]`, `key: []`), block lists, and a bare scalar
    (returned as a one-item list). Returns None when the key is absent.
    """
    lines = fm.splitlines()
    for i, line in enumerate(lines):
        m = re.match(rf"^{re.escape(key)}:(.*)$", line)
        if not m:
            continue
        val = m.group(1).strip()
        if val.startswith("["):  # inline list
            inner = val.strip("[]").strip()
            if not inner:
                return []
            return [_strip_yaml_scalar(v) for v in inner.split(",") if v.strip()]
        if val:  # bare scalar
            return [_strip_yaml_scalar(val)]
        items = []
        for nxt in lines[i + 1 :]:
            m2 = re.match(r"^\s+-\s+(.*)$", nxt)
            if m2:
                items.append(_strip_yaml_scalar(m2.group(1)))
            elif nxt.strip() == "":
                continue
            else:
                break
        return items
    return None


def _needs_quotes(value: str) -> bool:
    return bool(re.search(r"[\[\]{}:#&*!|>'\"%@`,]", value)) or value != value.strip()


def format_list_field(key: str, values: list[str]) -> str:
    """Render a list field in vault house style: `key: []` when empty,
    otherwise a block list with wikilink-safe quoting."""
    if not values:
        return f"{key}: []\n"
    out = [f"{key}:"]
    for v in values:
        if _needs_quotes(v):
            v = '"' + v.replace('"', '\\"') + '"'
        out.append(f"  - {v}")
    return "\n".join(out) + "\n"


def set_list_field(fm: str, key: str, values: list[str]) -> str:
    """Return frontmatter with `key` replaced (or inserted) as a list field.
    Only the key's own lines change; everything else is preserved verbatim."""
    rendered = format_list_field(key, values)
    lines = fm.splitlines(keepends=True)
    for i, line in enumerate(lines):
        if re.match(rf"^{re.escape(key)}:", line):
            j = i + 1
            while j < len(lines) and re.match(r"^\s+-\s+", lines[j]):
                j += 1
            return "".join(lines[:i]) + rendered + "".join(lines[j:])
    # Key absent: insert just before `created:` (house field order), else append.
    for i, line in enumerate(lines):
        if re.match(r"^created:", line):
            return "".join(lines[:i]) + rendered + "".join(lines[i:])
    return "".join(lines) + rendered


# ------------------------------------------------------------------ wikilinks

def parse_wikilinks(body: str) -> list[str]:
    """Outbound wikilink target names (no embeds), alias and heading stripped."""
    targets = []
    for m in WIKILINK_RE.finditer(body):
        target = m.group(1).split("|")[0].split("#")[0].strip()
        if target:
            targets.append(target)
    return targets


def build_resolver(notes: list[Path]) -> dict[str, Path]:
    """Map lowercase note name / path stem / alias -> note path, mirroring
    Obsidian's name-based resolution. Later duplicates do not clobber earlier
    ones (ambiguity is /lint's problem, not ours)."""
    resolver: dict[str, Path] = {}

    def claim(name: str, path: Path):
        key = name.lower()
        if key and key not in resolver:
            resolver[key] = path

    for path in notes:
        claim(path.stem, path)
    for path in notes:
        try:
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        except OSError:
            continue
        if fm:
            for alias in get_list_field(fm, "aliases") or []:
                claim(alias, path)
    return resolver


def resolve_link(resolver: dict[str, Path], target: str) -> Path | None:
    """Resolve a wikilink target (possibly path-style) to a note path."""
    hit = resolver.get(target.lower())
    if hit:
        return hit
    return resolver.get(target.rsplit("/", 1)[-1].lower())


# --------------------------------------------------------------- tag registry

def _table_tags(section: str) -> list[str]:
    """First-column backticked tags from markdown table rows in a section."""
    tags = []
    for line in section.splitlines():
        m = re.match(r"^\|\s*`([^`]+)`\s*\|", line)
        if m:
            tags.append(m.group(1))
    return tags


def read_tag_registry(vault: Path) -> dict[str, set[str]]:
    """Parse _meta/tags.md into {'active': ..., 'proposed': ...} tag sets.
    'active' includes the structural campaign/<name> exceptions."""
    text = (vault / "_meta" / "tags.md").read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)
    active, proposed = set(), set()
    for part in parts:
        if part.startswith("Active"):
            active.update(_table_tags(part))
        elif part.startswith("Proposed"):
            proposed.update(_table_tags(part))
    return {"active": active, "proposed": proposed}
