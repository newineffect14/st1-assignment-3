"""Stage 7 domain tests: construction, validation and status transitions."""


from datetime import datetime, timezone
from typing import Final

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)

BOOKING_TIME: Final[datetime] = datetime(2026, 10, 1, 9, 0)


def participants() -> tuple[Patient, Practitioner]:
    """Return fresh synthetic participants for a domain test."""
    return (
        Patient('P1', 'Alex Example'),
        Practitioner('D1', 'Taylor Example', 'General'),
    )


def test_patient_fields_are_trimmed_and_id_is_read_only() -> None:
    """TEST-D01 / FR-01, AC-01.1: verify trimmed fields and read-only ID."""
    patient: Patient = Patient('  P1  ', '  Alex Example  ')
    assert patient.patient_id == 'P1'
    assert patient.name == 'Alex Example'
    with pytest.raises(AttributeError):
        patient.patient_id = 'P2'
    assert patient.patient_id == 'P1'


@pytest.mark.parametrize('patient_id, name', [
    ('', 'Alex Example'),
    ('   ', 'Alex Example'),
    ('P1', ''),
    ('P1', '   '),
])
def test_patient_rejects_blank_id_or_name(patient_id: str, name: str) -> None:
    """TEST-D02 / FR-01 contract: verify blank ID or name raises
    ValueError.
    """
    with pytest.raises(ValueError):
        Patient(patient_id, name)


@pytest.mark.parametrize('practitioner_id, name, specialty', [
    ('   ', 'Taylor Example', 'General'),
    ('D1', '   ', 'General'),
    ('D1', 'Taylor Example', '   '),
])
def test_practitioner_rejects_blank_fields(
    practitioner_id: str,
    name: str,
    specialty: str,
) -> None:
    """TEST-D03 / FR-03 contract: verify each blank required field raises
    ValueError.
    """
    with pytest.raises(ValueError):
        Practitioner(practitioner_id, name, specialty)


def test_appointment_starts_scheduled_with_actual_participants() -> None:
    """TEST-D04 / FR-04, BR-04: verify initial status and object
    identity.
    """
    patient, practitioner = participants()
    appointment: Appointment = Appointment('A1', patient, practitioner, BOOKING_TIME)
    assert appointment.status is AppointmentStatus.SCHEDULED
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == BOOKING_TIME


@pytest.mark.parametrize('date_time', [
    datetime(2026, 10, 1, 9, 0, 30),
    datetime(2026, 10, 1, 9, 0, 0, 500),
    datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
])
def test_appointment_rejects_non_minute_or_aware_time(date_time: datetime) -> None:
    """TEST-D05 / datetime contract: verify seconds, microseconds and
    timezone-aware values raise ValueError.
    """
    patient, practitioner = participants()
    with pytest.raises(ValueError):
        Appointment('A1', patient, practitioner, date_time)


def test_appointment_rejects_participant_ids_instead_of_objects() -> None:
    """TEST-D06 / BR-04: verify plain ID strings are not accepted as
    participants.
    """
    patient, practitioner = participants()
    with pytest.raises(ValueError):
        Appointment('A1', 'P1', practitioner, BOOKING_TIME)
    with pytest.raises(ValueError):
        Appointment('A1', patient, 'D1', BOOKING_TIME)


def test_cancel_changes_scheduled_to_cancelled() -> None:
    """TEST-D07 / FR-06, AC-05.1: verify the domain transition."""
    patient, practitioner = participants()
    appointment: Appointment = Appointment('A1', patient, practitioner, BOOKING_TIME)
    appointment.cancel()
    assert appointment.status is AppointmentStatus.CANCELLED


@pytest.mark.parametrize('status', [
    AppointmentStatus.CANCELLED,
    AppointmentStatus.COMPLETED,
])
def test_cancel_rejects_non_scheduled_without_change(
    status: AppointmentStatus,
) -> None:
    """TEST-D08 / BR-06, AC-05.3: verify illegal transitions raise
    ValueError and leave the status unchanged.
    """
    patient, practitioner = participants()
    appointment: Appointment = Appointment(
        'A1',
        patient,
        practitioner,
        BOOKING_TIME,
        status,
    )
    with pytest.raises(ValueError):
        appointment.cancel()
    assert appointment.status is status
