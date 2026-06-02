# ReactionImageExtractor

A fork of [OpenChemIE](https://github.com/CrystalEye42/OpenChemIE) focused on **extracting figures from chemistry PDFs**, modernized to run on **Python 3.12**.

This fork keeps only the figure-extraction functionality. Given a PDF from the
chemistry literature, it locates the figures on each page and returns them as
cropped images together with their bounding boxes and page numbers, using a
PubLayNet-trained EfficientDet layout-detection model.

> **Scope:** The upstream molecule/reaction/coreference/NER models
> (MolScribe, RxnScribe, MolDetect, ChemNER, ChemRxnExtractor) are **not
> maintained or supported in this fork**. Their imports are loaded lazily, so
> figure extraction works without installing that ML stack. If you need those
> models, use upstream OpenChemIE.

## Installation

This fork targets **Python 3.9+** and is tested on **Python 3.12**.

```bash
# 1. Create and activate a virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# 2. Install PyTorch (CPU build shown; use the CUDA index for GPU)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 3. Install this package + figure-extraction dependencies
pip install 'ReactionImageExtractor @ git+https://github.com/scify/ReactionImageExtractor'
```

For local development, clone and install as editable instead:

```bash
git clone https://github.com/scify/ReactionImageExtractor.git
cd ReactionImageExtractor
pip install --editable .
```

**Poppler** is required by `pdf2image`. If it is not already installed, follow
the [installation instructions](https://github.com/jalan/pdftotext#os-dependencies)
for your OS (e.g. `sudo apt install poppler-utils` on Debian/Ubuntu).

### Layout-detection model checkpoint

The PubLayNet EfficientDet checkpoint (~80 MB) is downloaded automatically on
first use and cached by `huggingface_hub` for subsequent runs — no manual setup
is required.

> Note: `layoutparser`'s original model catalog points the checkpoint at a dead
> Dropbox link that now serves an HTML page (the classic symptom is
> `invalid load key, '<'`). This fork sidesteps that by fetching the checkpoint
> from the [HuggingFace mirror](https://huggingface.co/layoutparser/efficientdet)
> instead, inside `init_pdfparser`.

### Offline / air-gapped usage

Figure extraction needs two model files at runtime (~103 MB total):

| File | Source | Cache location |
|------|--------|----------------|
| `publaynet-tf_efficientdet_d1.pth.tar` (~80 MB) | HuggingFace `layoutparser/efficientdet` | `$HF_HOME` |
| `tf_efficientdet_d1_40-a30f94af.pth` (~27 MB) | effdet release (torch hub) | `$TORCH_HOME` |

To run on a machine with no internet access, pre-download both into one
portable folder **on a connected machine** using the included script:

```bash
python prefetch_models.py model_cache    # downloads into ./model_cache
```

Copy `model_cache/` into the sandbox, then point the caches at it and enable
offline mode before running:

```bash
export HF_HOME="$PWD/model_cache/huggingface"
export TORCH_HOME="$PWD/model_cache/torch"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
```

With those set, `extract_figures_from_pdf` runs with no network access. (Note:
the Python dependencies themselves must also be installed offline — e.g. build
a wheelhouse with `pip download` and `pip install --no-index`.)

## Usage

```python
from openchemie import OpenChemIE

model = OpenChemIE(device="cpu")  # change to "cuda" for GPU
pdf_path = "example/acs.joc.2c00749.pdf"  # path to your PDF

figures = model.extract_figures_from_pdf(
    pdf_path,
    num_pages=None,      # or an int to process only the first N pages
    output_bbox=True,
    output_image=True,
)
```

- [`extract_figures_from_pdf`](https://github.com/scify/ReactionImageExtractor/blob/main/openchemie/interface.py#L181)

### Output format

```
[
    {   # first figure
        'title': {
            'text': str,
            'bbox': list in form [x1, y1, x2, y2],
        },
        'figure': {
            'image': PIL image or None,   # None if output_image=False
            'bbox': list in form [x1, y1, x2, y2],
        },
        'table': {
            'bbox': list in form [x1, y1, x2, y2] or empty list,
            'content': {
                'columns': list of column headers,
                'rows': list of list of row content,
            } or None
        },
        'footnote': str or empty,
        'page': int
    },
    # more figures
]
```

### Example / smoke test

A runnable example is included that extracts figures from the bundled sample
PDF, prints a summary, and saves the cropped images to
`example/extracted_figures/`:

```bash
PYTHONPATH=. python example/test_extract_figures.py
```

## Loading a custom checkpoint

To use a different layout-detection checkpoint, pass its path to the init method:

```python
from openchemie import OpenChemIE

model = OpenChemIE(device="cpu")
model.init_pdfparser("/path/to/checkpoint.pth.tar")
```

## Attribution

This is a fork of **OpenChemIE** by Yujie Qian, Alex Wang, Vincent Fan,
Amber Wang, and Regina Barzilay *(MIT CSAIL)*. If you use this work in your
research, please cite the original [paper](https://arxiv.org/abs/2404.01462):

```
@misc{fan2024openchemie,
      title={OpenChemIE: An Information Extraction Toolkit For Chemistry Literature},
      author={Vincent Fan and Yujie Qian and Alex Wang and Amber Wang and Connor W. Coley and Regina Barzilay},
      year={2024},
      eprint={2404.01462},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

The figure layout detection uses a PubLayNet-trained EfficientDet model via
[LayoutParser](https://github.com/Layout-Parser/layout-parser).
