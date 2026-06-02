"""Pre-download every model needed by extract_figures_from_pdf into a single
portable cache folder, for use in an offline / air-gapped sandbox.

Usage:
    python prefetch_models.py [TARGET_DIR]   # default: ./model_cache

This warms two caches under TARGET_DIR:
  - huggingface/  : the PubLayNet EfficientDet checkpoint (HuggingFace mirror)
  - torch/        : effdet's base weights (torch hub)

Copy TARGET_DIR into the sandbox, then before running set:
    export HF_HOME="<sandbox>/model_cache/huggingface"
    export TORCH_HOME="<sandbox>/model_cache/torch"
    export HF_HUB_OFFLINE=1
    export TRANSFORMERS_OFFLINE=1
"""
import os
import sys

# Cache env vars MUST be set before torch / huggingface_hub are imported.
target = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "model_cache")
os.environ["HF_HOME"] = os.path.join(target, "huggingface")
os.environ["TORCH_HOME"] = os.path.join(target, "torch")
os.makedirs(os.environ["HF_HOME"], exist_ok=True)
os.makedirs(os.environ["TORCH_HOME"], exist_ok=True)


def main():
    from openchemie import OpenChemIE

    print(f"Warming model caches into: {target}")
    print(f"  HF_HOME    = {os.environ['HF_HOME']}")
    print(f"  TORCH_HOME = {os.environ['TORCH_HOME']}")

    # Instantiating the pdf parser runs the exact runtime code path, so both
    # the HuggingFace checkpoint and the effdet torch-hub weights get cached.
    model = OpenChemIE(device="cpu")
    _ = model.pdfparser
    print("\nAll figure-extraction models downloaded and cached.")
    print("Copy the folder above into your sandbox and set HF_HOME / TORCH_HOME "
          "(plus HF_HUB_OFFLINE=1) to point at it.")


if __name__ == "__main__":
    main()
