"""Stage 9 service listing and integrated workflow tests (QRY-04, UI-01)."""


import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Final

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

BOOKING_TIME: Final[datetime] = datetime(2026, 10, 1, 9, 0)

PROJECT_DIR: Final[Path] = Path(__file__).resolve().parents[1]


def run_console(lines: list[str]) -> str:
    """Run the real interactive menu with scripted input and return its
    output.
    """
    result: subprocess.CompletedProcess[str] = subprocess.run(
        [sys.executable, 'main.py', '--interactive'],
        cwd=PROJECT_DIR,
        input='\n'.join(lines) + '\n',
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0
    return result.stdout

def foundation() -> tuple[SmartCareDataStore, AppointmentService]:
    """Return a fresh store with P1, D1 and D2 plus an appointment
    service.
    """
    data_store: SmartCareDataStore = SmartCareDataStore()
    PatientService(data_store).register_patient('P1', 'Alex Example')
    practitioners: PractitionerService = PractitionerService(data_store)
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Morgan Example', 'General')
    return data_store, AppointmentService(data_store)


def test_known_practitioner_without_appointments_returns_empty() -> None:
    """TEST-W01 / QRY-04: verify a known practitioner with no matches
    gives an empty list.
    """
    _, appointment_service = foundation()
    assert appointment_service.list_practitioner_appointments('D1') == []
    assert appointment_service.list_practitioner_appointments(
        'D1',
        AppointmentStatus.CANCELLED,
    ) == []


def test_unknown_practitioner_raises_lookup_error() -> None:
    """TEST-W02 / QRY-04: verify a valid unregistered ID raises
    LookupError.
    """
    _, appointment_service = foundation()
    with pytest.raises(LookupError):
        appointment_service.list_practitioner_appointments('D9')


def test_blank_practitioner_id_raises_value_error() -> None:
    """TEST-W03 / QRY-04: verify a blank ID raises ValueError."""
    _, appointment_service = foundation()
    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments('   ')


def test_text_status_raises_value_error() -> None:
    """TEST-W04 / QRY-04: verify status text is rejected, not treated as
    no matches.
    """
    _, appointment_service = foundation()
    appointment_service.book_appointment('A1', 'P1', 'D1', BOOKING_TIME)
    with pytest.raises(ValueError):
        appointment_service.list_practitioner_appointments('D1', 'scheduled')


def test_conflict_cancel_history_and_freed_slot_workflow() -> None:
    """TEST-W05 / UI-01, FR-05, FR-07, AC-05.2: verify the integrated
    booking, cancellation and listing workflow.
    """
    data_store, appointment_service = foundation()
    first: Appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        BOOKING_TIME,
    )

    # Same practitioner and time is rejected without changing state.
    before: list[Appointment] = data_store.list_appointments()
    with pytest.raises(ValueError):
        appointment_service.book_appointment('A9', 'P1', 'D1', BOOKING_TIME)
    assert data_store.list_appointments() == before
    assert data_store.find_appointment('A9') is None

    # Unknown patient is rejected and does not reserve the ID.
    with pytest.raises(LookupError):
        appointment_service.book_appointment('A8', 'P9', 'D1', BOOKING_TIME)
    assert data_store.find_appointment('A8') is None

    # Different practitioner at the same time is allowed (AC-04.2).
    appointment_service.book_appointment('A2', 'P1', 'D2', BOOKING_TIME)

    # Cancelling keeps the same object as history (FR-07).
    appointment_service.cancel_appointment('A1')
    assert appointment_service.find_appointment('A1') is first
    assert first.status is AppointmentStatus.CANCELLED
    assert appointment_service.list_practitioner_appointments('D1') == [first]
    assert appointment_service.list_practitioner_appointments(
        'D1',
        AppointmentStatus.SCHEDULED,
    ) == []

    # Repeated cancellation is rejected and status is unchanged.
    with pytest.raises(ValueError):
        appointment_service.cancel_appointment('A1')
    assert first.status is AppointmentStatus.CANCELLED

    # The freed slot can be booked again.
    replacement: Appointment = appointment_service.book_appointment(
        'A3',
        'P1',
        'D1',
        BOOKING_TIME,
    )
    assert appointment_service.list_practitioner_appointments('D1') == [
        first,
        replacement,
    ]
    assert appointment_service.list_practitioner_appointments(
        'D1',
        AppointmentStatus.SCHEDULED,
    ) == [replacement]


def test_listing_uses_registered_practitioner_id() -> None:
    """TEST-W06 / QRY-04: verify surrounding spaces still match the
    registered practitioner.
    """
    _, appointment_service = foundation()
    appointment: Appointment = appointment_service.book_appointment(
        'A1',
        'P1',
        'D1',
        BOOKING_TIME,
    )
    assert appointment_service.list_practitioner_appointments('  D1  ') == [
        appointment,
    ]

def test_console_ui01_demonstration() -> None:
    """TEST-W07 / UI-01: verify the full menu demonstration in one
    session.
    """
    output: str = run_console([
        '1', 'P1', 'Alex Example',
        '3', 'D1', 'Taylor Example', 'General',
        '3', 'D2', 'Morgan Example', 'General',
        '2', 'P1',
        '4', 'D1',
        '4', 'D2',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A9', 'P1', 'D1', '2026-10-01 09:00',
        '5', 'A2', 'P1', 'D2', '2026-10-01 09:00',
        '6', 'A1',
        '7', 'A1',
        '8', 'D1', '',
        '8', 'D1', 'scheduled',
        '5', 'A3', 'P1', 'D1', '2026-10-01 09:00',
        '8', 'D1', '',
        '0',
    ])
    assert 'Found patient P1: Alex Example' in output
    assert 'Booked A2: P1 with D2, 2026-10-01 09:00, scheduled' in output
    assert 'A1: P1 with D1, 2026-10-01 09:00, cancelled' in output
    assert 'No matching appointments.' in output
    assert 'Booked A3: P1 with D1, 2026-10-01 09:00, scheduled' in output
    assert 'Goodbye' in output


def test_console_ui02_recovers_from_invalid_input() -> None:
    """TEST-W08 / UI-02: verify invalid input is reported and the menu
    continues without partial changes.
    """
    output: str = run_console([
        '9',
        '2', '   ',
        '2', 'P9',
        '1', 'P1', 'Alex Example',
        '1', 'P1', 'Replacement',
        '3', 'D1', 'Taylor Example', 'General',
        '5', 'A5', 'P9', 'D1', '2026-10-01 09:00',
        '5', 'A6', 'P1', 'D1', '2026-13-01 09:00',
        '7', 'A5',
        '6', 'A7',
        '5', 'A1', 'P1', 'D1', '2026-10-01 09:00',
        '6', 'A1',
        '6', 'A1',
        '8', 'D1', 'bogus',
        '2', 'P1',
        '0',
    ])
    assert 'Unknown option; choose 0-8.' in output
    assert output.count('Error:') >= 9
    # The original patient was not overwritten by the duplicate.
    assert 'Found patient P1: Alex Example' in output
    assert 'Goodbye' in output