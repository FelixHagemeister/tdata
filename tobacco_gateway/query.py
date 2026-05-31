from __future__ import annotations
import pathlib
import re
import yaml
from dataclasses import dataclass, field

_ROOT = pathlib.Path(__file__).parent.parent


@dataclass
class SourceMatch:
    source_id: str
    name: str
    score: int
    matched_terms: list[str]
    geographic_level: str
    tobacco_topics: list[str] = field(default_factory=list)
    fetch_script: str = ""


def query(question: str, sources_dir: str | None = None) -> list[SourceMatch]:
    """Return sources ranked by keyword relevance to the question.

    >>> results = query("e-cigarette use trend in Bavaria")
    >>> [r.source_id for r in results[:3]]
    [...]
    """
    sources_path = pathlib.Path(sources_dir) if sources_dir else _ROOT / "sources"
    tokens = _tokenize(question)
    matches = []

    for source_dir in sorted(sources_path.iterdir()):
        if not source_dir.is_dir():
            continue
        md_file = source_dir / "SOURCE.md"
        if not md_file.exists():
            continue
        meta = _parse_frontmatter(md_file)
        if not meta:
            continue
        score, matched = _score(tokens, meta)
        if score > 0:
            matches.append(SourceMatch(
                source_id=meta.get("id", source_dir.name),
                name=meta.get("name", source_dir.name),
                score=score,
                matched_terms=matched,
                geographic_level=meta.get("geographic_level", "unknown"),
                tobacco_topics=meta.get("tobacco_topics", []),
                fetch_script=meta.get("fetch_script", ""),
            ))

    return sorted(matches, key=lambda m: m.score, reverse=True)


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-zäöüß]+", text.lower()) if len(t) >= 3}


def _parse_frontmatter(path: pathlib.Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def _score(tokens: set[str], meta: dict) -> tuple[int, list[str]]:
    parts: list[str] = []
    for key in ("tobacco_topics", "sample_questions", "name", "notes", "population"):
        val = meta.get(key)
        if isinstance(val, list):
            parts.extend(str(v) for v in val)
        elif isinstance(val, str):
            parts.append(val)

    corpus_tokens = _tokenize(" ".join(parts))
    matched = [t for t in tokens if t in corpus_tokens]
    score = len(matched)

    # Geographic bonus — prefer sources closer to the requested area
    geo = meta.get("geographic_level", "")
    geo_tokens = tokens & {"münchen", "munich", "muenchen"}
    if geo_tokens:
        score += 5 if geo == "munich" else (2 if geo == "bavaria" else 0)
    elif tokens & {"bavaria", "bavarian", "bayerisch", "bayern"}:
        score += 3 if geo == "bavaria" else (2 if geo == "munich" else 0)

    return score, matched
