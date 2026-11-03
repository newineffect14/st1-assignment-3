# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Group 5, Thursday 2:30
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

File shorthand (paths relative to `project/`): **R** = `tests/test_regressions.py` (Stage 8, student-authored). Test IDs TEST-R01 to TEST-R03 are in each docstring.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason:

1. **"Appointment disappears after cancellation"**: *symptom*. It describes what a user or tester saw. It doesn't say which call "lost" it (list, store lookup or service lookup) or why.
2. **"The data-store removal path is probably being called"**: *hypothesis*. It is a testable guess about the cause ("probably"). In our project it is weak from the start, because `SmartCareDataStore` has no public delete/remove method. It is tested by checking whether `list_appointments()` still contains the object after cancelling. If it does, nothing was removed.
3. **"The failing test shows store.find_appointment('A1') returns None"**: *evidence*. It is a concrete, repeatable observed value from a real run. It narrows the problem to the store's lookup, not the service.
4. **"The service layer is badly designed"**: *opinion*. It names no specific behaviour, value or check that could prove it wrong, so it can't guide a fix.
5. **"Traceback points to smartcare/services.py line 42"**: *evidence* of **where** the failure was observed, not of why. The cause may be in a method called from that line (for example the store), so it is a starting point for reading the call path.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason (cancelled-history scenario):

- **Expected:** after `cancel_appointment('A1')`, the same object is kept with status CANCELLED. `list_appointments()` still contains it, `store.find_appointment('A1')` returns that object, and `AppointmentService.find_appointment('A1')` returns it rather than raising LookupError. Requirements: FR-06 (guarded cancellation), FR-07 and BR-07 (history retained), AC-05.2 (retained history is protected), FR-08 (lookup).
- **Observed:** [complete from your run. Record the actual first failing assertion of R `test_cancelled_appointment_is_still_found`]
- **Minimal reproduction:** fresh `SmartCareDataStore`; register patient `P1` and practitioner `D1`; book `A1` for `P1`/`D1` at 2026-10-01 09:00; cancel `A1`; then check status, list membership, store lookup and service lookup in that order.
- **Initial hypothesis:** [complete. Your own guess, written before Copilot; keep it even if it turns out wrong]
- **Evidence to inspect:** whether the object is still in `list_appointments()` (this separates "removed" from "not found"); what `store.find_appointment('A1')` returns compared with the service lookup (this separates None from LookupError); and the code of `SmartCareDataStore.find_appointment`, plus `git diff` of the prepared commit.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason:

- **Deletion test:** that is a **test defect**. The test contradicts FR-07, which says cancelled appointments stay as history, so the test should be changed to assert the opposite: the object is retained with CANCELLED status and can still be found. The code should not be changed to delete appointments just to turn that test green. Expected behaviour comes from the requirements, not from whatever a test happens to say.
- **Different practitioners at the same time:** that test does **not** reflect AC-04.2. AC-04.2 allows a different practitioner to be booked at the same time; only the same practitioner at the same time is a conflict (FR-05 / AC-04.1). The test is wrong and should be corrected to expect a successful booking. If the code passed such a test, that would itself be a product defect. We don't invent patient-conflict or duration-overlap rules either.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason:

**Smells and small refactorings**
| Smell | Small behaviour-preserving change |
|---|---|
| Long method (70 lines doing several jobs) | Extract small private helpers, one step at a time, with tests run after each |
| Duplicate magic status strings (`"scheduled"`, `"cancelled"`) | Use the existing `AppointmentStatus` enum members |
| Direct collection manipulation (service edits the store's list or dict) | Go through the existing `SmartCareDataStore` add/find/list methods; the service shouldn't touch store internals |
| Printing inside the service | Remove the prints. Report failures by raising ValueError or LookupError; output belongs in the console layer |
| Validation mixed with workflow | Rely on the domain constructors and the existing ID trimming, rather than repeating checks |
| Four nested conditionals | Use guard clauses (raise early) to flatten the nesting |

**Classification**
| Change | Type | Why |
|---|---|---|
| Rename `appt` to `appointment` | Refactoring | Naming only; behaviour unchanged |
| Extract a repeated conflict helper | Refactoring | Same rule, one place; results unchanged |
| Add rescheduling | Feature | New behaviour not in the current contracts |
| Restore retained cancellation lookup | Repair | Brings back required FR-07/FR-08 behaviour that was broken |
| Replace a magic status string with the existing enum | Refactoring | Same comparison, clearer and typo-proof |

**Behaviour that must remain unchanged:** the same returned objects (identity, not copies); ValueError for invalid values and LookupError for unknown IDs; SCHEDULED → CANCELLED only through `Appointment.cancel`; cancelled appointments retained and findable; same-practitioner/time conflicts rejected without changing the store; different practitioners allowed.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason (based on R `test_cancelled_appointment_is_still_found`; confirm the values against your own run in section G):

- **Assertion:** `AssertionError` at R line 71, `assert data_store.find_appointment('A1') is appointment`.
- **Expected / observed:** expected the booked `Appointment` object; observed [complete: copy the value from your run].
- **Earlier lines in the same test:** [complete: state whether lines 69 (status CANCELLED) and 70 (list still holds the object) passed]
- **Call path:** test → `SmartCareDataStore.find_appointment('A1')` in `smartcare/data_store.py`. The service's `find_appointment` and `cancel_appointment` both call the same store method.
- **Requirement:** FR-07 / BR-07 / AC-05.2 (history retained), FR-08 (lookup).

| Rank | Plausible cause | Discriminating check |
|---|---|---|
| [complete] | `find_appointment` skips appointments by status | Read the method body; book without cancelling and check whether lookup works; check whether line 70 passes |
| [complete] | Cancellation removes the appointment from the store | Check whether `list_appointments()` still holds the object after cancel (line 70) |
| [complete] | The ID is changed or not trimmed the same way during cancel or lookup | Print `appointment.appointment_id` after cancelling; compare it with `'A1'` |

Rank these yourselves after your run, using the evidence you actually see.

**Why a traceback alone isn't enough:** it only shows where the assertion was checked. It doesn't show which earlier decision produced the wrong value. The cause can be in a method called further down, or in code that ran before this line. You need a discriminating check to tell the causes apart.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: The first place you look usually isn't where the cause is, and the test itself may be wrong (see A.3). Editing straight away tends to fix the symptom rather than the cause, can break other behaviour, and makes it hard to tell which change actually mattered. Reproducing the failure, stating the expected behaviour from a requirement and checking a hypothesis first leads to the smallest fix that can be justified, plus a test that keeps the fault from coming back.


Classification responses (1–5, each with reason): see A.1.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: see A.2. [complete observed and hypothesis]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: see A.5. [complete observed values and ranking]

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: `77c8f95baacb6cf2dd2723d3d6ae7ed4b4291fef` (integrated `main` on GitHub at the start of Stage 8) / SmartCare A3 Requirements Baseline 2026, revision 2
- Baseline test command / working directory / observed result / evidence: `python -m pytest -q` / `project/` / 12 passed in 0.08s; `git status --short` empty (Lemuel, 3 Nov 2026) [add each member's matching result]
- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
- Branch and preparer / how teammates obtained this branch: `debug/stage8` / [complete] / `git fetch` then `git switch debug/stage8`
- Downloaded tool version, source SHA256 and --check outcome: [complete: version line printed by the tool, `sha256sum` of prepare_debugging.py, and the CHECK ONLY line]
- --apply and --verify output summaries / artefact references: [complete]
- Bounded diff inspected and recovery location (not committed): [complete: `git diff --stat` showed only `project/smartcare/data_store.py`]; backup in `project/.stage8_faults/` (ignored by .gitignore, not committed)
- Prepared faulty-state commit SHA: [complete]
- Preparation or recovery issues and resolution, if any: [complete or "None"]
- Initial prepared full-suite command / result / key failures: `python -m pytest -q` / `project/` / [complete]

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete from your run]
- Expected behaviour and requirement: booking the same practitioner at the same datetime as an existing SCHEDULED appointment raises ValueError, and the store is unchanged (FR-05 / AC-04.1). A different practitioner at that time is booked successfully (AC-04.2). No patient-conflict or duration-overlap rule.
- Minimal synthetic reproduction steps: fresh store; register `P1`, `P2`, `D1`, `D2`; book `A1` = `P1`/`D1` at 2026-10-01 09:00; book `A2` = `P2`/`D1` at the same time (expect ValueError, store unchanged); book `A3` = `P2`/`D2` at the same time (expect SCHEDULED).
- Meaningful failing test path/name and exact relevant failure: `project/tests/test_regressions.py::test_same_practitioner_same_time_is_rejected` (TEST-R01) / [complete: exact failure line]
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete from your run]
- Expected behaviour and requirement: after cancelling, the same object is retained with CANCELLED status, stays in `list_appointments()`, and is returned by both store and service lookup (FR-06, FR-07, BR-07, AC-05.2, FR-08). A repeated cancel is still rejected with ValueError and changes nothing.
- Minimal synthetic reproduction steps: fresh store; register `P1`, `D1`; book `A1` at 2026-10-01 09:00; cancel `A1`; check status, list membership, `store.find_appointment('A1')` (None vs object) and `service.find_appointment('A1')` (LookupError vs object); cancel `A1` again (expect ValueError).
- Meaningful failing test path/name and exact relevant failure: `project/tests/test_regressions.py::test_cancelled_appointment_is_still_found` (TEST-R02) / [complete: exact failure line]
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

### F8-02 human entry
Likely cause and why plausible: [complete]
Evidence intended to inspect / competing explanation / discriminating check: [complete]
Member and saved sequence/time or commit showing this preceded consultation: [complete]

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | `python -m pytest -q tests/test_regressions.py::test_same_practitioner_same_time_is_rejected` in `project/` | [complete] |
| F8-01 after repair | [complete] | same | [complete] |
| F8-02 before repair | [complete] | `python -m pytest -q tests/test_regressions.py::test_cancelled_appointment_is_still_found` in `project/` | [complete] |
| F8-02 after repair | [complete] | same | [complete] |
| Full suite after both repairs, before refactor | [complete] | `python -m pytest -q` in `project/` | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour:
- TEST-R01 uses `pytest.raises(ValueError)` around the same-practitioner booking, so a booking that wrongly succeeds fails the test. `list_appointments() == before` and `find_appointment('A2') is None` catch a booking that is rejected but still stored. Booking `A3` with `D2` catches the opposite mistake, where different practitioners are treated as a conflict (AC-04.2).
- TEST-R02 checks status, list membership and identity (`is`, not `is not None`) for both store and service lookup. A lookup that returns None, raises LookupError or returns a different object all fail. The final repeated cancel checks that the FR-06 guard still raises ValueError and doesn't change anything after the repair.
- TEST-R03 checks that a cancelled appointment doesn't block the same slot, so the "SCHEDULED only" part of the conflict rule is protected while F8-01 is repaired and during the refactor.

Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: magic status string. In `project/smartcare/data_store.py`, `SmartCareDataStore.has_practitioner_conflict` compares `appointment.status.value == "scheduled"` instead of using the existing `AppointmentStatus` enum. [complete: line number]
Small proposed structural change / why justified: replace that comparison with `appointment.status is AppointmentStatus.SCHEDULED`, and add `AppointmentStatus` to the domain import in `data_store.py`. The enum is already the project's single definition of the statuses (Stage 4). A string literal can be mistyped without any error, and the enum makes the rule's intent clear. It's a one-line change, with no new architecture or dependency.
External behaviour to preserve / relevant tests: only SCHEDULED appointments for the same practitioner at the same time conflict; cancelled ones do not; different practitioners are allowed; the store is unchanged after a rejected booking. Tests: TEST-R01 and TEST-R03 in `tests/test_regressions.py`, plus every existing conflict test in the retained suite (list them by name: [complete]).
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: see B, C, D and H.
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete] / `git switch main`, `git pull`, `python -m pytest -q` in `project/` / [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Read the exact failure, reproduce it with small synthetic input, state the expected behaviour from a requirement, and write down a hypothesis together with a check that could prove it wrong. Only change code once the evidence supports the cause.

2. Where should expected behaviour come from during debugging?

Response: From the published requirements and acceptance criteria (here, revision 2: FR, AC and BR IDs) and the agreed service and store contracts. Not from what the code currently does, from a test that might itself be wrong, or from a Copilot suggestion.

3. What is a debugging hypothesis?

Response: A specific, testable explanation of why a failure happens, paired with a check that would confirm it or rule it out. For example, "the store lookup skips cancelled appointments; check by cancelling and then calling `store.find_appointment`."

4. What is a regression test and why is it retained?

Response: A test that reproduces a defect that has been fixed and passes once the defect is repaired. It stays in the suite so that if a later change (for example a refactor) brings the defect back, the suite fails straight away.

5. What is meant by root cause?

Response: The underlying code decision or condition that actually produces the failure, as opposed to where it was noticed. Fixing the root cause stops the symptom; fixing only the symptom leaves the fault in place.

6. What is refactoring?

Response: Changing the internal structure of code (names, duplication, method size, responsibilities) without changing its external behaviour. You do it under passing tests and confirm the same tests still pass afterwards.

7. What is a swallowed exception?

Response: An exception that is caught and then ignored, for example `except Exception: pass`, or caught and turned into a silent default. It hides the failure, so the caller carries on with wrong state and the real cause becomes harder to find.

8. What is a code smell?

Response: A sign in the code that suggests a design problem, such as duplication, a long method, magic strings, unclear names or a responsibility in the wrong place. It isn't a bug in itself, but it makes bugs more likely and is a reason to consider refactoring.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: As hypotheses, not answers. Check each one against the requirements, the code and actual test runs; classify it as correct, partly correct or wrong; and accept, modify or reject it with a reason. Sounding confident isn't evidence, and Copilot doesn't replace your own diagnosis or a human reviewer.

10. What is the Stage 8 engineering rule?

Response: Diagnose before you fix. Observe and reproduce, state the expected behaviour, form a hypothesis and test it against evidence, make the smallest supported repair, keep a regression test, and only refactor under passing tests.

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
