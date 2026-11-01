# Lab 3 results: openness grading

Run in Google Colab, October 2026.

```
OLMo-2-1124-7B     Open-source  because: weights, code, data and licence all open
Mistral-7B-v0.1    Open-weight  because: no training code, no training data
Llama-3.1-8B       Open-washed  because: no training code, no training data, restrictive or custom licence, marketed as open source anyway
```

## Status of the evidence

These grades come from the starting yes/no values in the lab. They have not yet been checked one by one against each model's card, repository and licence. Until that is done, treat them as provisional.

| Model | Evidence already confirmed in this repo | Still to confirm |
| --- | --- | --- |
| OLMo-2-1124-7B | Apache 2.0 licence; training datasets named in metadata (Lab 1) | Training code repository; technical report |
| Mistral-7B-v0.1 | None yet | Licence; absence of training code and data |
| Llama-3.1-8B | Licence declared as `llama3.1` (Lab 2 trace) | How Meta describes the release; licence restrictions |

## Notes

- Llama is the borderline case. "Open-washed" depends on how its makers describe it and how strictly the licence is read. The grade needs a quoted source for the "claims open source" input before it can stand.
- DeepSeek-R1-Distill-Llama-8B (from Lab 2) is the next model to grade: openly released weights under a declared MIT licence, built on a model with a custom licence.
