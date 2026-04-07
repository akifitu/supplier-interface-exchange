"""Load supplier interface data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


SupplierRecord = Dict[str, Any]


def load_suppliers(data_file: Path | str) -> List[SupplierRecord]:
    """Load supplier interface records from JSON."""
    return json.loads(Path(data_file).read_text(encoding="utf-8"))
