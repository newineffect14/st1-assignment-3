# SmartCare v1.0 – course release

SmartCare is a small console application for clinic staff to register patients and practitioners, book and cancel appointments, and list a practitioner's appointments. It is the Software Technology 1 Assignment 3 group project (undergraduate scope, Stages 6, 7, 8, 9 and 12), built against the SmartCare A3 2026 revision 2 requirements.

This is a **course release**. It makes no claim of production, clinical or security readiness. Use synthetic data only.

## Scope

Included (common UG scope):

- Register and find patients and practitioners (FR-01–FR-03)
- Book an appointment linking one registered patient and one registered practitioner (FR-04)
- Reject a second SCHEDULED booking for the same practitioner at exactly the same time; a different practitioner at that time is allowed (FR-05)
- Cancel only SCHEDULED appointments and keep them as CANCELLED history (FR-06, FR-07)
- Find an appointment by ID (FR-08)
- List a practitioner's appointments, optionally filtered by status, ordered by date/time then appointment ID (FR-09, QRY-01–QRY-04, FP-01–FP-03)
- Interactive console menu that recovers from invalid input (UI-01, UI-02)

Out of scope: saving data between runs (FR-10 is retired), rescheduling (PG only), authentication and roles, patient portal, SMS/email notifications, billing, clinical rules, patient double-booking checks, past-date checks, clinic hours and appointment durations.

## Environment

- Python 3.13 is the teaching team's verified baseline. This release was also run on Python 3.14.3 (macOS).
- pytest 8.3.5 is the only development dependency (`requirements-dev.txt`). The application itself uses only the standard library.
- On macOS use `python3` if `python` is not found.

Create and activate a virtual environment from the repository root before installing:

```sh
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\Activate.ps1       # Windows PowerShell
```

If Windows says "running scripts is disabled on this system", run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first. It only applies to that PowerShell window.

## Running SmartCare

From the repository root (the block enters `project/` and returns at the end):

```sh
cd project
python -m pip install -r requirements-dev.txt
python main.py
python main.py --interactive
python -m pytest -q
cd ..
```

- `python main.py` runs a short synthetic demonstration.
- `python main.py --interactive` starts the menu.
- `python -m pytest -q` runs the full suite. Release result: **54 passed**.

## Interactive menu

```
1. Register patient          (ID, name)
2. Find patient              (ID)
3. Register practitioner     (ID, name, specialty)
4. Find practitioner         (ID)
5. Book appointment          (appointment ID, patient ID, practitioner ID, date/time)
6. Cancel appointment        (appointment ID)
7. Find appointment          (appointment ID)
8. List practitioner appointments (practitioner ID, optional status)
0. Exit
```

Dates use the format `YYYY-MM-DD HH:MM` (for example `2026-10-01 09:00`). For option 8, leave the status blank to list all appointments, or type `scheduled`, `cancelled` or `completed`. Status input is not case-sensitive.

Invalid input prints `Error: ...` and the menu continues. A rejected operation leaves stored records unchanged.

## Structure and responsibilities

```
project/
├── main.py                 entry point (demo or --interactive)
├── requirements-dev.txt    pinned pytest
├── smartcare/
│   ├── domain.py           Patient, Practitioner, Appointment, AppointmentStatus
│   ├── data_store.py       SmartCareDataStore: session collections
│   ├── services.py         PatientService, PractitionerService, AppointmentService
│   ├── queries.py          appointment_sort_key, select_appointments (pure)
│   └── console.py          menu, input parsing and output
└── tests/
    ├── test_starter.py     supplied and Stage 6–7 tests
    ├── test_domain.py      Stage 7 domain tests
    ├── test_services.py    Stage 6–7 service tests
    ├── test_regressions.py Stage 8 fault regressions
    ├── test_queries.py     Stage 9 pure query tests
    └── test_workflows.py   Stage 9 service and console tests
```

- **Domain** objects validate their own fields; `Appointment` owns the cancellation rule.
- **SmartCareDataStore** only holds and finds the current session's records.
- **Services** coordinate use cases through one shared store: lookups, conflicts, cancellation and validated listing.
- **Queries** are pure functions with explicit inputs. They filter and sort without changing anything.
- **Console** reads input, converts text (dates, status), calls services and prints results. It holds no business rules.

## Contracts

IDs are trimmed, non-blank, case-sensitive strings. Names and specialty are required. Invalid values, duplicate IDs, conflicts and illegal status changes raise `ValueError`. A valid but unknown ID raises `LookupError` from services; the store returns `None`. Lists are new containers holding the stored objects. Times are local, naive and minute-precision.

## Responsible AI use

GitHub Copilot Chat was used for bounded review, test ideas and debugging help. Human design and hypotheses were recorded first in each stage record, and every significant suggestion was checked against code and tests before an Accept/Modify/Reject decision. See `stage08/copilot_f8_01.md`, `stage08/copilot_f8_02.md`, `stage09/copilot_review.md` and each stage record's Copilot section.

## Known limitations

- Data lasts only for the current session and is lost on exit.
- No rescheduling, authentication, notifications or billing.
- No patient-conflict, past-date, clinic-hours or duration rules.
- The conflict rule is enforced by `AppointmentService`; code that adds appointments directly to the store bypasses it.
- Single user, single process; no concurrency or timezone handling.
- Not evaluated for accessibility or usability with real clinic staff.

## Release

Label: **SmartCare v1.0 (course release)**. The exact tested and submitted commit SHAs are recorded in `stage12/stage12_activities_and_evidence.md` section K; the label never replaces the SHA.