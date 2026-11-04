"""Stage 9 service listing and integrated workflow tests (QRY-04, UI-01)."""


from datetime import datetime
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