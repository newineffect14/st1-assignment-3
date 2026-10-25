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

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
