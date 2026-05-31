from __future__ import annotations
import importlib.util
import pathlib

import pandas as pd

_ROOT = pathlib.Path(__file__).parent.parent


def fetch(source_id: str, cache_dir: str | None = None, **kwargs) -> pd.DataFrame:
    """Fetch data for *source_id* and return a pandas DataFrame.

    Pass ``source_id="*"`` to attempt fetching every source and get back a
    ``dict[str, DataFrame | Exception]``.
    """
    if cache_dir is None:
        cache_dir = str(_ROOT / "data")

    if source_id == "*":
        return _fetch_all(cache_dir, **kwargs)

    fetch_file = _ROOT / "sources" / source_id / "fetch.py"
    if not fetch_file.exists():
        available = sorted(p.name for p in (_ROOT / "sources").iterdir()
                           if (p / "fetch.py").exists())
        raise ValueError(
            f"Unknown source: {source_id!r}.\nAvailable: {available}"
        )

    mod = _load_module(source_id, fetch_file)
    return mod.fetch(cache_dir=cache_dir, **kwargs)


def _fetch_all(cache_dir: str, **kwargs) -> dict[str, pd.DataFrame | Exception]:
    results: dict[str, pd.DataFrame | Exception] = {}
    for source_dir in sorted((_ROOT / "sources").iterdir()):
        if not source_dir.is_dir() or not (source_dir / "fetch.py").exists():
            continue
        try:
            results[source_dir.name] = fetch(source_dir.name, cache_dir=cache_dir, **kwargs)
        except Exception as exc:
            results[source_dir.name] = exc
    return results


def _load_module(source_id: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(f"_tdg_{source_id}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
