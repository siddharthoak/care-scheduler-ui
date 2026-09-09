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
    form = CancelForm(appointment_id="a1", cancellation_reason="No longer needed")
    assert form.to_payload() == {
        "appointment_id": "a1",
        "cancellation_reason": "No longer needed",
    }


def test_cancel_form_missing_id_raises():
    form = CancelForm(appointment_id="", cancellation_reason="No longer needed")
    with pytest.raises(FormValidationError) as exc:
        form.to_payload()
    assert "appointment_id is required" in str(exc.value)


def test_cancel_form_missing_reason_raises():
    form = CancelForm(appointment_id="a1", cancellation_reason="")
    with pytest.raises(FormValidationError) as exc:
        form.to_payload()
    assert "cancellation_reason is required" in str(exc.value)


def test_cancel_form_whitespace_reason_raises():
    form = CancelForm(appointment_id="a1", cancellation_reason="   \n\t  ")
    with pytest.raises(FormValidationError) as exc:
        form.to_payload()
    assert "cancellation_reason is required" in str(exc.value)


def test_cancel_form_reason_too_long_raises():
    form = CancelForm(appointment_id="a1", cancellation_reason="a" * 201)
    with pytest.raises(FormValidationError) as exc:
        form.to_payload()
    assert "cancellation_reason cannot exceed 200 characters" in str(exc.value)


def test_cancel_form_reason_exact_length_allowed():
    reason = "a" * 200
    form = CancelForm(appointment_id="a1", cancellation_reason=reason)
    assert form.to_payload() == {
        "appointment_id": "a1",
        "cancellation_reason": reason,
    }


def test_cancel_form_trims_reason():
    form = CancelForm(appointment_id="a1", cancellation_reason="   Schedule conflict   ")
    assert form.to_payload() == {
        "appointment_id": "a1",
        "cancellation_reason": "Schedule conflict",
    }
