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
    form = CancelForm(appointment_id="a1", reason="scheduling conflict")
    assert form.to_payload() == {
        "appointment_id": "a1",
        "reason": "scheduling conflict",
    }


def test_cancel_form_missing_id_raises():
    form = CancelForm(appointment_id="", reason="scheduling conflict")
    with pytest.raises(FormValidationError):
        form.to_payload()


def test_cancel_form_missing_reason_raises():
    form = CancelForm(appointment_id="a1", reason="")
    with pytest.raises(FormValidationError):
        form.to_payload()

    form2 = CancelForm(appointment_id="a1", reason="   ")
    with pytest.raises(FormValidationError):
        form2.to_payload()


def test_cancel_form_placeholder_reasons_raise():
    placeholders = ["placeholder", "none", "n/a", "na", "no reason", "blank", "test", "tbd", "temp", "null", "undefined"]
    for placeholder in placeholders:
        form = CancelForm(appointment_id="a1", reason=placeholder)
        with pytest.raises(FormValidationError) as excinfo:
            form.to_payload()
        assert "reason cannot be a placeholder" in str(excinfo.value)

        # case-insensitive check
        form_caps = CancelForm(appointment_id="a1", reason=placeholder.upper())
        with pytest.raises(FormValidationError):
            form_caps.to_payload()


def test_cancel_form_punctuation_only_reasons_raise():
    punctuations = ["-", "...", "???", "!!!", " - - "]
    for punc in punctuations:
        form = CancelForm(appointment_id="a1", reason=punc)
        with pytest.raises(FormValidationError) as excinfo:
            form.to_payload()
        assert "reason cannot be a placeholder" in str(excinfo.value)


def test_cancel_form_placeholder_variations_raise():
    for reason_val in ["  none  ", "   TBD   ", " - - "]:
        form = CancelForm(appointment_id="a1", reason=reason_val)
        with pytest.raises(FormValidationError):
            form.to_payload()


