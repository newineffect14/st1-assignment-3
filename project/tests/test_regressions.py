"""Stage 8 regression tests for the two prepared defects.

Each test reproduces one defect with synthetic data in a fresh store,
using the current service signatures. They are kept after the repairs
so the same faults cannot come back unnoticed.
"""

from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

WHEN = datetime(2026, 10, 1, 9, 0)


def clinic() -> tuple[SmartCareDataStore, AppointmentService]:
    """Fresh store with two patients and two practitioners (synthetic)."""
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    patients.register_patient('P1', 'Alex Example')
    patients.register_patient('P2', 'Sam Example')
    practitioners = PractitionerService(data_store)
    practitioners.register_practitioner('D1', 'Taylor Example', 'General')
    practitioners.register_practitioner('D2', 'Jordan Example', 'General')
    return data_store, AppointmentService(data_store)


def test_same_practitioner_same_time_is_rejected() -> None:
    """TEST-R01 F8-01, FR-05 / AC-04.1 and AC-04.2.

    A second SCHEDULED booking for the same practitioner at the same
    datetime raises ValueError and leaves the store unchanged. A
    different practitioner at that same time is still allowed.
    """
    data_store, appointments = clinic()
    first = appointments.book_appointment('A1', 'P1', 'D1', WHEN)
    before = data_store.list_appointments()

    with pytest.raises(ValueError):
        appointments.book_appointment('A2', 'P2', 'D1', WHEN)

    assert data_store.list_appointments() == before
    assert data_store.find_appointment('A2') is None

    other = appointments.book_appointment('A3', 'P2', 'D2', WHEN)
    assert other.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, other]


def test_cancelled_appointment_is_still_found() -> None:
    """TEST-R02 F8-02, FR-06 / FR-07 / BR-07, AC-05.2 and FR-08.

    A cancelled appointment stays in the store as the same object with
    CANCELLED status, and both store and service lookups return it.
    Cancelling it again is still rejected without changing anything.
    """
    data_store, appointments = clinic()
    appointment = appointments.book_appointment('A1', 'P1', 'D1', WHEN)

    appointments.cancel_appointment('A1')

    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]
    assert data_store.find_appointment('A1') is appointment
    assert appointments.find_appointment('A1') is appointment

    with pytest.raises(ValueError):
        appointments.cancel_appointment('A1')
    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.list_appointments() == [appointment]


def test_cancelled_slot_can_be_rebooked() -> None:
    """TEST-R03 FR-05 boundary: only SCHEDULED appointments conflict.

    Protects the status condition in the conflict check while F8-01 is
    repaired and while the refactor in section H changes that line.
    """
    data_store, appointments = clinic()
    appointments.book_appointment('A1', 'P1', 'D1', WHEN)
    appointments.cancel_appointment('A1')

    rebooked = appointments.book_appointment('A2', 'P2', 'D1', WHEN)

    assert isinstance(rebooked, Appointment)
    assert rebooked.status is AppointmentStatus.SCHEDULED
    assert len(data_store.list_appointments()) == 2
