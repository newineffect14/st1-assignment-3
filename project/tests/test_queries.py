"""Stage 9 query tests (QRY-01 to QRY-03, FP-01 to FP-03)."""

from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import appointment_sort_key, select_appointments

P1 = Patient('P1', 'Alex Example')
D1 = Practitioner('D1', 'Taylor Example', 'General')
D2 = Practitioner('D2', 'Morgan Example', 'General')
NINE = datetime(2026, 10, 1, 9, 0)
TEN = datetime(2026, 10, 1, 10, 0)


def make_appointments():
    """Fresh unsorted synthetic appointments with mixed statuses."""
    return [
        Appointment('A3', P1, D1, TEN),
        Appointment('A2', P1, D1, NINE, AppointmentStatus.COMPLETED),
        Appointment('A1', P1, D1, NINE, AppointmentStatus.CANCELLED),
        Appointment('B1', P1, D2, NINE),
    ]


def test_sort_key_returns_date_time_then_id():
    """TEST-Q01 / FP-03: named key is (date_time, appointment_id)."""
    appointment = Appointment('A1', P1, D1, NINE)
    assert appointment_sort_key(appointment) == (NINE, 'A1')


def test_only_requested_practitioner_is_selected():
    """TEST-Q02 / QRY-01: D2 appointment acts as the control."""
    result = select_appointments(make_appointments(), 'D1')
    assert [a.appointment_id for a in result] == ['A1', 'A2', 'A3']
    assert all(a.practitioner is D1 for a in result)


def test_default_status_includes_every_status():
    """TEST-Q03 / QRY-02: None keeps scheduled, cancelled and completed."""
    result = select_appointments(make_appointments(), 'D1')
    assert {a.status for a in result} == set(AppointmentStatus)


def test_explicit_status_filter_and_no_match():
    """TEST-Q04 / QRY-02: each enum filters; no match gives []."""
    appointments = make_appointments()
    scheduled = select_appointments(
        appointments, 'D1', AppointmentStatus.SCHEDULED,
    )
    cancelled = select_appointments(
        appointments, 'D1', AppointmentStatus.CANCELLED,
    )
    completed = select_appointments(
        appointments, 'D1', AppointmentStatus.COMPLETED,
    )
    assert [a.appointment_id for a in scheduled] == ['A3']
    assert [a.appointment_id for a in cancelled] == ['A1']
    assert [a.appointment_id for a in completed] == ['A2']
    assert select_appointments(
        appointments, 'D2', AppointmentStatus.CANCELLED,
    ) == []


def test_orders_by_time_then_id_tie_break():
    """TEST-Q05 / QRY-03: A1 and A2 share 09:00, so ID breaks the tie."""
    result = select_appointments(make_appointments(), 'D1')
    assert [a.appointment_id for a in result] == ['A1', 'A2', 'A3']
    assert result == sorted(result, key=appointment_sort_key)


def test_source_unchanged_and_repeatable():
    """TEST-Q06 / FP-01: source order and fields unchanged; same result."""
    appointments = make_appointments()
    before_order = list(appointments)
    before_fields = [
        (a.appointment_id, a.date_time, a.status) for a in appointments
    ]
    first = select_appointments(appointments, 'D1')
    second = select_appointments(appointments, 'D1')
    assert appointments == before_order
    assert [
        (a.appointment_id, a.date_time, a.status) for a in appointments
    ] == before_fields
    assert first == second


def test_returns_new_list_for_empty_sorted_and_unsorted():
    """TEST-Q07 / FP-02: always a distinct list holding the same objects."""
    empty = []
    unsorted = make_appointments()
    already_sorted = select_appointments(unsorted, 'D1')
    for source in (empty, unsorted, already_sorted):
        result = select_appointments(source, 'D1')
        assert result is not source
    assert select_appointments(already_sorted, 'D1')[0] is already_sorted[0]