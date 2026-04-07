"""Analysis helpers for supplier exchange."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Mapping, Sequence


VALID_STATUSES = {"planned", "active", "validated"}
REQUIRED_FIELDS = {
    "supplier_id",
    "supplier_name",
    "interface_name",
    "protocol",
    "status",
    "owning_repo",
    "delivery_gate",
    "documents",
}


@dataclass
class ExchangeResult:
    errors: List[str]
    warnings: List[str]
    summary: Dict[str, Any]
    supplier_rows: List[Dict[str, str]]
    gate_rows: List[Dict[str, str]]


def analyze_suppliers(records: Sequence[Mapping[str, Any]]) -> ExchangeResult:
    """Validate supplier interface records and build export rows."""
    errors: List[str] = []
    warnings: List[str] = []
    _check_duplicate_ids(records, errors)

    supplier_rows: List[Dict[str, str]] = []
    gate_rollup: Dict[str, int] = defaultdict(int)

    for record in records:
        if not _validate_record(record, errors):
            continue
        supplier_rows.append(
            {
                "supplier_id": record["supplier_id"],
                "supplier_name": record["supplier_name"],
                "interface_name": record["interface_name"],
                "protocol": record["protocol"],
                "status": record["status"],
                "owning_repo": record["owning_repo"],
                "delivery_gate": record["delivery_gate"],
                "document_count": str(len(record["documents"])),
            }
        )
        gate_rollup[record["delivery_gate"]] += 1
        if len(record["documents"]) < 2:
            warnings.append(f"{record['supplier_id']}: fewer than two supporting documents are listed.")

    gate_rows = [
        {
            "delivery_gate": gate,
            "interface_count": str(count),
        }
        for gate, count in sorted(gate_rollup.items())
    ]

    summary = {
        "supplier_count": len({row["supplier_id"] for row in supplier_rows}),
        "interface_count": len(supplier_rows),
        "validated_count": sum(1 for row in supplier_rows if row["status"] == "validated"),
        "owning_repo_count": len({row["owning_repo"] for row in supplier_rows}),
        "delivery_gate_count": len(gate_rows),
        "error_count": len(errors),
        "warning_count": len(warnings),
    }
    return ExchangeResult(errors, warnings, summary, supplier_rows, gate_rows)


def _check_duplicate_ids(records: Sequence[Mapping[str, Any]], errors: List[str]) -> None:
    seen = set()
    for record in records:
        supplier_id = record.get("supplier_id")
        if supplier_id in seen:
            errors.append(f"duplicate supplier_id '{supplier_id}' detected.")
        seen.add(supplier_id)


def _validate_record(record: Mapping[str, Any], errors: List[str]) -> bool:
    supplier_id = str(record.get("supplier_id", "<missing-supplier>"))
    missing = sorted(field for field in REQUIRED_FIELDS if record.get(field) in ("", None))
    if missing:
        errors.append(f"{supplier_id}: missing required fields: {', '.join(missing)}.")
        return False
    if record["status"] not in VALID_STATUSES:
        errors.append(f"{supplier_id}: invalid status '{record['status']}'.")
    if not isinstance(record["documents"], list) or not record["documents"]:
        errors.append(f"{supplier_id}: documents must contain at least one entry.")
    return True
