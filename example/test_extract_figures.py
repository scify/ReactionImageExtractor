"""Smoke test for OpenChemIE.extract_figures_from_pdf on Python 3.12.

Runs figure extraction on the bundled example PDF (first few pages) and
prints a summary of what was found. Saves any extracted figure images to
example/extracted_figures/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, "acs.joc.2c00749.pdf")
OUT_DIR = os.path.join(HERE, "extracted_figures")


def main():
    from openchemie import OpenChemIE

    model = OpenChemIE(device="cpu")
    print(f"Running extract_figures_from_pdf on {PDF} ...")
    figures = model.extract_figures_from_pdf(PDF, num_pages=2, output_bbox=True)

    print(f"\nFound {len(figures)} figure(s).")
    os.makedirs(OUT_DIR, exist_ok=True)
    for idx, fig in enumerate(figures):
        title = fig.get("title", "")
        page = fig.get("page")
        bbox = fig.get("figure", {}).get("bbox")
        image = fig.get("figure", {}).get("image")
        print(f"  [{idx}] page={page} title={title!r} bbox={bbox} "
              f"image={'yes' if image is not None else 'no'}")
        if image is not None:
            path = os.path.join(OUT_DIR, f"figure_{idx}_page{page}.png")
            image.save(path)
            print(f"       saved -> {path}")

    assert isinstance(figures, list), "expected a list of figures"
    print("\nOK: extract_figures_from_pdf ran successfully.")


if __name__ == "__main__":
    sys.exit(main())
