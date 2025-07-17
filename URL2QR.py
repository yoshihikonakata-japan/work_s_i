#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL2QR: Batch QR-code generator for a list of URLs.

Reads URLs from a text file (one URL per line) and outputs PNG-format QR codes
at three fixed sizes (270×270, 360×360, 450×450 pixels). Filenames are derived
from the last four characters of each URL (uppercased).

Dependencies:
    pip install segno pillow

Usage:
    python URL2QR.py
    (uses predefined INPUT_FILE and OUTPUT_DIR unless overridden via args)
"""
import argparse
import logging
import math
from pathlib import Path
from io import BytesIO

import segno
from PIL import Image

# デフォルトの入出力パスを定義
INPUT_FILE = Path(r"C:\pyQR\URL_List\URL_List.txt")
OUTPUT_DIR = Path(r"C:\pyQR\QR_generate")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Batch-generate PNG QR codes from URLs."
    )
    parser.add_argument(
        "-i", "--input", type=Path,
        default=INPUT_FILE,
        help="Input text file with one URL per line."
    )
    parser.add_argument(
        "-o", "--output", type=Path,
        default=OUTPUT_DIR,
        help="Directory to save generated QR code images."
    )
    parser.add_argument(
        "-e", "--error-level", choices=["l", "m", "q", "h"],
        default="m",
        help="QR code Reed-Solomon error correction level."
    )
    return parser.parse_args()


def extract_code(url: str, length: int = 4) -> str:
    """
    Derive a base filename from the last `length` characters of the URL,
    stripping trailing slashes or hashes, and convert to uppercase.
    """
    cleaned = url.rstrip("/#!")
    return cleaned[-length:].upper()


def generate_qr_images(
    url: str,
    sizes: list[int],
    error_level: str,
    output_dir: Path,
) -> None:
    code = extract_code(url)
    qr = segno.make_qr(url, error=error_level)

    border = 4  # modules
    module_count, _ = qr.symbol_size()
    total_modules = module_count + border * 2
    initial_scale = math.ceil(max(sizes) / total_modules)

    # Generate PIL image via buffer since to_pil may not be available
    buf = BytesIO()
    qr.save(buf, kind='png', scale=initial_scale, border=border)
    buf.seek(0)
    pil_img = Image.open(buf)

    for size in sizes:
        img = pil_img.resize((size, size), Image.NEAREST)
        filename = f"{code}_{size}x{size}.png"
        out_path = output_dir / filename
        img.save(out_path)
        logging.info("Generated %s", out_path)


def main() -> None:
    args = parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    input_file: Path = args.input
    output_dir: Path = args.output
    sizes = [270, 360, 450]

    if not input_file.exists():
        logging.error("Input file not found: %s", input_file)
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    with input_file.open(encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            if not url:
                continue
            try:
                generate_qr_images(url, sizes, args.error_level, output_dir)
            except Exception as e:
                logging.error("Failed on URL %s: %s", url, e)


if __name__ == "__main__":
    main()
