# Supplier Interface Exchange

`Supplier Interface Exchange` is a systems engineering portfolio repository for supplier-facing interface coordination. It tracks external delivery interfaces, exchange protocols, readiness gates, and required documents in one structured workspace.

## What This Repo Demonstrates

- supplier interface governance
- external ICD and delivery management
- structured review of interface readiness
- automation, tests, and reviewer-friendly exports

## Repository Map

```text
.
|-- data/                               # Supplier interface records
|-- docs/                               # Build plan and exchange notes
|-- reports/                            # Generated summaries and dashboards
|-- src/supplier_interface_exchange/    # Validation, analysis, export, and CLI logic
|-- tests/                              # Regression tests
|-- .github/workflows/                  # CI pipeline
|-- Makefile                            # Common commands
`-- README.md
```

## Quick Start

```bash
make test
make audit
```

Or run the CLI directly:

```bash
PYTHONPATH=src python3 -m supplier_interface_exchange.cli audit --data-file data/suppliers.json --export-dir reports
```

## Generated Outputs

- `reports/supplier-summary.md`
- `reports/supplier-register.csv`
- `reports/delivery-gates.csv`
- `reports/supplier-dashboard.html`

## Documentation

- [docs/README.md](docs/README.md)
- [docs/project_plan.md](docs/project_plan.md)
- [docs/exchange_notes.md](docs/exchange_notes.md)
