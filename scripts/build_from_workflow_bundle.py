#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_report_package import build_package_from_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build report package directly from workflow bundle report-input JSON.")
    parser.add_argument("--workflow-report-input", required=True, help="Path to workflow-generated report-input JSON.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    parser.add_argument("--prefix", default="report", help="Filename prefix.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.workflow_report_input)
    payload = json.loads(input_path.read_text(encoding="utf-8"))
    files = build_package_from_payload(payload, Path(args.output_dir), args.prefix)
    print("generated:")
    for path in files.values():
        print(path)


if __name__ == "__main__":
    main()
