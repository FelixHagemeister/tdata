#!/usr/bin/env python3
"""Download all sources to the local data/ cache."""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from tobacco_gateway import fetch


def main():
    results = fetch("*")
    ok, failed = [], []
    for source_id, result in results.items():
        if isinstance(result, Exception):
            failed.append((source_id, result))
        else:
            ok.append(source_id)

    print(f"\n{'='*60}")
    print(f"Fetched successfully ({len(ok)}): {', '.join(ok) or 'none'}")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for sid, exc in failed:
            print(f"  {sid}: {exc}")
    print("="*60)


if __name__ == "__main__":
    main()
