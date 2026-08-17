import pytest

from forms import BookingForm, CancelForm, FormValidationError


def test_booking_form_valid_payload():
    form = BookingForm(patient_id="p1", provider_id="prov1", start_time="2026-09-01T10:00:00")
    assert form.to_payload() == {
        "patient_id": "p1",
        "provider_id": "prov1",
        "start_time": "2026-09-01T10:00:00",
        "reason_for_visit": "",
    }


def test_booking_form_missing_fields_raises():
    form = BookingForm(patient_id="", provider_id="prov1", start_time="")
    with pytest.raises(FormValidationError):
        form.to_payload()


def test_cancel_form_valid_payload():
    form = CancelForm(appointment_id="a1")
    assert form.to_payload() == {"appointment_id": "a1"}


def test_cancel_form_missing_id_raises():
    form = CancelForm(appointment_id="")
    with pytest.raises(FormValidationError):
        form.to_payload()
