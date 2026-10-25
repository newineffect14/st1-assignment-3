# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [Group 5, Thursday 2:30]
- Members, GitHub usernames and cohorts: []
- Repository URL: [https://github.com/newineffect14/st1-assignment-3/tree/main]
- Starting SHA: [e91c2447ce93402ff7fc23daf1b6bb537b985f54]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Implement patient search by ID
- Context: SmartCare needs a way to find existing patients using their patient ID intsead of manually searching through records 
- Requirement: FR-02 Patient Search
- Acceptance criteria: - The system returns the actual stored patient when a valid ID is entered. Invalid or blank IDs raise ValueError, while unknown IDs raise LookupError. IDs are case-sensitive and surrounding spaces are removed.
- Scope: Implement the find_patient() method in PatientService and create tests for valid, invalid and unknown patient IDS.
- Definition of Done: The method works correctly, tests pass, and the code has been reviewed and approved by another team member.
- Owner: Joshua-Sisourath 
- Actual issue link: https://github.com/newineffect14/st1-assignment-3/issues/1

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Implement appointment cancellation with retained history 
- Context: SmartCare needs a way to cancel appointments without deleting their records, so the clinic can still access appointment history.
- Requirement: FR-06 Appointment Cancellation and FR-07 Retained History
- Acceptance criteria: The system allows scheduled appointments to be cancelled and changes their status to CANCELLED. The same appointment remains stored and can still be retrieved. Cancelling an aldready cancelled or completed appointmnet raises ValueError. Invalid IDs raise ValueError, while unknow IDs raise LookupError.
- Scope: Implement the cancel_appointmnet() method in AppointmentService and create tests for successful cancellation, invalid IDs, repeated cancellation and retained history.
- Definition of Done: The cancellation method works correctly, all relevant tests pass, and another team member has reviewed and approved the code.
- Owner: Joshua-Sisourath
- Actual issue link: https://github.com/newineffect14st1-assignment-3/issues/2

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | [Weak] | [Doesn't explain what was changed in the code.] |
| final version | [Weak] | [Doesn't explained what was completed or updated] |
| Add patient search by ID | [Strong] | [Clearly explains the feature that was added] |
| fix stuff | [Weak] | [Too vague and doesn't identify what was fixed.] |
| Prevent cancellation of completed appointments | [Strong] | [Clearly explains the specific behaviour that was changed.] |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR includes unrelated changes that are not needed for appointment cancellation. This makes the changes harder to review.
- Responsibility and architecture concerns: Appointment cancellation should follow the existing domain rules. Changing unrelated patient fields or adding dependencies could affect other parts of SmartCare.
- Testing and review concerns: Even if the tests pass, the unrelated changes could introduce problems. The reviewer should check the actual code changes and make sure cancellation works correctly.
- Changes to remove or separate, with reasons: We would remove the unrelated patient field changes, code restructuring and new dependency from this PR. These should be separate changes if they are actually needed, so the cancellation feature is easier to test and review.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Copilot has not shown which tests were run or whether the code meets the requirements. The reviewer still needs to check the code changes and test results.

- Follow-up review question 1: Does the code meet the acceptance criteria of the linked requirement?

- Follow-up review question 2: Were all the tests actually run, and what were the results?

- Follow-up review question 3: Does the cancellation method prevent already cancelled or completed appointments from being cancelled again?

- Follow-up review question 4: Does the cancelled appointment remain stored so its history can still be accessed?

- Follow-up review question 5: Are there any unrelated code changes or unnecessary dependencies in the PR?

- Additional questions if useful: Does the code follow the existing SmartCare responsibilities and handle invalid IDs correctly?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [Use feature branches such as feature/patient-search or feature/appointment-cancellation.] |
| Commit message convention | [Use short and clear messages explaining what was changed, such as Add patient search by ID.] |
| PR size | [Keep pull requests small and focused on one feature or requirement.] |
| Another-member review requirement | [At least one different team member must review the code before it can be merged.] |
| Merge rule | [Only merge when tests pass, requirements are met, feedback is resolved and another member approves.] |
| Significant Copilot disclosure rule | [Record significant Copilot assistance, explain what was suggested and how the code was checked.] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/newineffect14/st1-assignment-3/issues/1 | FR-02 Patient Search | Joshua-Sisourath | Find stored patients by ID. Invalid IDs raise ValueError and unknown IDs raise LookupError. | Open |
| https://github.com/newineffect14/st1-assignment-3/issues/2 | FR-06 Cancellation / FR-07 Retained History | Joshua-Sisourath | Cancel scheduled appointments, retain the record and reject invalid cancellations. | Open |
| https://github.com/newineffect14/st1-assignment-3/issues/3 | FR-03 Supporting Practitioner Lookup | Joshua-Sisourath | Find stored practitioners by ID. Invalid IDs raise ValueError and unknown IDs raise LookupError. | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/newineffect14/st1-assignment-3/pull/4 - Implement appointment cancellation and tests
- Linked issue and requirement: https://github.com/newineffect14/st1-assignment-3/issues/2 - FR-06 Appointment Cancellation and FR-07 Retained History.
- Feature branch: feature/patient-search
- Changed behaviour: Implemented appointment cancellation through AppointmentService. Cancelled appointments remain stored for history instead of being deleted. The system also rejects repeated cancellations and unknown appointment IDs.
- Changed files: project/smartcare/services.py and project/tests/test_starter.py.
- Test command, directory and observed result: Ran `python3 -m pytest -q` inside the `project/` directory. All 11 tests passed in 0.01 seconds.
- Code commit SHA: 92c2af6
- Another-member reviewer: newineffect14
- Requirement, responsibilities, test assertions and unrelated-scope checks: The changes address FR-06 Appointment Cancellation and FR-07 Retained History. AppointmentService handles cancellation. Tests cover successful cancellation, repeated cancellation, unknown appointment IDs and retained history. Changes were limited to cancellation functionality and related tests.
- Key feedback: newineffect14 verbally reviewed my appointment cancellation implementation and said the code was good. No specific changes were requested.
- Author response/change and verification: The reviewer said the implementation was good, so no additional code changes were requested. I ran `python3 -m pytest -q` inside the `project/` directory and all 11 tests passed.
- Reviewer recheck and approval: newineffect14 verbally confirmed the code was good. No formal GitHub approval link has been recorded.
- Merge outcome and SHA: Pull Request #4 was successfully merged into main by Joshua-Sisourath. The merge commit SHA is c30d980.
- Significant Copilot assistance: I used GitHub Copilot during Stage 6 to assist with my appointment cancellation implementation.
- Linked issue closure: Issue #2 covers FR-06 Appointment Cancellation and FR-07 Retained History. Issue closure has not yet been confirmed.
- Each member updated main: Joshua-Sisourath updated the local main branch using `git pull origin main`. Other team members have not yet confirmed their updates.
- Integrated verification after merge: After merging PR #4, I switched to main and ran `git pull origin main` to update the repository. I then ran `python3 -m pytest -q` inside the `project/` directory. All 11 tests passed in 0.02 seconds. The merged code SHA is c30d980.

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Joshua-Sisourath – Implement appointment cancellation for SmartCare (FR-06 and FR-07).
- Prompt/purpose and relevant issue/diff: Used GitHub Copilot to assist with the appointment cancellation implementation linked to Issue #2.
- Summary of output: Copilot assisted with the appointment cancellation implementation in AppointmentService.
- Human check against actual code, requirements and tests: I checked the appointment cancellation implementation against FR-06 and FR-07. I also ran `python3 -m pytest -q` and confirmed all 11 tests passed.
- Decision – Accept / Modify / Reject: Accept – I reviewed Copilot's suggestion and accepted it after checking the implementation and confirming the tests passed.
- Reason: The final implementation supports appointment cancellation, retains cancelled appointments for history and handles invalid cancellation attempts.
- Verification/evidence: Pull Request #4 – https://github.com/newineffect14/st1-assignment-3/pull/4. All 11 tests passed after merging into main at commit c30d980.

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: newineffect14 verbally reviewed the appointment cancellation implementation and said the code was good. No specific problems were reported.
- Copilot noticed: I used Copilot to assist with the implementation, but no separate Copilot review findings were recorded.
- Overlap: Both activities related to the appointment cancellation functionality, but there are no documented findings to compare directly.
- What did the human reviewer notice that Copilot did not: No specific differences were recorded.
- What did Copilot identify that the human reviewer initially missed: No additional findings were documented.
- Unsupported or incorrect Copilot suggestion: None identified in the available records. This does not confirm that every suggestion was correct.
- Human judgement accepted, modified or rejected, and why: I accepted the Copilot suggestion after checking the final implementation against FR-06 and FR-07 and running the tests successfully.
- Which evidence justified merge approval: Pull Request #4 was merged into main at commit c30d980. All 11 tests passed after merging. The teammate's verbal feedback was positive, but formal GitHub review approval was not recorded.

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Joshua-Sisourath
- Implementation: Implemented appointment cancellation in `project/smartcare/services.py`, including retaining cancelled appointments for history. Evidence: PR #4, commit `92c2af6`.
- Testing: Added tests in `project/tests/test_starter.py` for successful cancellation, repeated cancellation, unknown appointment IDs and retained history. All 11 tests passed.
- Review: Reviewed my implementation against FR-06 and FR-07. Teammate newineffect14 also provided positive verbal feedback.
- Issue refinement: Documented Issue #2 for appointment cancellation and retained history, including acceptance criteria.
- Design and responsibility discussion: Worked on the appointment cancellation behaviour and how AppointmentService should handle cancellation and retain appointment records.
- Debugging or integration: Merged PR #4 into main and verified the integrated code using `python3 -m pytest -q`. All 11 tests passed in 0.02 seconds.
- Documentation or team support: Updated the Stage 6 activities and evidence document, including GitHub issues, pull request evidence and testing results.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count does not always mean someone contributed more. A person might make many small commits, while another person makes fewer commits with more important changes. The quality of work, testing and teamwork matter more.

## L Stage 6 formative questions

1. What is version control?**

Version control tracks changes made to code and allows developers to work together and restore previous versions if needed.

2. Why is a feature branch useful?**

A feature branch allows developers to work on new features without affecting the main code until the changes are ready.

3. What makes a commit a good engineering commit?**

A good commit contains clear, focused changes with a meaningful message explaining what was done.

4. What is a pull request?**

A pull request allows developers to submit code changes for review before merging them into the main branch.

5. What is the purpose of code review?**

Code review helps identify mistakes, check requirements and improve code quality before merging.

6. What does a Git diff show?**

A Git diff shows the differences between versions of code, including lines that were added, removed or changed.

7. What is a Definition of Done?**

A Definition of Done is a checklist of requirements that must be completed before a task is considered finished, such as implementation, testing and review.

8. What is the appropriate role of GitHub Copilot in pull-request review?**

GitHub Copilot can help identify possible issues and suggest improvements, but a human reviewer must check its suggestions and make the final decision.

9. Why should individual contribution not be judged only by commit count?**

Commit count does not show the quality or difficulty of someone's work. Testing, reviewing, debugging and helping teammates are also important contributions.

10. What is the Stage 6 engineering rule?**

Code changes should be linked to requirements, tested, reviewed by another team member and verified before being considered complete.

## M Completion and handover

- Starting SHA: `e91c244`
- Final Stage 6 code SHA: `c30d980`
- Test command: `python3 -m pytest -q`
- Working directory: `project/`
- Observed result: 11 tests passed in 0.02 seconds after merging into main.
- PR and another-member reviewer: https://github.com/newineffect14/st1-assignment-3/pull/4 – newineffect14 provided positive verbal feedback. No formal GitHub review was recorded.
- Unresolved issue or none: Issue #2 was last confirmed open. Remaining team issues require confirmation.
- Stage 7 handover status: Appointment cancellation implemented, merged and tested. Remaining team requirements need confirmation.
- Final submitted SHA if later than tested SHA: Not yet submitted. Tested code SHA is `c30d980`.

- [ ] Three Stage 6 service targets completed and checked.
- [x] Original supplied tests retained and passing.
- [x] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [x] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer materials kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.
