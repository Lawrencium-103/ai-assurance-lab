# AI Assurance Lab

Hands-on checks a public institution can run before buying or deploying an AI model: reading model cards, tracing where a model came from, grading how open it really is, documenting its components, and testing whether personal data leaks.

I'm working through these labs to build practical skills in AI procurement and data protection, with a focus on Nigeria and the Nigeria Data Protection Act (NDPA). This repository records the code, the raw results and what I concluded from them, including what didn't work.

## Status

| Lab | Topic | Status |
| --- | --- | --- |
| 1 | Reading model cards | In progress (1 of 3 models recorded) |
| 2 | Model lineage and licence inheritance | Done |
| 3 | Openness grading: open-source, open-weight, open-washed | Run; evidence still being verified |
| 4 | AI bill of materials (CycloneDX ML-BOM) | Done; checksum step to rerun |
| 5 | Detecting personal data before it reaches a vendor | Done on 3 records; larger test planned |
| 6 | Red-teaming a chatbot for data leakage | Not started |
| 7 | Benchmarking a small model | Not started |

## Findings so far

**1. Model metadata can say a model has no ancestors while its own documentation says otherwise.**

DeepSeek-R1-Distill-Llama-8B declares an MIT licence in its Hugging Face metadata and lists no base model. Its model card text states that it is derived from Llama 3.1-8B-Base and originally licensed under the Llama 3.1 licence. An automated licence check reading only the metadata finds no conflict. By contrast, `bartowski/Meta-Llama-3.1-8B-Instruct-GGUF`, a quantized copy of Llama 3.1, declares its full chain back to Meta's base model with the same licence at every step.

For procurement, metadata is not enough. A buyer should require a machine-readable bill of materials that declares every ancestor model, and check it against the model card. See [results/lab2_lineage.md](results/lab2_lineage.md).

**2. In a three-record test, an open-source PII scanner missed a Nigerian name and a street address.**

Presidio with the small English spaCy model redacted a NIN, a phone number, an email and the name "Mrs Chioma Eze", but let "Adebayo Okafor" and "14 Allen Avenue" through unchanged. Three records show that misses happen, not how often; a larger test with Nigerian names is the next step. Out-of-the-box tools should not be the only safeguard before citizen data is sent to an AI vendor. See [results/lab5_pii_scan.md](results/lab5_pii_scan.md).

**3. A procurement-style ML-BOM can be written and validated with free tools.**

An example CycloneDX 1.6 ML-BOM recording a model's ancestry, licences, limitations and fine-tuning data validates against the official schema. See [results/lab4_aibom.md](results/lab4_aibom.md) and [results/ai-bom.json](results/ai-bom.json).

## Run it

Python 3.10+ or Google Colab. No GPU needed.

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
huggingface-cli login        # read token from huggingface.co/settings/tokens

python labs/lab1_model_cards.py
python labs/lab2_lineage.py deepseek-ai/DeepSeek-R1-Distill-Llama-8B
python labs/lab3_openness.py
python labs/lab4_aibom.py --checksum
python labs/lab5_pii_scan.py
```

Meta's Llama repositories are gated. Request access on the model page first, or the scripts will report the card as unreadable.

## Repository layout

```
labs/
  lab1_model_cards.py   read card metadata, keyword-check key sections
  lab2_lineage.py       trace base_model chain, compare with card text
  lab3_openness.py      grade releases from yes/no evidence
  lab4_aibom.py         write and validate a CycloneDX ML-BOM; verify a SHA-256
  lab5_pii_scan.py      detect and redact personal data in synthetic records
results/
  lab1_model_cards.md
  lab2_lineage.md
  lab3_openness.md
  lab4_aibom.md
  lab5_pii_scan.md
  ai-bom.json
```

## Limitations

- Model cards are edited over time. Results are dated and may not reproduce exactly.
- The section checks in Lab 1 are keyword matches. They show whether a topic is mentioned, not whether it is covered properly.
- The Lab 3 grades are only as good as their yes/no inputs, which are still being checked against sources.
- The Lab 5 test uses three records. It shows that misses happen, not how often.
- Nothing here is legal advice. Where a licence question comes up, it is recorded as an open question.

## Data

These labs use public model cards and synthetic records only. No real personal data is used anywhere in this repository.
