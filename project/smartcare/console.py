"""Console helpers and a small runnable starting demonstration."""


import re
from datetime import datetime
from typing import Final

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)

MENU: Final[str] = (
    '\nSmartCare menu\n'
    '1. Register patient\n'
    '2. Find patient\n'
    '3. Register practitioner\n'
    '4. Find practitioner\n'
    '5. Book appointment\n'
    '6. Cancel appointment\n'
    '7. Find appointment\n'
    '8. List practitioner appointments\n'
    '0. Exit'
)

def parse_date_time(text: str) -> datetime:
    """Parse YYYY-MM-DD HH:MM; raise ValueError for invalid input."""
    if (
        not isinstance(text, str)
        or re.fullmatch(
            '[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', text
        ) is None
    ):
        raise ValueError('Use date/time format YYYY-MM-DD HH:MM')
    try:
        return datetime.strptime(text, '%Y-%m-%d %H:%M')
    except ValueError:
        raise ValueError(
            'Invalid calendar date/time; use YYYY-MM-DD HH:MM',
        ) from None


def parse_status(text: str) -> AppointmentStatus | None:
    """Convert status text to an enum; blank means every status."""
    cleaned: str = text.strip().lower()
    if not cleaned:
        return None
    try:
        return AppointmentStatus(cleaned)
    except ValueError:
        raise ValueError(
            'Status must be blank, scheduled, cancelled or completed',
        ) from None

def format_appointment(appointment: Appointment) -> str:
    """Return readable synthetic appointment details without changing
    state.
    """
    return (
        f'{appointment.appointment_id}: '
        f'{appointment.patient.patient_id} with '
        f'{appointment.practitioner.practitioner_id}, '
        f'{appointment.date_time:%Y-%m-%d %H:%M}, {appointment.status.value}'
    )


def run_demo() -> None:
    """Demonstrate supplied registration and booking using synthetic
    records.
    """
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    patients.register_patient('P1', 'Alex Example')
    practitioners.register_practitioner(
        'DR1',
        'Taylor Example',
        'General practice',
    )
    try:
        appointments.book_appointment(
            'A1',
            'P1',
            'DR1',
            parse_date_time('2026-10-01 09:00'),
        )
        print(format_appointment(appointments.find_appointment('A1')))
    except (ValueError, LookupError) as error:
        print(f'Error: {error}')
    print('Session-only data: records are lost on exit.')


def run_menu() -> None:
    """Run the register/find/book/cancel/list/exit menu.

    One store and one set of services last for the whole session.
    Expected ValueError and LookupError messages are shown and the
    menu continues without partial state changes.
    """
    data_store: SmartCareDataStore = SmartCareDataStore()
    patients: PatientService = PatientService(data_store)
    practitioners: PractitionerService = PractitionerService(data_store)
    appointments: AppointmentService = AppointmentService(data_store)

    while True:
        print(MENU)
        try:
            choice: str = input('Choose an option: ').strip()
        except EOFError:
            # End of piped input is treated as exit.
            choice = '0'

        if choice == '0':
            print('Goodbye. Session-only data: records are lost on exit.')
            break

        try:
            if choice == '1':
                patient_id: str = input('Patient ID: ')
                name: str = input('Patient name: ')
                patient = patients.register_patient(patient_id, name)
                print(f'Registered patient {patient.patient_id}: {patient.name}')
            elif choice == '2':
                patient = patients.find_patient(input('Patient ID: '))
                print(f'Found patient {patient.patient_id}: {patient.name}')
            elif choice == '3':
                practitioner_id: str = input('Practitioner ID: ')
                name = input('Practitioner name: ')
                specialty: str = input('Specialty: ')
                practitioner = practitioners.register_practitioner(
                    practitioner_id,
                    name,
                    specialty,
                )
                print(
                    f'Registered practitioner {practitioner.practitioner_id}: '
                    f'{practitioner.name} ({practitioner.specialty})',
                )
            elif choice == '4':
                practitioner = practitioners.find_practitioner(
                    input('Practitioner ID: '),
                )
                print(
                    f'Found practitioner {practitioner.practitioner_id}: '
                    f'{practitioner.name} ({practitioner.specialty})',
                )
            elif choice == '5':
                appointment_id: str = input('Appointment ID: ')
                patient_id = input('Patient ID: ')
                practitioner_id = input('Practitioner ID: ')
                # Parse the date first so bad input changes nothing.
                date_time: datetime = parse_date_time(
                    input('Date/time (YYYY-MM-DD HH:MM): '),
                )
                appointment = appointments.book_appointment(
                    appointment_id,
                    patient_id,
                    practitioner_id,
                    date_time,
                )
                print(f'Booked {format_appointment(appointment)}')
            elif choice == '6':
                appointment = appointments.cancel_appointment(
                    input('Appointment ID: '),
                )
                print(f'Cancelled {format_appointment(appointment)}')
            elif choice == '7':
                appointment = appointments.find_appointment(
                    input('Appointment ID: '),
                )
                print(format_appointment(appointment))
            elif choice == '8':
                practitioner_id = input('Practitioner ID: ')
                # Convert text to the enum here, at the console boundary.
                status: AppointmentStatus | None = parse_status(
                    input('Status (blank, scheduled, cancelled, completed): '),
                )
                results: list[Appointment] = (
                    appointments.list_practitioner_appointments(
                        practitioner_id,
                        status,
                    )
                )
                if not results:
                    print('No matching appointments.')
                for appointment in results:
                    print(format_appointment(appointment))
            else:
                print('Unknown option; choose 0-8.')
        except (ValueError, LookupError) as error:
            print(f'Error: {error}')
