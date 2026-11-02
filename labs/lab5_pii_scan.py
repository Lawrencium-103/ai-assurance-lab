"""Lab 5: detect and redact personal data in synthetic Nigerian records before
they are sent to an AI vendor.

Usage:
    pip install presidio-analyzer presidio-anonymizer
    python -m spacy download en_core_web_sm
    python labs/lab5_pii_scan.py

All records are invented. Never run real citizen data through test code.
"""

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine

SPACY_MODEL = "en_core_web_sm"  # try en_core_web_lg for comparison

RECORDS = [
    "Complaint from Adebayo Okafor, NIN 12345678901, phone 08031234567, "
    "lives at 14 Allen Avenue, Ikeja.",
    "Mrs Chioma Eze (chioma.eze@example.com) says her pension has not "
    "been paid since March.",
    "Caller asked about passport renewal. No personal details given.",
]
ENTITIES = ["PERSON", "EMAIL_ADDRESS", "LOCATION", "NG_PHONE", "NG_NIN"]


def build_analyzer():
    provider = NlpEngineProvider(nlp_configuration={
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": SPACY_MODEL}],
    })
    analyzer = AnalyzerEngine(nlp_engine=provider.create_engine(),
                              supported_languages=["en"])
    analyzer.registry.add_recognizer(PatternRecognizer(
        supported_entity="NG_PHONE",
        patterns=[Pattern("ng_phone", r"(?:\+234|0)[789][01]\d{8}\b", 0.6)],
        context=["phone", "call", "mobile", "whatsapp", "number"],
    ))
    analyzer.registry.add_recognizer(PatternRecognizer(
        supported_entity="NG_NIN",
        patterns=[Pattern("ng_nin", r"\b\d{11}\b", 0.3)],
        context=["nin", "nimc", "identity", "identification"],
    ))
    return analyzer


if __name__ == "__main__":
    analyzer = build_analyzer()
    anonymizer = AnonymizerEngine()
    for text in RECORDS:
        found = analyzer.analyze(text=text, language="en", entities=ENTITIES)
        for r in found:
            print(f"  {r.entity_type:14} score={r.score:.2f}  '{text[r.start:r.end]}'")
        print("  ->", anonymizer.anonymize(text=text, analyzer_results=found).text, "\n")
