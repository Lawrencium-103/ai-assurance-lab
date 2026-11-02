"""Lab 2: trace a model's lineage through Hugging Face metadata and compare it
with what the model card text says.

Usage:
    python labs/lab2_lineage.py bartowski/Meta-Llama-3.1-8B-Instruct-GGUF
    python labs/lab2_lineage.py deepseek-ai/DeepSeek-R1-Distill-Llama-8B
"""

import re
import sys
from huggingface_hub import ModelCard

LINEAGE_PATTERN = (r"[^.\n]*(based on|derived from|fine-tuned from|distilled|built with)"
                   r"[^.\n]*")


def trace(repo_id, depth=0, seen=None):
    """Follow the base_model field upward, printing the licence at each level."""
    seen = seen if seen is not None else set()
    if repo_id in seen or depth > 6:
        return []
    seen.add(repo_id)
    pad = "    " * depth
    try:
        meta = ModelCard.load(repo_id).data.to_dict()
    except Exception:
        print(f"{pad}{repo_id}  [card not readable: gated or missing]")
        return [(repo_id, "unknown")]

    lic = meta.get("license", "not declared")
    print(f"{pad}{repo_id}  licence = {lic}")
    chain = [(repo_id, lic)]
    bases = meta.get("base_model") or []
    if isinstance(bases, str):
        bases = [bases]
    for b in bases:
        chain += trace(b, depth + 1, seen)
    return chain


def flag_conflicts(chain):
    """Report ancestors whose declared licence differs from the top model's."""
    top_repo, top_licence = chain[0]
    conflicts = [(r, l) for r, l in chain[1:] if l not in (top_licence, "unknown")]
    for repo, lic in conflicts:
        print(f"CONFLICT: {top_repo} says '{top_licence}' but ancestor {repo} says '{lic}'")
    if not conflicts:
        print("No licence conflict in the metadata chain.")
    return conflicts


def lineage_in_text(repo_id):
    """Search the human-readable card text for lineage statements."""
    text = ModelCard.load(repo_id).text
    matches = [m.group(0).strip()
               for m in re.finditer(LINEAGE_PATTERN, text, flags=re.IGNORECASE)]
    print(f"Lineage phrases found: {len(matches)}")
    for m in matches:
        print("  -", m)

    # The pattern stops at the first full stop, so version numbers like
    # "Llama3.1" cut sentences short. Print whole lines as a second check.
    print("\nLines mentioning 'llama':")
    for line in text.splitlines():
        if "llama" in line.lower():
            print("  >", line.strip()[:200])
    return text


def compare(repo_id):
    print("METADATA (machine-readable)")
    chain = trace(repo_id)
    flag_conflicts(chain)

    print("\nCARD TEXT (human-readable)")
    text = lineage_in_text(repo_id)

    meta_llama = any("llama" in r.lower() for r, _ in chain[1:])
    text_llama = "llama" in text.lower()
    print("\nSUMMARY")
    print(f"Metadata names a Llama ancestor: {meta_llama}")
    print(f"Card text mentions Llama:        {text_llama}")
    if text_llama and not meta_llama:
        print("GAP: lineage appears only in the card text, not in the metadata.")


if __name__ == "__main__":
    for repo in sys.argv[1:] or ["deepseek-ai/DeepSeek-R1-Distill-Llama-8B"]:
        print(f"\n######## {repo} ########")
        compare(repo)
