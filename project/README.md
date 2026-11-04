# SmartCare – Stage 9

## Requirements

- Python 3.13 or compatible version
- pytest 8.3.5
- Runtime uses the Python standard library

## Running SmartCare

Open a terminal in the `project` directory.

Run the standard demonstration:

```bash
python3 main.py
```

Run the interactive console:

```bash
python3 main.py --interactive
```

Run the automated tests:

```bash
python3 -m pytest -q
```

If pytest is missing, install the development dependencies:

```bash
python3 -m pip install -r requirements-dev.txt
```

## Interactive menu

The interactive console provides the following options:

0. Exit
1. Register patient
2. Find patient
3. Register practitioner
4. Find practitioner
5. Book appointment
6. Cancel appointment
7. Find appointment
8. List practitioner appointments

## Features

SmartCare supports patient and practitioner registration and lookup, appointment booking, cancellation and appointment queries.

The system prevents double-booking for the same practitioner at the same time. Cancelled appointments remain available in the appointment history, and their previous time slots can be booked again.

Appointments can be listed by practitioner and optionally filtered by status.

## Validation

The console checks invalid menu selections, missing records, duplicate IDs, invalid dates, booking conflicts and invalid status filters.

Errors are displayed without closing the interactive session.

## Testing

Stage 9 includes automated workflow tests and manual UI-01 and UI-02 demonstrations.

The automated test suite passed with 31 tests.

## Limitations

- Data is stored in memory and is lost when the application closes.
- Only synthetic patient information should be used.
- Appointment rescheduling is not supported.
- The system does not check patient scheduling conflicts or prevent past-date bookings.
