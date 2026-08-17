# care-scheduler-ui

Patient-facing form validation for the care-scheduler platform -- validates
and formats booking/cancellation input before it's sent to
care-scheduler-api. No real browser/frontend framework, to keep this repo
dependency-light for a multi-repo AI pipeline (Driftbridge) demo.

One of four repos in a multi-repo Driftbridge demo:

- [care-scheduler-db](https://github.com/siddharthoak/care-scheduler-db) -- data models + repository
- [care-scheduler-api](https://github.com/siddharthoak/care-scheduler-api) -- booking/cancellation logic
- **care-scheduler-ui** (this repo) -- patient-facing forms
- [care-scheduler-notify](https://github.com/siddharthoak/care-scheduler-notify) -- appointment notifications

Run tests: `pytest`
