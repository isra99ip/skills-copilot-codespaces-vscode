"""Ejecuta el smoketest de backtest de BetIntel AI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from betintel.smoke import run_smoke_backtest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ejecuta el smoketest de backtest.")
    parser.add_argument(
        "--output",
        type=Path,
        help="Ruta opcional para guardar el resumen JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = run_smoke_backtest(args.output)
    print(json.dumps(summary.to_dict(), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
