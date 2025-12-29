# FAS2rDNA
# Copyright © 2025 Marvin De los Santos
# This version works with FAS2rDNA in local implementation (v1.0)
# fas2rdna_cli.py for Linux
# https://fas2rdna.chordexbio.com


import argparse
import os
import sys
import subprocess
import urllib.request
import ssl
from pathlib import Path

# ---------------------------
# GitHub raw base
# ---------------------------
def github_ssl_context():
    """
    Create a relaxed SSL context ONLY for GitHub downloads.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


GITHUB_BASE = "https://raw.githubusercontent.com/mahvin92/FAS2rDNA/main/source"

FILES_TO_FETCH = {
    "fas2rdna.py":
        f"{GITHUB_BASE}/fas2rdna.py",
    "install/codeenigma_runtime-1.2.0-py3-none-any.whl":
        f"{GITHUB_BASE}/install/codeenigma_runtime-1.2.0-py3-none-any.whl",
    "install/fas2rdna_pyproject.toml":
        f"{GITHUB_BASE}/install/fas2rdna_pyproject.toml",
    "install/codeenigma_runtime/__init__.py":
        f"{GITHUB_BASE}/install/codeenigma_runtime/__init__.py",
}

# ---------------------------
# Utilities
# ---------------------------
def download_if_missing(url, dest: Path):
    if dest.exists():
        return

    dest.parent.mkdir(parents=True, exist_ok=True)

    print(f"[DOWNLOAD] {url}")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "FAS2rDNA-CLI"}
    )

    with urllib.request.urlopen(req, context=github_ssl_context()) as response:
        with open(dest, "wb") as f:
            f.write(response.read())


def ensure_source_tree(input_dir: Path):
    source_dir = input_dir / "source"

    source_dir.mkdir(exist_ok=True)

    for rel_path, url in FILES_TO_FETCH.items():
        download_if_missing(url, source_dir / rel_path)

    return source_dir



def install_wheel_if_needed(source_dir: Path):
    wheel_path = (
        source_dir
        / "install"
        / "codeenigma_runtime-1.2.0-py3-none-any.whl"
    )

    if not wheel_path.exists():
        raise FileNotFoundError(
            f"Required wheel not found after download: {wheel_path}"
        )

    print(f"[INSTALL] {wheel_path.name}")

    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "--quiet",
        "--upgrade",
        str(wheel_path)
    ])



# ---------------------------
# CLI
# ---------------------------
def main():
    print("FAS2rDNA is running ...")

    parser = argparse.ArgumentParser(description="FAS2rDNA local CLI")
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing input TXT files",
    )
    parser.add_argument(
        "--header",
        default="{sample_id}",
        help="FASTA header template",
    )
    parser.add_argument(
        "--combined-name",
        default="All_sequences.fasta",
        help="Combined FASTA output filename",
    )

    args = parser.parse_args()
    input_dir = Path(args.input_dir).resolve()

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    # 1. Prepare source runtime
    source_dir = ensure_source_tree(input_dir)

    # 2. Install runtime wheel
    install_wheel_if_needed(source_dir)

    # 3. Ensure source dir is importable
    sys.path.insert(0, str(source_dir))

    # 4. Import AFTER install
    import fas2rdna  # noqa: E402

    # 5. Execute
    result = fas2rdna.run_fas2rdna(
        str(input_dir),
        args.header,
        args.combined_name,
    )

    return result


if __name__ == "__main__":
    main()
