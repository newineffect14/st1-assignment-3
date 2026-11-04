# F8-02 Copilot consultation

Member: Lemuel Legaspi. Date: 3 Nov 2026, after the E entry was committed in fb377e0.
Tool: GitHub Copilot Chat in VS Code.

## Prompt
Observed behaviour:After cancelling appointment A1, its status is CANCELLED and data_store.list_appointments() still contains it, but data_store.find_appointment('A1') returns None and AppointmentService.find_appointment('A1') raises LookupError: Appointment not found. Cancelling A1 a second time raises LookupError instead of ValueError.Expected behaviour:A cancelled appointment is retained as the same object with CANCELLED status and both store and service lookup return it (FR-06, FR-07, BR-07, AC-05.2, FR-08). A repeated cancel is rejected with ValueError without changing state.Steps to reproduce:1. New SmartCareDataStore; register patient P1 and practitioner D1.2. book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9, 0)).3. cancel_appointment('A1').4. Check status, list_appointments(), data_store.find_appointment('A1') and AppointmentService.find_appointment('A1').Failing test:project/tests/test_regressions.py::test_cancelled_appointment_is_still_foundtests\test_regressions.py:71: AssertionError: assert None is <smartcare.domain.Appointment object>(lines 69 and 70, status CANCELLED and list membership, pass)My hypothesis:SmartCareDataStore.find_appointment skips appointments whose status is CANCELLED, so it returns None even though the object is still stored.Relevant code (smartcare/data_store.py):def find_appointment(self, appointment_id: str) -> Appointment | None:        if not isinstance(appointment_id, str) or not appointment_id.strip():            raise ValueError("Appointment ID cannot be blank")        for appointment in self.list_appointments():            if (appointment.appointment_id == appointment_id.strip()                    and appointment.status.value != "cancelled"):                return appointment        return NoneTask:Rank the three most likely causes. For each, identifythe evidence I should inspect to distinguish it fromthe other possible causes.Do not rewrite the entire application.Do not invent requirements.Treat all suggested explanations as hypotheses.

## Copilot reply
Your hypothesis is a strong candidate, but it is still only a hypothesis. Based on the behaviour you observed and the code fragment provided, I would rank the likely causes as follows.

1. find_appointment() deliberately filters out CANCELLED appointments
Why it is the most likely cause

The implementation you showed contains an explicit status check:

Python
if (appointment.appointment_id == appointment_id.strip()
and appointment.status.value != "cancelled"):
return appointment

That means an appointment can:

remain in list_appointments()
have status CANCELLED
still fail lookup through find_appointment()

which matches the observed symptoms exactly.

It also naturally explains the second failure:

First cancellation succeeds.
Appointment remains stored.
Subsequent lookup returns None because cancelled appointments are filtered out.
Service interprets None as "appointment does not exist".
Second cancel raises LookupError rather than a state-related error such as ValueError.
Evidence to inspect

Inspect whether:

list_appointments() returns the cancelled appointment object.
The object returned by list_appointments() has the same ID (A1).
Stepping through find_appointment() reaches the matching appointment but fails the status predicate.
Removing or bypassing only the status check causes:
data_store.find_appointment("A1") to return the object,
AppointmentService.find_appointment("A1") to return the object,
repeated cancellation behaviour to change.

If all of those occur, this hypothesis is strongly supported.

2. Cancellation replaces or mutates the appointment into a state representation that lookup does not recognise
Why it is plausible

The failure may not be caused solely by the datastore filter.

For example, cancellation logic might:

replace the original appointment object,
alter the status value unexpectedly,
move the appointment to a different collection,
wrap it in another type,
change identifiers.

The datastore filter would still be suspicious, but the deeper defect could actually be in cancellation behaviour itself.

Evidence to inspect

Inspect the appointment object immediately:

before cancellation,
after cancellation,
when iterating inside find_appointment().

Specifically compare:

Python
id(appointment)
appointment.appointment_id
appointment.status
appointment.status.value
type(appointment)

Things that would support this hypothesis:

object identity changes unexpectedly,
appointment_id changes,
status becomes something other than the expected cancelled value,
cancelled appointments are stored in a different collection than active appointments.

Things that would weaken this hypothesis:

the exact same object remains in the same collection with the expected ID and status, and is only excluded by the status filter shown above.
3. Service-layer logic independently treats cancelled appointments as "not found"
Why it is plausible

The datastore method shown clearly excludes cancelled appointments, but the observed failure involves both:

SmartCareDataStore.find_appointment()
AppointmentService.find_appointment()

There are two possibilities:

Service simply delegates to datastore and inherits the defect.
Service has its own "active only" filtering logic.

If the service also filters cancelled appointments, fixing the datastore alone may not resolve all failing requirements.

Evidence to inspect

Inspect:

Python
AppointmentService.find_appointment(...)

and any helper methods it uses.

Look for patterns such as:

Python
if appointment.status == AppointmentStatus.CANCELLED:
return None

or

Python
raise LookupError(...)

after a successful datastore lookup.

Evidence supporting this hypothesis:

datastore returns the cancelled appointment,
service still rejects it.

Evidence against it:

service merely does:
Python
appointment = data_store.find_appointment(...)
if appointment is None:
raise LookupError(...)

In that case the root cause is more likely entirely within datastore lookup.

Distinguishing the hypotheses quickly

A useful diagnostic sequence is:

Verify cancelled appointment still exists in underlying storage.
Iterate through list_appointments() and inspect the exact object.
Step through data_store.find_appointment("A1").
Observe whether the matching appointment is rejected only by:
Python
appointment.status.value != "cancelled"
Then inspect AppointmentService.find_appointment() to see whether it has any additional filtering.

If step 4 shows the object is found but excluded solely because of that predicate, Hypothesis 1 becomes the leading explanation. If the object itself has changed unexpectedly, Hypothesis 2 gains weight. If datastore returns the object correctly but service still rejects it, Hypothesis 3 becomes the primary explanation.

## Runtime check (run by Lemuel after the reply)
before cancel: 2720909534144 'A1' AppointmentStatus.SCHEDULED | store lookup is a: True
after cancel : 2720909534144 'A1' AppointmentStatus.CANCELLED | same object in list: True
store lookup : None