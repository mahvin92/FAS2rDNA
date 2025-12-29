# FAS2rDNA
# Copyright © 2025 Marvin De los Santos
# This version works with FAS2rDNA in local implementation (v1.0)
# fas2rdna_cli.py for non-Linux OS
# https://fas2rdna.chordexbio.com

import argparse
import urllib.request
import tempfile
import os
import importlib.util
import ssl
from urllib.error import URLError, HTTPError

# ─────────────────────────────
# Hosted assets (public)
# ─────────────────────────────
LOADER_URL = "https://assets.zyrosite.com/CmRam6QtIHMUASqE/loader.py-HW4X26xO9sd0AMRL.txt"
ZIP_URL    = "https://assets.zyrosite.com/CmRam6QtIHMUASqE/payload.zip-UH3deRtuO3d3g8NF.txt"


# ─────────────────────────────
# Safe downloader (macOS-proof)
# ─────────────────────────────
def safe_download(url, dest_path):
    req = urllib.request.Request(url, headers={"User-Agent": "FAS2rDNA-CLI"})

    try:
        with urllib.request.urlopen(req) as r, open(dest_path, "wb") as f:
            f.write(r.read())

    except (URLError, HTTPError):
        # Retry with relaxed SSL (macOS cert issue)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        with urllib.request.urlopen(req, context=ctx) as r, open(dest_path, "wb") as f:
            f.write(r.read())


# ─────────────────────────────
# Dynamic loader import
# ─────────────────────────────
def load_loader(path):
    spec = importlib.util.spec_from_file_location("fas2rdna_loader", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ─────────────────────────────
# Main CLI
# ─────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="FAS2rDNA CLI (runtime-loaded)"
    )

    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing input .txt files"
    )

    parser.add_argument(
        "--header",
        default="{sample_id}",
        help="FASTA header template"
    )

    parser.add_argument(
        "--combined-name",
        default="All_sequences.fasta",
        help="Combined FASTA output filename"
    )

    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        loader_path = os.path.join(tmpdir, "loader.py")
        zip_path    = os.path.join(tmpdir, "payload.zip")

        # 🔐 SSL-safe downloads + suffix stripping
        safe_download(LOADER_URL, loader_path)
        safe_download(ZIP_URL, zip_path)

        loader = load_loader(loader_path)
        module, temp_ctx = loader.load_fas2rdna_from_zip(zip_path)

        try:
            module.run_fas2rdna(
                args.input_dir,
                args.header,
                args.combined_name
            )
        finally:
            temp_ctx.cleanup()


if __name__ == "__main__":
    main()
