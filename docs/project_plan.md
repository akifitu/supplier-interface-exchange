# Step-By-Step Plan

## Phase 1: Define supplier exchange scope

1. Choose which supplier interfaces matter.
2. Define lifecycle states and delivery gates.
3. Decide which documents must be tracked.

## Phase 2: Build the source dataset

1. Create one record per supplier-facing interface.
2. Capture protocol, owning repo, and delivery gate.
3. Record required document sets.

## Phase 3: Implement the exchange audit

1. Validate statuses and required fields.
2. Roll up delivery-gate coverage.
3. Export supplier and gate-level reports.

## Phase 4: Debug and verify

1. Add tests for invalid statuses and missing documents.
2. Check gate counts against the source data.
3. Fix formatting or validation gaps.

## Phase 5: Publish professionally

1. Write clear supplier-facing docs.
2. Commit generated outputs.
3. Push publicly and keep CI green.

## To-Do

- [x] define the supplier interface schema
- [x] create a realistic exchange dataset
- [x] implement validation and exporter logic
- [x] add regression tests
- [ ] publish the repository
