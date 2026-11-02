# Lab 5 results: personal data detection

Run in Google Colab, October 2026, with Presidio and spaCy `en_core_web_sm`. All records are synthetic.

```
  NG_PHONE       score=0.95  '08031234567'
  LOCATION       score=0.85  'Ikeja'
  NG_NIN         score=0.65  '12345678901'
  NG_NIN         score=0.65  '08031234567'
  -> Complaint from Adebayo Okafor, NIN <NG_NIN>, phone <NG_PHONE>, lives at 14 Allen Avenue, <LOCATION>.

  EMAIL_ADDRESS  score=1.00  'chioma.eze@example.com'
  PERSON         score=0.85  'Mrs Chioma Eze'
  -> <PERSON> (<EMAIL_ADDRESS>) says her pension has not been paid since March.

  -> Caller asked about passport renewal. No personal details given.
```

## Finding

The scan caught the NIN, the phone number, the email address and "Mrs Chioma Eze", and correctly left the third record unchanged. It missed two things in the first record:

- **The name "Adebayo Okafor" was not detected.** The small English spaCy model did not recognise it as a person, so it would have been sent to the vendor in clear text.
- **The street address "14 Allen Avenue" was not detected.** Only the area name "Ikeja" was redacted.

The phone number was also flagged as a possible NIN, because both are 11 digits. In this case it was still redacted, but the overlap would make any count of "NINs found" unreliable.

An automated scan of this kind is a first filter. On this evidence it is not enough on its own before citizen data leaves a ministry: a human review step or a better-tuned model is needed.

## Next

- Rerun with `en_core_web_lg` and compare.
- Build a larger synthetic set with Yoruba, Igbo, Hausa and other Nigerian names and addresses, and measure the miss rate for each model.
- Add a recogniser for Nigerian street addresses.

## About the warnings

Presidio prints warnings that Spanish, Italian and Polish recognisers were not added, and that the `PERCENT` entity is unmapped. These are expected when only English is configured and do not affect the results.
