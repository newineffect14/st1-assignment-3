"""Stage 6-7 service tests: lookup, errors and guarded cancellation."""


from datetime import datetime
from typing import Final

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

BOOKING_TIME: Final[datetime] = datetime(2026, 10, 1, 9, 0)


def foundation() -> tuple[
    SmartCareDataStore,
    PatientService,
    PractitionerService,
    AppointmentService,
]:
    """Return a fresh store and the three services sharing it."""
    data_store: SmartCareDataStore = SmartCareDataStore()
    return (
        data_store,
        PatientService(data_store),
        PractitionerService(data_store),
        AppointmentService(data_store),
    )


def test_find_patient_returns_the_registered_object() -> None:
    """TEST-S01 / FR-02, AC-02.1: verify lookup returns the same stored
    object, including with surrounding spaces.
    """
    _, patients, _, _ = foundation()
    registered: Patient = patients.register_patient('P1', 'Alex Example')
    assert patients.find_patient('P1') is registered
    assert patients.find_patient('  P1  ') is registered


def test_find_patient_unknown_and_case_sensitive_raise_lookup_error() -> None:
    """TEST-S02 / FR-02, AC-02.2: verify absent and wrong-case IDs report
    absence without creating a patient.
    """
    data_store, patients, _, _ = foundation()
    patients.register_patient('P1', 'Alex Example')
    with pytest.raises(LookupError):
        patients.find_patient('P9')
    with pytest.raises(LookupError):
        patients.find_patient('p1')
    assert len(data_store.list_patients()) == 1


def test_find_patient_blank_id_raises_value_error() -> None:
    """TEST-S03 / ID contract: verify a blank ID is invalid, not absent."""
    _, patients, _, _ = foundation()
    with pytest.raises(ValueError):
        patients.find_patient('   ')


def test_find_practitioner_returns_the_registered_object() -> None:
    """TEST-S04 / FR-03: verify practitioner lookup returns the same stored
    object.
    """
    _, _, practitioners, _ = foundation()
    registered: Practitioner = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    assert practitioners.find_practitioner('D1') is registered
    assert practitioners.find_practitioner('  D1  ') is registered


def test_find_practitioner_unknown_blank_and_case_sensitive() -> None:
    """TEST-S05 / FR-03 contract: verify unknown and wrong-case IDs raise
    LookupError and a blank ID raises ValueError.
    """
    _, _, practitioners, _ = foundation()
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    with pytest.raises(LookupError):
        practitioners.find_practitioner('D9')
    with pytest.raises(LookupError):
        practitioners.find_practitioner('d1')
    with pytest.raises(ValueError):
        practitioners.find_practitioner('   ')


def test_cancel_completed_appointment_is_rejected_without_change() -> None:
    """TEST-S06 / FR-06, BR-06: verify a COMPLETED fixture cannot be
    cancelled and is left unchanged in the store.
    """
    data_store, patients, practitioners, appointments = foundation()
    patient: Patient = patients.register_patient('P1', 'Alex Example')
    practitioner: Practitioner = practitioners.register_practitioner(
        'D1',
        'Taylor Example',
        'General',
    )
    completed: Appointment = Appointment(
        'A1',
        patient,
        practitioner,
        BOOKING_TIME,
        AppointmentStatus.COMPLETED,
    )
    data_store.add_appointment(completed)
    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')
    assert appointments.find_appointment('A1') is completed
    assert completed.status is AppointmentStatus.COMPLETED


def test_cancel_returns_same_object_and_keeps_history() -> None:
    """TEST-S07 / FR-06, FR-07, AC-05.1, AC-05.2: verify cancellation
    returns and keeps the same stored object.
    """
    data_store, patients, practitioners, appointments = foundation()
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    booked: Appointment = appointments.book_appointment(
        'A1',
        'P1',
        'D1',
        BOOKING_TIME,
    )
    cancelled: Appointment = appointments.cancel_appointment('A1')
    assert cancelled is booked
    assert data_store.find_appointment('A1') is booked
    assert booked.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [booked]
