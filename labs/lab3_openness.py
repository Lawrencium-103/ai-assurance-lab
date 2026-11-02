"""Lab 3: grade a model release as open-source, open-weight, open-washed or closed.

The yes/no inputs below must be checked against each model's card, repository
and technical report. They are the evidence; the grade only follows from them.

Usage:
    python labs/lab3_openness.py
"""

from dataclasses import dataclass


@dataclass
class Release:
    name: str
    weights: bool             # downloadable without a custom agreement
    training_code: bool       # code used to train the model is published
    training_data: bool       # data published, or described well enough to rebuild
    tech_report: bool         # paper or report on how it was built
    osi_licence: bool         # OSI-approved licence with no use restrictions
    claims_open_source: bool  # makers describe it as "open source"


def grade(r: Release):
    if not r.weights:
        return "Closed", ["weights not downloadable"]
    if r.training_code and r.training_data and r.osi_licence:
        return "Open-source", ["weights, code, data and licence all open"]
    reasons = []
    if not r.training_code:
        reasons.append("no training code")
    if not r.training_data:
        reasons.append("no training data")
    if not r.osi_licence:
        reasons.append("restrictive or custom licence")
    if r.claims_open_source:
        return "Open-washed", reasons + ["marketed as open source anyway"]
    return "Open-weight", reasons


MODELS = [
    Release("OLMo-2-1124-7B", True, True, True, True, True, True),
    Release("Mistral-7B-v0.1", True, False, False, True, True, False),
    Release("Llama-3.1-8B", True, False, False, True, False, True),
]

if __name__ == "__main__":
    for m in MODELS:
        g, why = grade(m)
        print(f"{m.name:18} {g:12} because: {', '.join(why)}")
