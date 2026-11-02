"""Lab 1: read Hugging Face model cards and check which key sections they cover.

Usage:
    python labs/lab1_model_cards.py
    python labs/lab1_model_cards.py allenai/OLMo-2-1124-7B mistralai/Mistral-7B-v0.1

Gated models (such as Meta's Llama) need a Hugging Face token with access granted:
    huggingface-cli login
"""

import sys
from huggingface_hub import ModelCard

DEFAULT_MODELS = [
    "allenai/OLMo-2-1124-7B",
    "mistralai/Mistral-7B-v0.1",
    "meta-llama/Llama-3.1-8B",
]

# Keyword checks. A match means the topic is mentioned, not that it is covered well.
CHECKS = {
    "Intended use": ["intended use", "use case", "out-of-scope"],
    "Training data": ["training data", "pretraining data", "dataset"],
    "Evaluation": ["evaluation", "benchmark"],
    "Limitations / bias": ["limitation", "bias", "risk"],
    "Environmental cost": ["carbon", "co2", "emission", "gpu hours"],
}


def read_card(repo_id):
    try:
        card = ModelCard.load(repo_id)
    except Exception as e:
        print(f"=== {repo_id} ===")
        print(f"Could not read card ({type(e).__name__}). It may be gated: "
              f"https://huggingface.co/{repo_id}\n")
        return None

    meta = card.data.to_dict()
    print(f"=== {repo_id} ===")
    for label, key in [("Licence", "license"), ("Base model", "base_model"),
                       ("Datasets", "datasets"), ("Languages", "language"),
                       ("Task", "pipeline_tag")]:
        print(f"{label + ':':13} {meta.get(key)}")
    return card


def audit_sections(card):
    text = card.text.lower()
    for section, words in CHECKS.items():
        found = any(w in text for w in words)
        print(f"  {'FOUND  ' if found else 'MISSING'}  {section}")


if __name__ == "__main__":
    models = sys.argv[1:] or DEFAULT_MODELS
    for repo in models:
        card = read_card(repo)
        if card is not None:
            audit_sections(card)
        print()
