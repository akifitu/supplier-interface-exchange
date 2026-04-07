"""CLI for the supplier exchange."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .analysis import analyze_suppliers
from .data import load_suppliers
from .export import export_reports


def build_parser() -> argparse.ArgumentParser:
    """Build the command line parser."""
    parser = argparse.ArgumentParser(
        prog="supplier-interface-exchange",
        description="Validate and export supplier interface exchange artifacts.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    audit_parser = subparsers.add_parser("audit", help="Analyze supplier records and export reports.")
    audit_parser.add_argument("--data-file", default="data/suppliers.json", help="Path to the supplier JSON file.")
    audit_parser.add_argument("--export-dir", help="Directory where reports should be written.")
    return parser


def run(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return an exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "audit":
        result = analyze_suppliers(load_suppliers(Path(args.data_file)))
        _print_summary(result)
        if args.export_dir:
            export_reports(result, Path(args.export_dir))
            print(f"Reports exported to: {args.export_dir}")
        return 1 if result.errors else 0

    parser.error("Unknown command.")
    return 2


def _print_summary(result) -> None:
    summary = result.summary
    print("Supplier exchange summary")
    print(f"  Suppliers: {summary['supplier_count']}")
    print(f"  Interfaces: {summary['interface_count']}")
    print(f"  Validated interfaces: {summary['validated_count']}")
    print(f"  Owning repositories: {summary['owning_repo_count']}")
    print(f"  Delivery gates: {summary['delivery_gate_count']}")
    print(f"  Errors: {summary['error_count']}")
    print(f"  Warnings: {summary['warning_count']}")
    if result.errors:
        print("Validation errors:")
        for item in result.errors:
            print(f"  - {item}")
    if result.warnings:
        print("Validation warnings:")
        for item in result.warnings:
            print(f"  - {item}")


if __name__ == "__main__":
    raise SystemExit(run())
