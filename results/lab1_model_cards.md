# Lab 1 results: model cards

Run in Google Colab, October 2026. Model cards change over time, so a rerun may differ.

## OLMo-2-1124-7B (AllenAI)

```
=== allenai/OLMo-2-1124-7B ===
Licence:       apache-2.0
Base model:    None
Datasets:      ['allenai/dolmino-mix-1124', 'allenai/olmo-mix-1124']
Languages:     ['en']
Task:          None

MISSING  Intended use
FOUND    Training data
FOUND    Evaluation
FOUND    Limitations / bias
MISSING  Environmental cost
```

What this shows:

- The training data is named in the metadata, with links to the actual dataset repositories. Most model cards don't do this.
- No base model is listed, which is consistent with OLMo being trained from scratch.
- "Intended use" and "Environmental cost" were not found by keyword. This only means those exact words are absent; it still needs a manual read of the card to confirm whether the topics are covered under other wording.

## Mistral-7B-v0.1 and Llama-3.1-8B

Not yet recorded. The first run used `Llama-3.1-8B` without the `meta-llama/` prefix and failed before any output. To be rerun with the corrected script.

| Model | Licence | Training data named? | Limitations section? | Verdict on the card |
| --- | --- | --- | --- | --- |
| OLMo-2-1124-7B | Apache 2.0 | Yes, in metadata | Yes (keyword) | Strongest documentation of the three so far |
| Mistral-7B-v0.1 | pending | pending | pending | pending |
| Llama-3.1-8B | pending | pending | pending | pending |
