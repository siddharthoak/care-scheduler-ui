"""Patient-facing form validation for the care-scheduler platform.

A stand-in for the real UI layer in this demo project -- validates and
formats booking/cancellation input before it's sent to care-scheduler-api.
No actual browser/frontend framework, to keep this repo dependency-light
for a multi-repo AI pipeline (Driftbridge) demo.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class FormValidationError(Exception):
    pass


@dataclass
class BookingForm:
    patient_id: str
    provider_id: str
    start_time: str  # ISO 8601, as a real form field would submit it
    reason_for_visit: str = ""
    errors: list[str] = field(default_factory=list)

    def validate(self) -> bool:
        self.errors = []
        if not self.patient_id.strip():
            self.errors.append("patient_id is required")
        if not self.provider_id.strip():
            self.errors.append("provider_id is required")
        if not self.start_time.strip():
            self.errors.append("start_time is required")
        return not self.errors

    def to_payload(self) -> dict:
        if not self.validate():
            raise FormValidationError("; ".join(self.errors))
        return {
            "patient_id": self.patient_id,
            "provider_id": self.provider_id,
            "start_time": self.start_time,
            "reason_for_visit": self.reason_for_visit,
        }


@dataclass
class CancelForm:
    appointment_id: str
    cancellation_reason: str = ""
    errors: list[str] = field(default_factory=list)

    def validate(self) -> bool:
        self.errors = []
        if not self.appointment_id.strip():
            self.errors.append("appointment_id is required")
        trimmed_reason = self.cancellation_reason.strip()
        if not trimmed_reason:
            self.errors.append("cancellation_reason is required")
        elif len(trimmed_reason) > 200:
            self.errors.append("cancellation_reason cannot exceed 200 characters")
        return not self.errors

    def to_payload(self) -> dict:
        if not self.validate():
            raise FormValidationError("; ".join(self.errors))
        return {
            "appointment_id": self.appointment_id,
            "cancellation_reason": self.cancellation_reason.strip(),
        }
