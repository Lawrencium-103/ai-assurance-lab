# Lab 2 results: lineage and licence inheritance

Run in Google Colab, October 2026. Model cards change over time, so a rerun may differ.

## Case 1: a quantized copy of Llama 3.1 (clean)

```
bartowski/Meta-Llama-3.1-8B-Instruct-GGUF  licence = llama3.1
    meta-llama/Meta-Llama-3.1-8B-Instruct  licence = llama3.1
        meta-llama/Meta-Llama-3.1-8B  licence = llama3.1
No licence conflict in the metadata chain.
```

The GGUF file declares its parent, the parent declares its own parent, and the licence stays the same at every step. The metadata alone is enough to trace this model back to Meta's base release.

## Case 2: DeepSeek-R1-Distill-Llama-8B (gap between metadata and text)

Metadata:

```
deepseek-ai/DeepSeek-R1-Distill-Llama-8B  licence = mit
No licence conflict in the metadata chain.
```

Card text (excerpt from the lines mentioning Llama):

```
> | DeepSeek-R1-Distill-Llama-8B  | [Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | ...
> - DeepSeek-R1-Distill-Llama-8B is derived from Llama3.1-8B-Base and is originally
>   licensed under [llama3.1 license](https://huggingface.co/meta-llama/Llama-3.1-8B/blob/main/LICENSE).
```

Summary:

```
Metadata names a Llama ancestor: False
Card text mentions Llama:        True
GAP: lineage appears only in the card text, not in the metadata.
```

### Finding

DeepSeek-R1-Distill-Llama-8B declares an MIT licence in its Hugging Face metadata and lists no base model. Its model card text states that it is derived from Llama 3.1-8B-Base and originally licensed under the Llama 3.1 licence. An automated check of the metadata reports no licence conflict, while the card text shows an inherited licence with its own terms. A procurement process that relies on metadata alone would miss this. Requiring a machine-readable bill of materials with declared ancestry (for example a CycloneDX ML-BOM with `pedigree.ancestors`) would surface it.

### Open question

The Llama 3.1 licence includes naming and attribution terms for models built from Llama. Whether and how those terms apply to this distilled model is a legal question this lab does not answer. It is recorded here as something a procurement review should check, not as a conclusion.

## Notes on the method

- The text search found 11 lineage phrases. Several were false positives, such as the heading "Distilled Model Evaluation". A keyword match is a lead to check, not a finding.
- The search pattern stops at the first full stop, so "derived from Llama3.1-8B-Base" was cut to "derived from Llama3". Version numbers break simple sentence patterns. The script now also prints every full line that mentions Llama, which caught the complete sentence.
