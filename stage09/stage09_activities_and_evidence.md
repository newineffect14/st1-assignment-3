# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group 5, Thursday 2:30
Members and responsibilities: James Nguyen – queries, service listing, console menu and tests; Lemuel Legaspi – PR review and Stage 8 section L; Joshua Sisourath – README update and UI-01/UI-02 demo evidence
Stage 8 integrated SHA, command, working directory and actual result: af2da4a1e7ef7e9bd06028d2d9fd197472705ca6 – `python3 -m pytest -q` in project/ – 16 passed

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain | FR-01, BR-01 – patients must be registered and found by unique ID |
| Appointment history | Required session/domain | FR-07, BR-07 – cancelled appointments stay retrievable this session |
| Temporary menu choice | Transient | Only decides which console command runs; not a business record |
| Practitioner specialty | Required session/domain | FR-03 – required field when registering a practitioner |
| Debug print output | Transient | Diagnostic only; not a requirement and not stored |
| Appointment status | Required session/domain | FR-06, BR-08 – SCHEDULED/CANCELLED/COMPLETED controls cancellation and filtering |

What is intentionally lost on exit? All patients, practitioners and appointments. Data only lasts for the current session because FR-10 persistence is retired.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | appointment: Appointment | tuple[datetime, str] | Returns the ordering key only; no validation, no side effects | date_time (minute precision) and unique appointment_id |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus or None | New list[Appointment] | Pure filter and sort using the named key; assumes valid inputs; no store, input/output or mutation | practitioner.practitioner_id, AppointmentStatus enum |
| Service listing | practitioner_id: str, status: AppointmentStatus or None | New list[Appointment] | Blank ID → ValueError, unknown practitioner → LookupError, non-enum status → ValueError; gets data_store.list_appointments() then calls the query with the registered ID | Store find returns None for unknown; service raises LookupError |
| Console | User text input | Printed messages | Parses text and dates, converts status text to enum, calls services, shows ValueError/LookupError and returns to menu; no domain rules | parse_date_time, format_appointment, existing services |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: IDs are trimmed, non-blank, case-sensitive strings unique per entity. Names and specialty are required non-blank text. An appointment holds the actual registered Patient and Practitioner objects, a naive minute-precision date_time and an AppointmentStatus. No new fields are added.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain object does user interaction | Confirmation belongs in the console; cancel() should only guard the status change so it stays testable |
| Service prints/reads the menu | Service mixes presentation with workflow | Menu belongs in console.py; services must be testable without a UI (NFR-02) |
| Query sorts its source in place | appointments.sort() changes the caller's list, so the query is not pure | Use sorted() to return a new list and leave the source unchanged (FP-01) |
| Store prints Appointment saved | Store does output instead of returning data | Store should return the object so callers and tests can check it; printing is the console's job |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: `.sort()` reorders the original list in place and returns None. `sorted()` leaves the original untouched and returns a new list. Check: take `before = list(appointments)`, run the query, then `assert appointments == before` (same order and objects) and `assert result is not appointments`. Same length alone doesn't prove nothing changed.

Score-example prediction and explanation of passing the named key: Result is [('Chen', 5), ('Ali', 8), ('Bea', 8)]. Chen has the lowest score; Ali and Bea tie on 8 so name breaks the tie. `key=score_key` passes the function itself so sorted() can call it on each item. Writing `score_key()` would call it once immediately and fail.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancelling changes the same object's status to CANCELLED instead of deleting it, so history is kept (FR-07, BR-07). Checks: find_appointment returns the same object with CANCELLED status; listing with no status includes it; listing with SCHEDULED leaves it out because it is no longer scheduled.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: The pure query trusts its inputs; validation happens in the service so the query stays simple and reusable. The service uses the registered practitioner's ID so input with surrounding spaces still matches. The console converts status text to the enum so services only accept AppointmentStatus or None.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| FP-03 | One appointment | appointment_sort_key (queries.py) | Returns (date_time, appointment_id) | TEST-Q01 |
| QRY-01 | Appointments for D1 and D2 | select_appointments (queries.py) | Only D1's appointments returned | TEST-Q02 |
| QRY-02 | Mixed statuses | select_appointments | None = all statuses; enum filters; no match = [] | TEST-Q03, TEST-Q04 |
| QRY-03 | Same-time appointments | select_appointments with named key | Ordered by time then ID; source order unchanged | TEST-Q05, TEST-Q06 |
| FP-02 | Empty, sorted and unsorted lists | select_appointments | Always a new list, same objects unchanged | TEST-Q07 |
| QRY-04 | Unknown ID, blank ID, 'scheduled' string | AppointmentService.list_practitioner_appointments | LookupError / ValueError / ValueError; known with no matches = [] | TEST-W01–W04 |
| FR-07 / AC-05.2 | Cancelled A1 | Service find and listing | Same object, CANCELLED, still listed | TEST-W05 |
| UI-01 / UI-02 | Menu input | console.run_menu | All commands work; errors recover with no partial changes | Manual demo + TEST-W06 |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: Empty: a known practitioner with no matches returns a new empty list. Unknown: a valid but unregistered practitioner ID raises LookupError. Invalid: a blank ID or a non-enum status like 'scheduled' raises ValueError. The console converts status text to AppointmentStatus before calling the service. Results contain the actual stored Appointment objects, not copies. The console catches ValueError and LookupError, shows the message and returns to the menu. Failed operations leave stored records unchanged.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| FP-03 / TEST-Q01 | queries.py `appointment_sort_key` | Key equals `(date_time, appointment_id)` | Pass | project/tests/test_queries.py::test_sort_key_returns_date_time_then_id |
| QRY-01 / TEST-Q02 | queries.py `select_appointments` | Only D1 returned; D2 appointment is the control | Pass | test_queries.py::test_only_requested_practitioner_is_selected |
| QRY-02 / TEST-Q03 | queries.py `select_appointments` | Default None keeps scheduled, cancelled and completed | Pass | test_queries.py::test_default_status_includes_every_status |
| QRY-02 / TEST-Q04 | queries.py `select_appointments` | Each enum filters correctly; no match returns `[]` | Pass | test_queries.py::test_explicit_status_filter_and_no_match |
| QRY-03 / TEST-Q05 | queries.py, named key | A1 and A2 share 09:00 so ID breaks the tie; result equals sort by named key | Pass | test_queries.py::test_orders_by_time_then_id_tie_break |
| FP-01 / TEST-Q06 | queries.py | Source order and fields unchanged; repeated call gives same result | Pass | test_queries.py::test_source_unchanged_and_repeatable |
| FP-02 / TEST-Q07 | queries.py | New list for empty, unsorted and already-sorted input; same objects inside | Pass | test_queries.py::test_returns_new_list_for_empty_sorted_and_unsorted |
| QRY-04 / TEST-W01 | services.py `list_practitioner_appointments` | Known practitioner with no matches returns `[]` | Pass | project/tests/test_workflows.py::test_known_practitioner_without_appointments_returns_empty |
| QRY-04 / TEST-W02 | services.py | Valid unknown ID raises LookupError | Pass | test_workflows.py::test_unknown_practitioner_raises_lookup_error |
| QRY-04 / TEST-W03 | services.py | Blank ID raises ValueError | Pass | test_workflows.py::test_blank_practitioner_id_raises_value_error |
| QRY-04 / TEST-W04 | services.py | Text `'scheduled'` raises ValueError, not an empty list | Pass | test_workflows.py::test_text_status_raises_value_error |
| FR-07, AC-05.2 / TEST-W05 | services.py | Cancelled A1 is the same object, still listed with all statuses, excluded from SCHEDULED | Pass | test_workflows.py::test_conflict_cancel_history_and_freed_slot_workflow |
| QRY-04 / TEST-W06 | services.py | `'  D1  '` uses the registered ID and finds A1 | Pass | test_workflows.py::test_listing_uses_registered_practitioner_id |

Full suite: `python3 -m pytest -q` in project/ – 31 passed at `bf7b2f6`.

Purity explanation from code inspection, including absence of hidden state and I/O: `select_appointments` only uses its three arguments. It builds a new local list, never calls `.sort()` on the input, never changes an appointment, has no print or input, and does not import the store or services. `appointment_sort_key` only reads two fields and returns a tuple.

What the tests do and do not establish: The tests show the right appointments are selected and ordered, the source list is unchanged and repeated calls match for the cases tested. They do not prove purity for every possible input; that also relies on reading the code for hidden state and side effects.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Register P1, D1 and D2; book A1; reject conflicting A9; book A2; cancel A1; retrieve and filter appointments; book A3 into the freed slot. | Valid bookings succeed, double-booking is rejected, cancelled history remains accessible, and the freed slot can be reused. | Passed. A9 was rejected, A2 was booked with D2, A1 remained cancelled, and A3 was booked successfully. The final listing showed both A1 (cancelled) and A3 (scheduled). | `test_workflows.py::test_console_ui01_demonstration` |
| UI-02 invalid-input recovery | Invalid menu option, blank/unknown patient IDs, duplicate registration, invalid bookings, repeated cancellation and invalid status filter. | Invalid inputs display errors without crashing or incorrectly changing stored records. | Passed. Unknown option 9, blank and unknown patient IDs, duplicate P1, unknown-patient booking, impossible date 2026-13-01, repeated cancellation and invalid status 'bogus' each printed an Error and the menu continued. Lookups of A5 and A6 then failed, showing neither failed booking was stored, and P1 was still Alex Example. TEST-W08 automates this sequence (31 passed). | `test_workflows.py::test_console_ui02_recovers_from_invalid_input` |
| Automated service workflow | TEST-W05: booking conflict, cancellation, history retention and freed-slot reuse. | Service rejects conflicts, retains cancelled appointments and allows reuse of cancelled slots. | Passed in the automated regression suite (31 tests passed, 0 failed). | `test_workflows.py::test_conflict_cancel_history_and_freed_slot_workflow` |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: Sections A and B committed at `c1757ee` before Copilot was used.
Actual prompt/context supplied: Handout prompt plus queries.py, services.py, console.py and test_queries.py – see [copilot_review.md](copilot_review.md).
Actual response: Copied in full in [copilot_review.md](copilot_review.md). Copilot Chat, Ask mode, at `f3cc6f4`.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Critical/Important: none found | Observed evidence matched our own reading of queries.py, services.py and console.py | – | Accept as an observation, but we checked it against the tests ourselves rather than trusting it | No change | 31 passed |
| EOF during a field prompt is not handled | console.py `input()` calls inside each option | Optional | Reject – a keyboard user cannot trigger this; not in UI-02; fields are read before any service call so no partial write | No change | Read console.py: no service call happens before all fields are read |
| Conflict rule can be bypassed by direct store insertion | data_store.py `add_appointment`, services.py `book_appointment` | Optional | Reject – over-engineering; conflict checking belongs in the service and the store contract is unchanged since Stage 8 | No change | TEST-W05 and Stage 8 regressions still pass through the service |
| Query helper does not reject invalid status | queries.py `select_appointments` | Optional | Reject – handout says the pure helper assumes valid filter values; the service validates | No change | TEST-W04 shows the service rejects `'scheduled'` |
| UI-02 test does not check the malformed-date booking was not stored | test_workflows.py UI-02 test | Optional | Accept – a fair gap in our no-partial-state evidence | Added `'7', 'A6'` lookup and raised the error count to 10 (`bf7b2f6`) | 31 passed after the change |

Responsibility check: Domain objects validate their own fields and Appointment owns the cancel rule. The store only holds and finds records. Services coordinate lookups, conflicts and validated listing. The pure query only filters and sorts what it is given. The console only reads input, converts text, calls services and prints results.

## F. Required reflections

**1. Architectural concern**

One important concern was making sure validation happened in the correct part of the system. The console converts user input into the correct format, while the service checks the practitioner and appointment status. This keeps the query functions simple and separates responsibilities.

**2. Copilot suggestion**

Copilot suggested moving the booking conflict check into the data store. We decided not to use this because conflict checking already belongs in the service layer. Moving it would add unnecessary complexity without improving the current design.

**3. Cancelled appointment history**

We verified this by cancelling A1 and checking that it could still be retrieved with its cancelled status. The appointment also appeared when listing all appointments for D1 but was excluded when filtering for scheduled appointments. This was checked through both automated tests and the interactive menu.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It only uses the arguments passed in, builds a new local list and returns a sorted copy, with no printing, input, store access or changes to the original list. Calling appointments.sort() on the input, printing results or reading a global store would make it impure.
2. Which explicit inputs are needed, and why avoid a global store? It needs the appointment list, the practitioner ID and an optional status filter. If it read a hidden global store instead, the result would depend on outside state, so the same call could give different answers and would be harder to test.
3. How can a new list reuse Appointment objects safely? The function returns a new list container, but it holds the same Appointment objects instead of copies. This is safe because the query only reads them and never changes them, which TEST-Q06 and TEST-Q07 check.
4. Why use a named key, and what breaks equal-time ties? appointment_sort_key returns (date_time, appointment_id), so the sort rule lives in one place that can be reused and tested directly (TEST-Q01). When two appointments are at the same time, the appointment ID decides the order, so results are always consistent (TEST-Q05).
5. How do default and explicit status filters differ? With the default of None, every status is returned, including cancelled and completed appointments. Passing a specific AppointmentStatus returns only that status, and if nothing matches the result is an empty list (TEST-Q03, TEST-Q04).
6. How do empty, unknown practitioner and invalid filter cases differ? A known practitioner with no matching appointments gives an empty list, which is a normal result (TEST-W01). An unknown but valid ID raises LookupError (TEST-W02), while a blank ID or a text status like 'scheduled' raises ValueError (TEST-W03, TEST-W04).
7. Which console errors recover, and how is unchanged state checked? The menu catches ValueError and LookupError, prints "Error: ..." and keeps running, covering unknown options, blank or unknown IDs, duplicates, bad dates, invalid statuses and cancelling twice. TEST-W08 then looks the records up afterwards to confirm A5 and A6 were never stored and P1 was not overwritten.
8. What is data integrity for registered participants, conflicts and history? Appointments link to the actual registered Patient and Practitioner objects, not loose IDs or copies. A practitioner can't be double-booked at the same time, and cancelled appointments stay stored with status CANCELLED so the history isn't lost.
9. What is Copilot's review role, and who verifies findings? Copilot acted as a reviewer, and we treated its suggestions as ideas to check, not as facts. Our group checked each finding against the code and tests and decided what to do, and we accepted 1 of the 4 findings (section E and stage09/copilot_review.md).
10. How do pure functions and OOP responsibilities work together? The objects keep their own rules (for example, Appointment handles cancelling), the services coordinate the workflow, the pure query only filters and sorts, and the console only handles input and output. This means the menu never decides business rules, so each part is easier to test on its own.

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.