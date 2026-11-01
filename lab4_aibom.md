# Lab 4 results: AI bill of materials

Run in Google Colab, October 2026.

## ML-BOM

An example CycloneDX 1.6 ML-BOM for a hypothetical ministry helpdesk chatbot built on Llama 3.1. The file is [ai-bom.json](ai-bom.json).

```
Saved ai-bom.json
Valid ML-BOM
```

It validates against the official CycloneDX 1.6 JSON schema. How the earlier labs map into it:

| Earlier lab | Where it lives in the BOM |
| --- | --- |
| Lineage (Lab 2) | `components[0].pedigree.ancestors` |
| Licence chain (Lab 2) | `licenses` on the model and on each ancestor |
| Limitations from the model card (Lab 1) | `modelCard.considerations.technicalLimitations` |
| Fine-tuning data source | the `data` component, referenced from `modelParameters.datasets` |

The vendor, model and dataset names are invented. This is a template for what a procurement contract could require, not a record of a real system.

## Checksum

The checksum cell was added to the notebook but its output was not recorded. To be rerun with:

```
python labs/lab4_aibom.py --checksum
```

Once it runs, the next step is to add the model file's SHA-256 to the BOM in a `hashes` field so the BOM pins one exact file.
