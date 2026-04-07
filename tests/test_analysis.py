"""Regression tests for the supplier exchange."""

from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from supplier_interface_exchange.analysis import analyze_suppliers
from supplier_interface_exchange.cli import run
from supplier_interface_exchange.data import load_suppliers


DATA_FILE = ROOT / "data" / "suppliers.json"


class SupplierExchangeTests(unittest.TestCase):
    def test_clean_dataset_passes(self) -> None:
        result = analyze_suppliers(load_suppliers(DATA_FILE))
        self.assertEqual(result.errors, [])
        self.assertEqual(result.summary["interface_count"], 4)

    def test_invalid_status_is_detected(self) -> None:
        records = load_suppliers(DATA_FILE)
        records[0]["status"] = "late"
        result = analyze_suppliers(records)
        self.assertTrue(any("invalid status" in item for item in result.errors))

    def test_cli_exports_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = run(["audit", "--data-file", str(DATA_FILE), "--export-dir", temp_dir])
            self.assertEqual(exit_code, 0)
            export_dir = Path(temp_dir)
            self.assertTrue((export_dir / "supplier-summary.md").exists())
            self.assertTrue((export_dir / "supplier-register.csv").exists())
            self.assertTrue((export_dir / "delivery-gates.csv").exists())
            self.assertTrue((export_dir / "supplier-dashboard.html").exists())


if __name__ == "__main__":
    unittest.main()
