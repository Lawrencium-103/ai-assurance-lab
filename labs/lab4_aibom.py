"""Lab 4: write a CycloneDX 1.6 ML-BOM for an example procurement, validate it,
and optionally pin a model file by its SHA-256 hash.

Usage:
    pip install "cyclonedx-python-lib[validation]"
    python labs/lab4_aibom.py              # write and validate results/ai-bom.json
    python labs/lab4_aibom.py --checksum   # also verify a model file's SHA-256
"""

import hashlib
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "results" / "ai-bom.json"

BOM = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.6",
    "version": 1,
    "metadata": {
        "timestamp": "2026-10-31T00:00:00Z",
        "component": {"type": "application",
                      "name": "Ministry citizen helpdesk chatbot", "version": "0.1"},
    },
    "components": [
        {
            "type": "machine-learning-model",
            "bom-ref": "model-helpdesk",
            "name": "helpdesk-llama-8b",
            "version": "1.0",
            "supplier": {"name": "Example Vendor Ltd"},
            "licenses": [{"license": {"name": "Llama 3.1 Community License"}}],
            "pedigree": {
                "ancestors": [{
                    "type": "machine-learning-model",
                    "name": "meta-llama/Llama-3.1-8B-Instruct",
                    "licenses": [{"license": {"name": "Llama 3.1 Community License"}}],
                    "externalReferences": [{
                        "type": "website",
                        "url": "https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct"}],
                }]
            },
            "modelCard": {
                "modelParameters": {
                    "task": "text-generation",
                    "architectureFamily": "transformer",
                    "datasets": [{"ref": "data-ft"}],
                },
                "considerations": {
                    "users": ["Ministry helpdesk staff", "Citizens"],
                    "useCases": ["Answering questions about public services"],
                    "technicalLimitations": ["May give wrong answers about eligibility rules"],
                    "ethicalConsiderations": [{
                        "name": "Citizen personal data in prompts",
                        "mitigationStrategy": "PII redaction before prompts leave the ministry network",
                    }],
                },
            },
        },
        {
            "type": "data",
            "bom-ref": "data-ft",
            "name": "helpdesk-finetune-set",
            "data": [{"type": "dataset",
                      "name": "Anonymised helpdesk transcripts 2025",
                      "classification": "confidential"}],
        },
    ],
}


def write_and_validate():
    from cyclonedx.validation.json import JsonStrictValidator
    from cyclonedx.schema import SchemaVersion

    OUT.write_text(json.dumps(BOM, indent=2))
    errors = JsonStrictValidator(SchemaVersion.V1_6).validate_str(OUT.read_text())
    print(f"Wrote {OUT.name}:", "valid CycloneDX 1.6" if errors is None else errors)


def verify_checksum(repo="HuggingFaceTB/SmolLM2-135M-Instruct", fname="model.safetensors"):
    from huggingface_hub import HfApi, hf_hub_download

    info = HfApi().model_info(repo, files_metadata=True)
    sibling = next(s for s in info.siblings if s.rfilename == fname)
    lfs = sibling.lfs
    expected = lfs.sha256 if hasattr(lfs, "sha256") else lfs["sha256"]

    h = hashlib.sha256()
    with open(hf_hub_download(repo, fname), "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    actual = h.hexdigest()

    print("Published SHA-256:", expected)
    print("Computed SHA-256: ", actual)
    print("MATCH" if actual == expected else "MISMATCH: do not deploy this file")


if __name__ == "__main__":
    write_and_validate()
    if "--checksum" in sys.argv:
        verify_checksum()
