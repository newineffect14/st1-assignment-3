# Stage 9 GitHub Copilot review record

Tool: GitHub Copilot Chat in VS Code, Ask mode (read-only review; no edits applied by Copilot).
Reviewer: James Nguyen, 2026-11-04, branch `feature/stage9-queries` at `f3cc6f4`.
Human design (record sections A and B) was committed first at `c1757ee`.

## Prompt supplied

```
Act as a query and console integration reviewer for SmartCare.
Review the supplied code and tests for:
1. explicit inputs, purity and source non-mutation;
2. domain, service, data-store and console responsibilities;
3. validation and recovery without partial state changes;
4. correct object identity, enum filtering and ordering;
5. retained history and integrity risks;
6. missing query, workflow and console tests.
Do not redesign the domain or add storage/frameworks.
Do not invent fields or requirements or delete cancelled history.
Separate observed evidence from optional improvements.
Rank findings as Critical, Important or Optional.
For each finding, identify the code/test evidence to check.

#file:project/smartcare/queries.py #file:project/smartcare/services.py #file:project/smartcare/console.py #file:project/tests/test_queries.py
```

## Copilot response (copied as received)

**Critical:** None found.

**Important:** None confirmed in the service-driven query and console workflows reviewed.

**Observed Evidence**
- `select_appointments` receives its inputs explicitly, filters into a new list, and sorts that list without modifying appointments or the source. The query tests cover repeatability, source order and fields, ordering, and object identity in `queries.py` and `test_queries.py`.
- The service validates status values and resolves the practitioner through the store before querying. The store returns a new list containing its stored appointment objects; cancellation changes the existing object's status and retains it. The workflow tests cover filtering, ordering, cancellation history, and rebooking in `services.py`, `data_store.py`, and `test_workflows.py`.
- The console parses date and status input, delegates registration and booking to services, and catches expected `ValueError` and `LookupError` exceptions. The workflow tests exercise successful listing and recovery from invalid input in `console.py` and `test_workflows.py`.

**Optional**
- **Console EOF during a prompt is not handled.** EOF is caught when reading the menu choice, but not while reading fields for an operation. Incomplete scripted input can therefore raise `EOFError` and terminate the console. Check the `input()` calls in `console.py` and add a focused test if graceful mid-prompt EOF is expected. Registration and booking gather their fields before calling the service, so this path does not appear to cause partial writes.
- **The practitioner-conflict rule can be bypassed by direct store insertion.** `AppointmentService.book_appointment` checks for a conflict, while `SmartCareDataStore.add_appointment` checks identity and duplicate IDs but not scheduling conflicts. This is a risk only if callers are expected to use the store directly for booking; the current tests use the service. Check the call sites and intended store boundary in `services.py`, `data_store.py`, and `test_regressions.py`.
- **Direct query-helper calls do not reject invalid status values.** The service rejects text statuses, but `select_appointments` itself compares status by enum identity, so an invalid value can simply produce no matches. That is consistent with the helper's annotated input if it is internal; if it is intended as a public boundary, consider a direct-helper test or validation. Check `queries.py`, `services.py`, and `test_queries.py`.
- **Console assertions could verify invalid-booking state more directly.** The recovery test checks that an appointment with an unknown patient is subsequently not found, but it does not explicitly check that the malformed-date booking was not stored. Add a follow-up lookup assertion for that case if the test is intended to prove no partial state changes across console validation paths. Check `test_workflows.py` alongside the parse-before-book sequence in `console.py`.