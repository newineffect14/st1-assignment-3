# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Group 5, Thursday 2:30
Members and UG/PG applicability: James Nguyen, Lemuel Legaspi, Joshua Sisourath – we are all UG


## A Release scope and starting SHA

Release label/version and requirements baseline: SmartCare v1.0 (course release) – SmartCare A3 2026 revision 2.
Common starting SHA / branch / applicable members: `c77585a9f684f82d889f775419684835ab6dd309` on `main` (Stage 9 merge `f740044` plus section H record, PR #12). Release branch `release/stage12`. All three members.
PG starting SHA / branch / applicable members or not applicable: Not applicable – UG-only group.
Working-state review and approved integration: On `main` at `c77585a`, `git status --short`, `git diff` and `git diff --cached` were all empty, with no untracked or local work and no open PRs to integrate. Only reviewed changes were added on `release/stage12`: README updates (`224c937`, `1430e1b`) and one docstring correction (`78affea`).
Protected common candidate and PG differences: Protected common Stage 9 SHA `f7400446d2e69f7a379b1bc507b707845fc965a3`. Release candidate `78affeaedcafadda2a5c60df8be1801f259e2276` differs only in README text and one docstring, with no behaviour change. No PG work.
Feature freeze / owner / verifier: Features frozen at `c77585a`; code frozen at `78affea`. Owner James Nguyen; fresh-copy verifier Lemuel Legaspi; PR reviewer Joshua Sisourath.


## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: Release with conditions. Passing tests show the behaviour works but don't show another person can set it up, that the dependency is safe, or that users know the limits. Before sign-off: complete and fresh-copy-test the README, review the dependency's origin and licence, and document the limitation. If any of these can't be done, do not release.

Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | FR-06, FR-07, AC-05.1–05.3: cancel keeps the same object as CANCELLED; still found and listed; repeat cancel rejected | test_workflows.py::test_conflict_cancel_history_and_freed_slot_workflow; test_starter.py::test_cancel_appointment, test_cancel_appointment_twice – `78affea` | Lemuel Legaspi (PR #11), Joshua Sisourath (release PR) | Yes | None |
| Architecture responsibilities are appropriate | Code inspection: domain rules, store collections, service coordination, pure queries, console I/O kept separate | project/README.md "Structure and responsibilities"; section E – `78affea` | Joshua Sisourath | Yes, by inspection | Tests can't fully prove architecture; relies on review |
| Rescheduling is safe — PG only | Not applicable – UG-only group | – | – | – | – |
| AI use is responsible — common recheck / PG assurance | Copilot prompts, responses and Accept/Modify/Reject decisions recorded with human checks | stage08/copilot_f8_01.md, copilot_f8_02.md, stage09/copilot_review.md, Stage 6–9 records, section E | James Nguyen, Lemuel Legaspi | Yes for Stages 8–9 | Stage 6–7 AI evidence is lighter; disclosed in section E |
| System is maintainable | Small focused modules, type hints, docstrings, 31 meaningful tests, README with structure | project/smartcare/, project/tests/, project/README.md – `78affea` | Joshua Sisourath | Yes for course scale | Stale docstring found and fixed (section H) |
| FR-01–03 register/find and validation | AC-01.1, AC-01.2, AC-02.1/02.2; blank-ID and required-field validation | test_starter.py::test_registration_and_booking, test_duplicate_patient_preserves_original, test_required_fields; test_workflows.py::test_console_ui02_recovers_from_invalid_input – `78affea` | Lemuel Legaspi | Yes | None |
| FR-04–05 booking/conflict rules | AC-03.1, AC-03.2, AC-04.1, AC-04.2 | test_starter.py::test_conflict_rule_and_different_practitioner, test_unregistered_participants_rejected; test_workflows.py TEST-W05 – `78affea` | Lemuel Legaspi | Yes | None |
| FR-06–08 cancellation/history/find | AC-05.1–05.3, AC-06.1 | test_starter.py cancel tests; test_regressions.py (Stage 8 F8-02); test_workflows.py TEST-W05 – `78affea` | Lemuel Legaspi | Yes | None |
| FR-09 and QRY/FP listing/filter/order/purity | QRY-01–04, FP-01–03 | test_queries.py TEST-Q01–Q07; test_workflows.py TEST-W01–W04, W06 – `78affea` | Lemuel Legaspi | Yes | Purity also relies on code inspection |
| UI full console sequence and error recovery | UI-01, UI-02 run through the real menu | test_workflows.py TEST-W07, TEST-W08; section D fresh-copy demo – `78affea` | Lemuel Legaspi | Yes | None |
| Session-only scope / FR-10 retired | No persistence code; README and exit message state data is lost | project/README.md "Known limitations"; console exit message – `78affea` | Joshua Sisourath | Yes | Deliberate scope limit, not a defect |
| PG RES and assurance integration | Not applicable – UG-only group | – | – | – | – |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | James's MacBook Air, macOS, Python 3.14.3, pytest 8.3.5 (venv) | `project/` – `python3 -m pytest -q`; also `python3 main.py` | `c77585a9f684f82d889f775419684835ab6dd309` (starting state) | 31 passed, 0 failed; demo printed A1 with P1 and DR1 and the session-only message | Section A; release branch start |
| Complete PG if applicable | Not applicable – UG-only group | – | – | – | – |
| Affected focused checks after correction | Same as above | `project/` – `python3 -m pytest -q` (full suite, since the only code change was a docstring) | `78affeaedcafadda2a5c60df8be1801f259e2276` | 31 passed, 0 failed | Commit `78affea` (section H) |
| Full integrated recheck | Lemuel's Windows laptop, PowerShell, Python 3.13.17, pytest 8.3.5; fresh clone and new venv | `project/` – `python -m pytest -q` | `78affeaedcafadda2a5c60df8be1801f259e2276` | 31 passed in 0.32s, 0 failed | [08_pytest_31_passed.png](evidence/08_pytest_31_passed.png), [fresh_copy_results.md](evidence/fresh_copy_results.md) |
Prior assertions preserved / reviewed test diff: No test files changed in Stage 12 (`git diff c77585a 78affea -- project/tests` is empty). All 31 tests from Stages 6–9 are kept unchanged.
Remaining failure / limitation: None. Python 3.14.3 was used rather than the 3.13 baseline; both are documented in the README.


## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders | Clinic staff (the operator) register patients and practitioners, then book, cancel and list appointments. Stakeholders: reception staff, practitioners, patients, clinic manager | Course-scale scheduling with conflict rule and retained history | Explained before the demo; matches README purpose | [project/README.md](../project/README.md) |
| Register and find Patient and two Practitioners | Rows 1–5: P1 Alex Example; D1 Taylor Example; D2 Morgan Example; find P1 and D1 | FR-01–FR-03, AC-01.1, AC-02.1 | Registered and found as expected | [09](evidence/09_menu_part1a_rows1-2.png), [10](evidence/10_menu_part1b_rows2-4.png), [11](evidence/11_menu_part1c_rows5-7.png) |
| Valid booking | Row 6: A1, P1, D1, 2026-10-01 09:00 | FR-04, AC-03.1 | Booked A1 … scheduled | [11](evidence/11_menu_part1c_rows5-7.png) |
| Same practitioner exact-time conflict rejected | Row 7: A9, P1, D1, same time; row 9: find A9 | FR-05, AC-04.1, NFR-01 | "Error: Practitioner already has a SCHEDULED appointment at this time"; A9 then "not found", so no partial appointment | [11](evidence/11_menu_part1c_rows5-7.png), [12](evidence/12_menu_part1d_rows8-9.png) |
| Different practitioner same time allowed | Row 8: A2, P1, D2, same time | AC-04.2 | Booked A2 with D2 | [12](evidence/12_menu_part1d_rows8-9.png) |
| Cancel SCHEDULED and retain/find CANCELLED object | Row 10: cancel A1; row 12: find A1 | FR-06, FR-07, AC-05.1, AC-05.2 | A1 cancelled and still found as cancelled. Same object identity is asserted in TEST-W05 | [13](evidence/13_row10_cancel_A1.png), [15](evidence/15_row12_find_A1_cancelled.png) |
| Invalid/repeated cancellation rejected | Row 11: cancel A1 again | AC-05.3, BR-06 | "Error: Only SCHEDULED appointments may be cancelled"; menu continued | [14](evidence/14_row11_cancel_A1_again_error.png) |
| Default all-status listing | Row 13: list D1, blank status | QRY-02 | Listed A1 (cancelled) | [16](evidence/16_row13_list_D1_all.png) |
| Explicit filtering / empty vs unknown / deterministic order | Row 14: D1 `Scheduled`; row 15: D9; row 20: D1 blank after rebooking | QRY-02–QRY-04 | "No matching appointments." vs "Error: Practitioner not found"; final list A1 then A3. Equal-time ID tie-break shown by TEST-Q05 | [17](evidence/17_row14_list_D1_scheduled.png), [18](evidence/18_row15_list_D9_unknown_error.png), [23](evidence/23_row20_list_D1_ordered.png) |
| Invalid date/status/menu/lookup recovery and continued operation | Row 16: status `bogus`; row 17: date 2026-13-01; row 18: option 9; row 19: book A3 | UI-02, NFR-04 | Each printed an error and the menu continued; A3 then booked into the freed slot | [19](evidence/19_row16_invalid_status_error.png), [20](evidence/20_row17_impossible_date_error.png), [21](evidence/21_row18_unknown_option.png), [22](evidence/22_row19_rebook_A3.png) |
| Session-only limitation and normal exit | Row 21: option 0 | FR-10 retired, UI-01 | "Goodbye. Session-only data: records are lost on exit." | [24](evidence/24_row21_exit.png) |
| One meaningful requirement-linked pytest test explained | `test_workflows.py::test_conflict_cancel_history_and_freed_slot_workflow` | FR-05, FR-07, AC-05.2 | Rejects the conflict without changing state, cancels A1, asserts `find_appointment('A1') is` the same object with CANCELLED, still listed by default, excluded from SCHEDULED, and the slot can be rebooked. It doesn't prove behaviour for every possible input | 31 passed ([08](evidence/08_pytest_31_passed.png)) |
| Architecture and one actual AI decision / known limitation | Domain / store / services / pure queries / console | NFR-02, NFR-03 | Copilot suggested moving the conflict check into the store; rejected as over-engineering because conflict coordination belongs in the service. Known limitation: session-only data | Section E; [stage09/copilot_review.md](../stage09/copilot_review.md) |
| PG reschedule identity/participants/time and no-op | Not applicable – UG-only group | – | – | – |
| PG conflict/invalid status/failure non-mutation | Not applicable – UG-only group | – | – | – |
| PG old slot / current lookup/list ordering / assurance risks | Not applicable – UG-only group | – | – | – |
Stable demo owner / fresh process / command: Lemuel Legaspi, new process from the fresh clone at `78affea` on Windows (Python 3.13.17): `python main.py --interactive`. All 21 rows matched; full table in [fresh_copy_results.md](evidence/fresh_copy_results.md).
PG demonstrations through service/tests or not applicable: Not applicable – UG-only group.


## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | domain.py, data_store.py, services.py, queries.py, console.py | No finding. Appointment owns cancel; store only holds and finds records; services coordinate; queries are pure functions with explicit inputs; console only does I/O | No change; 31 passed at `78affea` |
| PascalCase and snake_case naming | All files in project/smartcare and project/tests | No finding. Classes are PascalCase (SmartCareDataStore, AppointmentService); functions and variables are snake_case | No change |
| Useful type hints and meaningful docstrings | services.py `find_patient` | Finding: docstring still said "Stage 6 TODO… raises NotImplementedError" although the method was implemented | Docstring corrected in `78affea` (section H); 31 passed |
| Four-space indentation and imports/layout | All source files | No finding. Four-space indentation; standard library imports first, then project imports | No change |
| Focused methods / duplication / dead or commented code | console.py `run_menu` | Minor: `run_menu` is long (one branch per menu option) but each branch only calls one service. No dead or commented-out code | Accepted, no change: splitting it now would be a refactor during feature freeze. Logged as technical debt (section G) |
| Globals / leakage / unnecessary inheritance or frameworks | console.py `MENU` | No finding. Only constant is `MENU: Final[str]`; no mutable globals, no inheritance, no frameworks | No change |
| No SQLite/persistence/repository ABCs/speculative features | Whole project | No finding. No database, file saving, repository ABC or extra features | No change |
| Synthetic data / secrets / dependencies / provenance | `git ls-files`, requirements-dev.txt, .gitignore | No finding. Only synthetic names (Alex Example, Taylor Example); no secrets or .env tracked; only dependency is pytest 8.3.5 (PyPI, MIT licence); Stage 8 tool and backups not tracked | No change |
| Significant common Copilot contributions and human verification | stage08/copilot_f8_01.md, copilot_f8_02.md, stage09/copilot_review.md | No finding. Each significant suggestion has a recorded human check and decision | No change |
| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST | – | Not applicable – UG-only group | – |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
| Stage 9: UI-02 test didn't check the malformed-date booking was not stored | UI-02; test_workflows.py | Read the test and the console booking flow | Accept – a real gap in no-partial-state evidence | Added `'7', 'A6'` lookup (`bf7b2f6`); 31 passed |
| Stage 9: conflict rule can be bypassed by direct store insertion | FR-05; data_store.py | Checked all booking goes through AppointmentService | Reject – over-engineering; conflict checking belongs in the service | No change; documented as a known limitation in README |
| Stage 9: pure query doesn't reject invalid status | QRY-04; queries.py | Checked the service validates (TEST-W04) | Reject – handout says the pure helper assumes valid inputs | No change |
| Stage 9: EOF during a field prompt isn't handled | UI-02; console.py | Confirmed fields are read before any service call | Reject – not reachable by a keyboard user; no partial writes | No change |
Access route or approved equivalent / limitations: GitHub Copilot Chat in VS Code (Ask mode for reviews) using members' own accounts. No agent mode used (UG).
Available AI evidence and missing evidence honestly disclosed: Copilot prompts and responses are recorded for Stages 8 and 9; Stage 6–7 decisions are recorded in those stage records. Everything was read, run and checked by the members through tests, code inspection and multiple PR reviews were done before being committed.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | project/README.md – title, intro, "Scope" | Lemuel Legaspi | Present and clear; UG common scope only |
| Out-of-scope capabilities and known limitations | project/README.md – "Scope", "Known limitations" | Lemuel Legaspi | Present |
| Confirmed teaching Python version and dependency installation | project/README.md – "Environment", "Running SmartCare" | Lemuel Legaspi | Gap: no commands to create/activate a venv, and Windows blocked `Activate.ps1`. Fixed in `b6cc15a` |
| Working directory / demo / interactive / test commands | project/README.md – "Running SmartCare" | Lemuel Legaspi | All commands worked. Gap: said "run from `project/`" but the block starts with `cd project`. Fixed in `b6cc15a` |
| Repository structure and architecture responsibilities | project/README.md – "Structure and responsibilities" | Lemuel Legaspi | Present |
| Responsible AI summary / synthetic-data rule | project/README.md – "Responsible AI use", intro | Lemuel Legaspi | Present |
| Release label/version and SHA links | project/README.md – "Release"; root README group index | Lemuel Legaspi | Present; exact SHAs in section K |
Root README index and project/README verified: Root README group index completed in `224c937`. project/README.md followed by Lemuel at `78affea`; the three gaps he found were fixed in `b6cc15a` (README only).
Fresh clone or extracted ZIP / candidate identity: Fresh `git clone` into a new folder (`Desktop\smartcare-fresh`), then `git checkout 78affeaedcafadda2a5c60df8be1801f259e2276`; `git rev-parse HEAD` confirmed ([01](evidence/01_fresh_clone_rev_parse_HEAD.png)).
Verifier and clean environment / actual version: Lemuel Legaspi (not the release author), Windows PowerShell, brand new venv, Python 3.13.17 (course baseline), pytest 8.3.5.
Setup/run/test commands and observed results: `python -m venv .venv` created ([02](evidence/02_create_venv.png)); `.venv\Scripts\Activate.ps1` blocked by execution policy, then worked with a process-only bypass ([03](evidence/03_activate_blocked_execution_policy.png), [04](evidence/04_venv_activated.png)); `pip install -r requirements-dev.txt` installed pytest 8.3.5 ([06](evidence/06_pip_install.png)); `python main.py` matched ([07](evidence/07_demo_main.png)); `python -m pytest -q` 31 passed in 0.32s ([08](evidence/08_pytest_31_passed.png)). Full results: [fresh_copy_results.md](evidence/fresh_copy_results.md).
Missing local file or setup gap / remedy and recheck: No missing files: everything needed was in the clone. Setup gaps: (1) no venv commands, (2) Windows execution-policy block, (3) misleading working-directory wording. Remedy: README updated in `b6cc15a` with venv commands for macOS/Windows, the process-only execution-policy note, and "From the repository root". No code changed, so the 31-test result still applies. Joshua re-checks the updated README in the release PR review.


## G Known limitations debt and release notes

Delivered features: Register and find patients and practitioners; book appointments with the same-practitioner exact-time conflict rule; cancel with retained CANCELLED history; find appointments; list a practitioner's appointments with optional status filter in date/time then ID order; interactive console menu (options 0–8) that recovers from invalid input.
Important fixes: Stage 8 repaired two data-store faults (F8-01 conflict check, F8-02 cancelled appointments disappearing from lookup) with regression tests. Stage 12 corrected a stale "TODO / NotImplementedError" docstring in `find_patient`.
Architecture/quality improvements: Stage 8 behaviour-preserving refactor; Stage 9 pure query functions with a reusable named sort key; validation kept in services and text-to-enum conversion kept in the console; final README with structure and responsibilities.
Known limitations: Session-only data; no rescheduling, authentication, notifications or billing; no patient-conflict, past-date, clinic-hours or duration rules; the conflict rule is enforced in the service, not the store; single user, single process.
AI-assisted development note: GitHub Copilot Chat was used for bounded reviews, test ideas and debugging help, and Claude was used as a step-by-step assistant. Human design came first, and every suggestion was checked against code and tests before being accepted, modified or rejected (section E).

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| `run_menu` is one long function | Harder to read and extend | Low | Split each menu option into a small helper function | Accepted – each branch only calls a service; refactoring during feature freeze adds risk |
| Conflict rule only in AppointmentService | Code adding appointments directly to the store could skip the check | Low | Keep all booking going through the service, or add a guard if the store is ever used directly | Accepted – all current callers use the service; documented in README |
| Mixed quote styles in early service code | Minor inconsistency | Low | Standardise on single quotes | Accepted – cosmetic only |
| No persistence | Records lost on exit | Out of scope | Only if a future requirement asks for it | Accepted – FR-10 retired |
Session-only synthetic data and minute-precision local time: Records last only for the running session. Times are local, naive and minute-precision, with no timezone handling. Only synthetic data is used.
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: None of these are included. Clinic staff are the assumed operator; this is out of scope for the course release.
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: Single user and single process; no concurrency, timezone policy, logging or monitoring; not tested for accessibility or usability with real clinic staff.
Difference between accepted scope limit and unresolved required behaviour: The items above are deliberate scope limits from the revision 2 requirements. No required behaviour (FR-01–FR-09, QRY, FP, UI) is unmet.
PG assurance residual risks / owner / status or not applicable: Not applicable – UG-only group.


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Maintainability / meaningful docstrings | `services.py` `find_patient` docstring said "Stage 6 TODO… The starter deliberately raises NotImplementedError", but the method returns the patient or raises LookupError | Low – misleading documentation, no behaviour impact | James Nguyen – correct the docstring | `78affea` (docstring only, 3 insertions, 4 deletions) | Full suite: 31 passed at `78affea` | None |
| README reflected Stage 9, not the release | `project/README.md` titled "SmartCare – Stage 9", no structure, AI summary or release label; root README group index blank | Medium – reproducibility and evidence gap | James Nguyen – write final README and group index | `224c937`, `1430e1b` | Fresh-copy check by Lemuel (section F) | None |
| Reproducibility (README) | Lemuel's fresh-copy check on Windows: README gave no venv commands, `Activate.ps1` was blocked by execution policy, and the working-directory wording was misleading | Medium – a new user could get stuck at setup | James Nguyen – update README | `b6cc15a` (README only) | No code change; Joshua re-checks in release PR review | None |
Justified no-change conclusion if no defect found: No behaviour defects found. The full suite, the menu demo and the code inspection in section E found nothing violating FR-01–FR-09, QRY, FP or UI requirements.
Release blockers still open / status: None.


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: Release branch `release/stage12`; release PR [#14](https://github.com/newineffect14/st1-assignment-3/pull/14), reviewed at `f10ded6` (code identical to release candidate `78affeaedcafadda2a5c60df8be1801f259e2276`).
Independent reviewer / feedback / response: Joshua Sisourath approved PR #14 after checking no code changed since `78affea`, the README covers Lem's 3 findings, the record matches the evidence, there's no junk, and 31 passed on his Mac. His one non-blocking note (section K wording understated the later non-code changes) was fixed in the next commit.
Tracked and untracked file inspection / cleanliness: `git ls-files` lists only README.md, .gitignore, project/ source and tests, and stage records. `git status --short` was empty. .gitignore excludes .venv, caches, .env and Stage 8 tool folders.
Secrets/staff material/caches/tool-metadata exclusion check: No secrets, .env, real patient data, staff solutions, peer forms, caches, Stage 8 utility or backups are tracked.
Candidate recovery plan / known-good SHA: Known-good tested SHA `78affeaedcafadda2a5c60df8be1801f259e2276`; protected Stage 9 SHA `f7400446d2e69f7a379b1bc507b707845fc965a3`. Either can be restored with `git checkout <SHA>` or a reviewed revert commit. History is never rewritten.
Named substantive contributions: James Nguyen – Stage 9 queries, service listing, console menu and tests; Stage 12 release branch, README and record. Lemuel Legaspi – Stage 8 debugging and refactoring; Stage 9 review (PR #11), sections G and H; Stage 12 fresh-copy verification and demo. Joshua Sisourath – Stages 6–7 implementation and testing; Stage 9 README and sections D/F; Stage 12 release PR review.


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: `78affeaedcafadda2a5c60df8be1801f259e2276` (31 passed; fresh-copy verified by Lemuel, section F).
Exact PG tested SHA or not applicable: Not applicable – UG-only group.
Final submitted SHA / repository URL: TO FILL (merge commit on `main`) – https://github.com/newineffect14/st1-assignment-3
Evidence-only later commit and difference explanation: Commits after `78affea` change only non-executable files: project/README.md (`b6cc15a`, fresh-copy setup fixes), stage12/evidence/ (`fea44b3`), stage09 record and screenshots (`1d3f880`), and the Stage 12 record. No code, tests or main.py changed (`git diff 78affea -- project/smartcare project/tests project/main.py` is empty, confirmed by Joshua in PR #14).
Executable changes after testing and re-verification: None after `78affea`. The full suite is rerun on the final submitted SHA anyway.
Source ZIP name / SHA correspondence / extracted comparison: TO FILL – `SmartCare-release.zip` from `git archive` of the final submitted SHA, extracted and checked.


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: Canvas "Assignment 3 Overview" (website URL submission), repository URL, full submitted SHA, tested SHA and source ZIP as confirmed with our tutor.
Deadline/timezone: Extended to Monday 9 November 2026 midnight
Repository access arrangement: Public repository https://github.com/newineffect14/st1-assignment-3
Mixed-candidate upload arrangement: Not applicable, UG-only group, one common candidate.
Oral/video recording/accessibility arrangements: Team viva as arranged by our tutor; no special arrangements requested.
Remaining administration or release dependency: Section M (Joshua), team sign-off of J and N, release PR approval and merge, then ZIP from the merge commit and Canvas submission.


## M Formative questions

1. What is a release candidate? A release candidate is the exact commit we propose to release once testing is done. Ours is `78affeaedcafadda2a5c60df8be1801f259e2276`, which James tested on Mac and Lem tested from a fresh Windows clone.

2. What is feature freeze and why is it used? Feature freeze means we stop adding new features so the release can be tested and stabilised without things changing underneath us. We froze features at `c77585a`; after that only one docstring fix (`78affea`) and documentation changed.

3. What is regression testing in a release context? Regression testing means re-running all the earlier tests to check that recent changes haven't broken anything that already worked. We kept all 31 tests from Stages 6–9, and they passed on both James's Mac and Lem's fresh Windows copy.

4. What is a known limitation? A known limitation is something the release deliberately doesn't do, written down so users aren't surprised. For example, SmartCare only keeps data for the current session and doesn't support rescheduling appointments.

5. What is technical debt? Technical debt is a shortcut or design weakness we accept now that will cost extra effort to fix later. For example, `run_menu` is one long function that would be harder to maintain or extend (see section G).

6. What are release notes? Release notes are a short summary of what the release delivers, what was fixed and improved, plus its known limitations and how AI was used. Ours are in section G.

7. What is software maintenance? Software maintenance is any change made after release, such as bug fixes, updates or improvements. These should go through reviewed commits so the submitted version can always be recovered.

8. What is the purpose of the individual demonstration/viva? The viva checks that each member actually understands the system and can explain how it works and what they contributed, not just that the code exists.

9. What should the final responsible-AI check establish before release? It should confirm that a human checked every AI suggestion, decisions are recorded, there are no secrets or real personal data, there are no unexplained changes or unnecessary dependencies, and AI use is disclosed honestly (section E).

10. What is the main course conclusion about AI and the role of the software engineer? AI can generate code, but engineers are still needed to understand the requirements, design the system, verify it with tests, review changes, make decisions and take responsibility for the result.


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | [response] |
| Two requirements and acceptance criteria | [response] |
| Domain model and architecture | [response] |
| Design trade-off | [response] |
| Meaningful test and its limits / 100 percent coverage | [response] |
| Diagnosed defect and verification | [response] |
| Shared store and session-state/query responsibilities | [response] |
| What would break if session-state lookup/query responsibilities changed? | [response] |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] |
| FR-07 retained history test | [response] |
| Actual AI change rejected/modified or honestly accepted with verification | [response] |
| Unresolved limitation / future production work | [response] |
| Personal implementation contribution | [response] |
| Personal test/review/design/integration contribution | [response] |
| PG agentic change and rescheduling verification | [response] |
| PG responsible-AI risk/remediation or supported no finding | [response] |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
