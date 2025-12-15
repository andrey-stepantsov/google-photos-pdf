# Google Photos to PDF Converter

A robust Command Line Interface (CLI) tool designed to convert messy Google Photos "Takeout" ZIP exports into clean, single-file PDFs.

It handles the complexities of modern photo libraries—like Apple's **HEIC format**, scattered **JSON metadata**, and random video files—so you don't have to.

## Features

* **Direct ZIP Input:** Processes the downloaded Google Takeout ZIP file directly without needing to unzip it first.
* **HEIC Support:** Automatically converts `.heic` and `.heif` images (common on iPhones and newer Androids) into a PDF-compatible format on the fly.
* **Smart Filtering:** Ignores non-image clutter like `.json` sidecar files, `.mp4`, and `.mov` videos.
* **Correct Ordering:** Sorts images alphanumerically to ensure your PDF pages are in sensible order.
* **Lossless Quality:** Uses `img2pdf` to embed existing JPEG files directly into the PDF without re-encoding them, preserving original quality and keeping file sizes manageable.
* **Memory Efficient:** Uses temporary storage for extraction and processing, handling large archives without overwhelming system RAM.

## Installation

### Prerequisites

1. Install **Nix**: [Download here](https://nixos.org/download.html)
2. *(Optional but recommended)* Enable **Flakes** if using an older Nix version: [Instructions here](https://nixos.wiki/wiki/Flakes#Enable_flakes)

### Quick Start (One-Time Use)

Download and run the tool for a one-off conversion without installing it permanently.

> **⚠️ Important:** Notice the double dash (`--`) before the input arguments. This is required.

