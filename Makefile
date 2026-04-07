PYTHON ?= python3

.PHONY: test audit

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

audit:
	PYTHONPATH=src $(PYTHON) -m supplier_interface_exchange.cli audit --data-file data/suppliers.json --export-dir reports
