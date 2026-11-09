# Stage 7 Testing and Verification Record

Group/tutorial: Group 5, Thursday 2:30  Members/cohorts: James Nguyen, Lemuel Legaspi, Joshua Sisourath – all UG
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a patient with a valid ID and name. | Try registering a patient with a duplicate ID. | The patient is stored successfully, and duplicate IDs raise ValueError. |
| FR-05 Prevent practitioner conflict | Book an appointment when the practitioner is available. | Try booking two appointments for the same practitioner at the same time. | The conflicting booking raises ValueError and is not stored. |
| FR-06 Cancel appointment | Cancel an existing scheduled appointment. | Try cancelling an appointment that is already cancelled. | The status changes to CANCELLED, and repeated cancellation raises ValueError. |
| FR-07 Retain cancelled history | Retrieve an appointment after cancellation. | Check whether cancellation removes the appointment from storage. | The cancelled appointment remains stored and can still be retrieved. |


### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear. Why: This always passes and does not check any actual behaviour.

`assert appointment is not None`
Judgement: Weak/unclear. Why: It only checks that an appointment exists, not whether its details or status are correct.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour. Why: It confirms the appointment status is CANCELLED, but does not prove the appointment is still stored.

`assert len(results) > 0`
Judgement: Weak/unclear. Why: It only checks that results are not empty, not whether the correct results were returned.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stated behaviour. Why: It confirms the stored appointment is the same object, but does not check its cancellation status.


### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.

For each input/state, expected result and supporting contract:

- Blank identifiers: Enter an empty patient or appointment ID. Expected result: ValueError because IDs must be valid.
- Whitespace-only names: Register a patient with a name containing only spaces. Expected result: ValueError because the name is invalid.
- Same-time practitioner bookings: Book two appointments for the same practitioner at the exact same time. Expected result: ValueError because a practitioner cannot have two appointments at the same time.
- Cancelled appointments: Try cancelling an appointment that is already cancelled. Expected result: ValueError because repeated cancellation is not allowed.
- Invalid status transitions: Try cancelling a completed appointment. Expected result: ValueError because completed appointments cannot be cancelled.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.


| Candidate | What is wrong | Rewritten test intention |
|---|---|---|
| 1 | Only checks that the patient object is not None. It does not verify correct registration. | Register a patient and check that the ID and name are correct and the patient is stored. |
| 2 | Only checks that the appointment object is not None. It does not verify the booking details. | Book an appointment and check the practitioner, patient, time and status are correct. |
| 3 | Uses assert True, which always passes and does not test anything. | Cancel an appointment and assert that its status changes to CANCELLED. |
| 4 | Assumes SMS notifications exist, but SMS is not part of the stated requirements. | Test that cancelling an appointment keeps its record stored for history. |
| 5 | Tests unsupported SMS behaviour instead of a required SmartCare feature. | Attempt to book two appointments for the same practitioner at the same time and verify the conflict is rejected. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
100% code coverage only means that all the code was executed during testing. It does not mean the tests checked the correct results. Weak tests can still pass even when the software has errors or does not meet the requirements.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 Register patient | Whitespace-only patient ID is rejected during Patient construction | TEST-01 | Negative | test_required_fields() - tests/test_starter.py | ValueError is raised for a whitespace-only patient ID | Passed in 12-test run | Supplied |
| FR-06 Cancel appointment | Cancelling a scheduled appointment changes its status to CANCELLED | TEST-02 | Positive | test_cancel_appointment() - tests/test_starter.py | Appointment status becomes CANCELLED | Passed in 12-test run | Student-authored |
| FR-06 Cancel appointment | Repeated cancellation is rejected | TEST-03 | Negative | test_cancel_appointment_twice() - tests/test_starter.py | Second cancellation raises ValueError | Passed in 12-test run | Student-authored |
| FR-06 Cancel appointment | Unknown appointment IDs are rejected | TEST-04 | Negative | test_cancel_unknown_appointment() - tests/test_starter.py | Unknown ID raises LookupError | Passed in 12-test run | Student-authored |
| FR-07 Retain cancelled history | Cancelled appointments remain stored | TEST-05 | Positive | test_cancel_appointment() - tests/test_starter.py | Stored appointment is the same cancelled object | Passed in 12-test run | Student-authored |
| FR-07 Retain cancelled history | Cancelling does not remove the appointment | TEST-06 | Positive | test_domain_cancellation_and_guard() - tests/test_starter.py | Appointment remains in storage after cancellation | Passed in 12-test run | Supplied |
| FR-01 Register patient | Patient and practitioner required fields are validated | TEST-07 | Negative | test_required_fields() - tests/test_starter.py | Invalid required fields raise ValueError | Passed in 12-test run | Supplied |
| FR-01 Register patient / Appointment booking | Patient registration and appointment booking work | TEST-08 | Positive | test_registration_and_booking() - tests/test_starter.py | Patient registration and appointment booking succeed | Passed in 12-test run | Supplied |
| FR-06 Cancel appointment | Cancelling an appointment changes its status to CANCELLED and retains the record | TEST-09 | Positive | test_domain_cancellation_and_guard() - tests/test_starter.py | Appointment status becomes CANCELLED and remains stored | Passed in 12-test run | Supplied |
| FR-06 Cancel appointment | Repeated cancellation is rejected | TEST-10 | Negative | test_domain_cancellation_and_guard() - tests/test_starter.py | ValueError is raised when cancelling an already cancelled appointment | Passed in 12-test run | Supplied |
| FR-05 Prevent double booking | Same practitioner cannot be booked twice at the same time | TEST-11 | Negative | test_double_booking_rejected() - tests/test_starter.py | ValueError is raised for a conflicting booking | Passed in 12-test run | Student-authored |
| FR-02 Find patient | AC-02.1 known patient returns that patient | TEST-S01 | Positive | test_find_patient_returns_the_registered_object() - tests/test_services.py | Same stored object, also with surrounding spaces | 54 passed at a8f3640 | Student-authored |
| FR-02 Find patient | AC-02.2 unknown patient reports absence | TEST-S02 | Negative / boundary | test_find_patient_unknown_and_case_sensitive_raise_lookup_error() - tests/test_services.py | 'P9' and wrong-case 'p1' raise LookupError; no patient created | 54 passed at a8f3640 | Student-authored |
| FR-02 ID contract | "IDs are strings, trimmed, non-blank and case-sensitive" | TEST-S03 | Boundary | test_find_patient_blank_id_raises_value_error() - tests/test_services.py | Blank ID raises ValueError (invalid, not absent) | 54 passed at a8f3640 | Student-authored |
| FR-03 Practitioner lookup | "A valid unknown service lookup raises LookupError" | TEST-S04, TEST-S05 | Positive / negative / boundary | test_find_practitioner_*() - tests/test_services.py | Same object returned; 'D9'/'d1' LookupError; blank ValueError | 54 passed at a8f3640 | Student-authored |
| FR-06, FR-07 Cancel and retain | AC-05.1, AC-05.2, BR-06 | TEST-S06, TEST-S07 | Negative / positive | test_cancel_completed_appointment_is_rejected_without_change(), test_cancel_returns_same_object_and_keeps_history() - tests/test_services.py | COMPLETED rejected and unchanged; cancel returns and keeps the same object | 54 passed at a8f3640 | Student-authored |
| FR-01, FR-03 Domain validation | AC-01.1 and "Required names and specialty are non-blank" | TEST-D01–D03 | Positive / boundary | tests/test_domain.py | Trimmed fields, read-only ID; blank fields raise ValueError | 54 passed at a8f3640 | Student-authored |
| FR-04, BR-04 Appointment construction | "Use local naive datetime values at minute precision" | TEST-D04–D06 | Positive / boundary | tests/test_domain.py | Starts SCHEDULED with actual objects; seconds/microseconds/timezone and ID strings rejected | 54 passed at a8f3640 | Student-authored |
| FR-06 Domain transition | AC-05.1, AC-05.3, BR-06 | TEST-D07, TEST-D08 | Positive / negative | tests/test_domain.py | SCHEDULED→CANCELLED; CANCELLED/COMPLETED cancel raises ValueError and status unchanged | 54 passed at a8f3640 | Student-authored |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-02 | FR-06 | Scheduled appointments can be cancelled | Positive | Cancel an existing scheduled appointment | Status changes to CANCELLED | Verifies cancellation through AppointmentService |
| TEST-03 | FR-06 | Repeated cancellation is rejected | Negative | Attempt to cancel an already cancelled appointment | ValueError is raised and status remains CANCELLED | Checks repeated cancellation handling |
| TEST-04 | FR-06 | Unknown appointment IDs are rejected | Negative | Cancel an appointment using an unknown ID | LookupError is raised | Checks handling of unknown appointment IDs |
| TEST-05 | FR-07 | Cancelled appointments remain stored | Positive | Retrieve an appointment after cancellation | The same cancelled appointment object is returned | Confirms appointment history is retained |
| TEST-11 | FR-05 | Same practitioner cannot be double-booked | Negative | Attempt to book two appointments for the same practitioner at the same time | ValueError is raised | Confirms conflicting bookings are rejected |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|
| TEST-02 | Create a data store, register a patient and practitioner, then book an appointment. | Call `service.cancel_appointment("A1")`. | `assert cancelled.status == AppointmentStatus.CANCELLED` | Confirms that cancelling an appointment changes its status to CANCELLED. |
| TEST-03 | Create and book an appointment, then cancel it once. | Attempt to cancel the same appointment again. | `with pytest.raises(ValueError)` | Confirms repeated cancellation is rejected. |
| TEST-04 | Create a service with no appointment matching ID A999. | Call `service.cancel_appointment("A999")`. | `with pytest.raises(LookupError)` | Confirms unknown appointment IDs are rejected. |
| TEST-05 | Create and book an appointment in the shared data store. | Cancel the appointment and retrieve it again. | `assert service.find_appointment("A1") is cancelled` | Confirms the same appointment remains stored after cancellation. |
| TEST-11 | Create a patient, practitioner and an existing appointment at a chosen time. | Attempt to book another appointment for the same practitioner at the same time. | `with pytest.raises(ValueError)` | Confirms the system rejects double bookings for the same practitioner and time. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-07 | Patient and practitioner required fields are validated | tests/test_starter.py - test_required_fields() | Passed in 12-test run |
| TEST-08 | Patient registration and appointment booking work | tests/test_starter.py - test_registration_and_booking() | Passed in 12-test run |
| TEST-09 | Appointment cancellation changes status to CANCELLED and retains the appointment in storage | tests/test_starter.py - test_domain_cancellation_and_guard() | Passed in 12-test run |
| TEST-10 | Cancelling an already cancelled appointment raises ValueError | tests/test_starter.py - test_domain_cancellation_and_guard() | Passed in 12-test run |
| TEST-D01–D08 | Patient/Practitioner construction and validation; Appointment initial status, datetime contract, participant objects, cancel transition and illegal transitions | tests/test_domain.py (new, student-authored) | 23 new tests passed; full suite 54 passed at a8f3640 |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|
| TEST-02 | Cancel a scheduled appointment and update its status | FR-06 Appointment Cancellation | tests/test_starter.py - test_cancel_appointment() | Passed in 12-test run |
| TEST-03 | Reject repeated cancellation | FR-06 Appointment Cancellation | tests/test_starter.py - test_cancel_appointment_twice() | Passed in 12-test run |
| TEST-04 | Reject an unknown appointment ID | FR-06 Appointment Cancellation | tests/test_starter.py - test_cancel_unknown_appointment() | Passed in 12-test run |
| TEST-05 | Keep cancelled appointments stored and retrievable | FR-07 Retained History | tests/test_starter.py - test_cancel_appointment() | Passed in 12-test run |
| TEST-11 | Reject double booking for the same practitioner and time | FR-05 Prevent Double Booking | tests/test_starter.py - test_double_booking_rejected() | Passed in 12-test run |
| TEST-S01–S07 | Patient and practitioner lookup (same object, trimmed, case-sensitive, unknown vs blank), guarded cancellation and retained history | FR-02, FR-03, FR-06, FR-07 / AC-02.1, AC-02.2, AC-05.1–05.3 | tests/test_services.py (new, student-authored) | Passed; full suite 54 passed at a8f3640 |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|
| Patient registration | Whitespace-only patient ID during Patient construction | ValueError is raised and the Patient object is not created | TEST-01 |
| Appointment cancellation | Cancel an already cancelled appointment | ValueError is raised and the appointment remains CANCELLED | TEST-03 |
| Appointment cancellation | Unknown appointment ID (A999) | LookupError is raised and no appointment is changed | TEST-04 |
| Cancelled appointment history | Retrieve an appointment after cancellation | The cancelled appointment remains stored and can be retrieved | TEST-05 |
| Appointment booking | Same practitioner booked twice at the same time | ValueError is raised and the conflicting booking is rejected | TEST-11 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-06 Appointment Cancellation
Acceptance criterion: Cancelling a scheduled appointment changes its status to CANCELLED. Repeated cancellation raises ValueError.
Behaviour to test: Successful appointment cancellation and rejection of repeated cancellation.
Human-first test idea/categories: Positive test for successful cancellation and negative test for repeated cancellation.
Prompt and purpose: Ask GitHub Copilot to suggest pytest tests for appointment cancellation, including checking the CANCELLED status and rejecting repeated cancellation.

For each significant candidate, copy this entry as needed:

- Copilot test idea/candidate: Test successful appointment cancellation and repeated cancellation using pytest.
- What it claims to verify: Cancelling an appointment changes its status to CANCELLED, and cancelling it again raises ValueError.
- Requirement trace: FR-06 Appointment Cancellation.
- Assertion quality: The intended checks are useful, but the test uses a string instead of AppointmentStatus.CANCELLED.
- Human critique: Copilot used AppointmentService() without the required data store and schedule_appointment() instead of book_appointment(). The code does not match our SmartCare implementation.
- Decision: Reject
- Reason: The generated test needs changes before it can run correctly. Existing tests already verify cancellation and repeated cancellation.
- Final test reference if accepted/modified: Not retained. Existing tests are test_cancel_appointment() and test_cancel_appointment_twice() in project/tests/test_starter.py.
- Actual verification result: Copilot's generated test was not run. The existing test suite passed all 12 tests.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak?
The appointment cancellation test looked convincing because it checked the CANCELLED status and used pytest.raises(ValueError) for repeated cancellation.

Why was it weak?
It used the wrong service setup and called schedule_appointment() instead of book_appointment(). It also compared the status with a string instead of AppointmentStatus.CANCELLED.

How did you strengthen it?
I compared the suggested test with our existing SmartCare code and tests. I rejected the generated code and kept the existing tests that correctly check cancellation and repeated cancellation.

Accepted / modified / rejected test decisions and evidence:
Rejected the Copilot-generated test. See Section H and the existing tests in project/tests/test_starter.py.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python3 -m pytest -q | project/ | cbdfa07 | 12 | 0 | None | No defects found in this run | All 12 tests passed in 0.01s |
| python3 -m pytest -q | project/ | a8f3640f5c77f76295f96cac172e5fc11002efac | 54 | 0 | None | No defects found; new tests only | Added test_domain.py and test_services.py so supplied checks (test_starter.py) and student-authored evidence are separate. No production code changed. |

Individual test runs and changed-order independence evidence: Not separately performed. Full pytest suite completed with 12 passed and 0 failed.

Optional tutor-led demonstration notes: Not performed.

A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.

Requirement → test → failure/observation → diagnosis → change → verification: FR-05 → TEST-11 → Conflicting booking rejected → No failure observed → No product change required → Verified in the 12-test pytest run.

## K What the Suite Still Does Not Prove

What does your test suite still not prove? The tests cover basic registration, booking and appointment cancellation, but they do not prove that every possible input or real-world situation works correctly.

Coverage if used: Not used.

Which uncovered areas matter, and why does coverage percentage alone not establish correctness? More testing is needed for edge cases, invalid inputs and interactions between services. High coverage only means code was executed, not that the correct behaviour was checked.

Optional fixtures/parametrisation used and why, if any: Not used.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|
| Stage 7 testing and verification | feature/stage7-testing | https://github.com/newineffect14/st1-assignment-3/pull/5 | suplemonaki and newineffect14 | Requested fixes to test IDs, duplicate tests, test organisation and missing evidence | Changes requested; PR awaiting updates |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| Joshua-Sisourath | Added and tested appointment cancellation, created Stage 7 test evidence, ran pytest with 12 passing tests, and submitted PR #5 for team review. | https://github.com/newineffect14/st1-assignment-3/pull/5 |

## N Formative Questions

1. What question does verification answer?
Verification checks whether the software was built correctly according to its requirements and design.

2. What question does validation answer?
Validation checks whether the software meets the user's needs and solves the intended problem.

3. What is a unit test?
A unit test checks a small part of the code, such as a function or method, to make sure it works correctly.

4. What is a pytest fixture?
A pytest fixture provides reusable test data or setup so multiple tests can run with the same starting conditions.

5. What is parametrisation in pytest?
Parametrisation allows the same test to run multiple times with different inputs and expected results, reducing repeated test code.

6. What is regression testing?
Regression testing checks that existing features still work correctly after changes or new code have been added.

7. What does code coverage tell us, and what does it not prove?
Code coverage shows how much code was executed during testing. It does not prove that the tests check the correct behaviour or that the software has no bugs.

8. What makes an assertion weak?
An assertion is weak when it only checks that code runs or returns something, without checking the actual expected result.

9. What is the appropriate role of GitHub Copilot as a test assistant?
GitHub Copilot should assist with suggesting test ideas and code, but developers must review, correct and verify its suggestions against the actual requirements.

10. What is the Stage 7 engineering rule?
Tests must provide meaningful evidence that the software meets its requirements. Passing tests alone are not enough if they do not check the correct behaviour.

## O Stage Completion

- Tested Stage 7 branch SHA: 564278e.
- Full-suite result: 12 tests passed, 0 failed.
- Unresolved defects and effect on baseline: No defects identified by the 12-test regression run.
- Clean working tree and integration evidence: Working tree clean. Commit 564278e pushed to feature/stage7-testing. PR #5 awaiting review and merge.
- Stage 8 handover status: Stage 7 testing and documentation completed. No Stage 8 work assigned.
- All tutorial/formative responses and traceability/Copilot decisions complete: Yes, completed and recorded in Sections A-N.