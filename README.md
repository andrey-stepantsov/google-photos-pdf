# Google Photos to PDF Converter

A robust Command Line Interface (CLI) tool designed to convert messy Google Photos "Takeout" ZIP exports into clean, single-file PDFs.

It handles the complexities of modern photo libraries—like Apple's **HEIC format**, scattered **JSON metadata**, and random video files—so you don't have to.

## ✨ Features

  * **Direct ZIP Input:** Processes the downloaded Google Takeout ZIP file directly without needing to unzip it first.
  * **HEIC Support:** Automatically converts `.heic` and `.heif` images (common on iPhones and newer Androids) into a PDF-compatible format on the fly.
  * **Smart Filtering:** Ignores non-image clutter like `.json` sidecar files, `.mp4`, and `.mov` videos.
  * **Correct Ordering:** Sorts images alphanumerically to ensure your PDF pages are in sensible order.
  * **Lossless Quality:** Uses `img2pdf` to embed existing JPEG files directly into the PDF without re-encoding them, preserving original quality and keeping file sizes manageable.
  * **Memory Efficient:** Uses temporary storage for extraction and processing, handling large archives without overwhelming system RAM.

-----

## 🚀 Usage (End Users)

You can run this tool directly using the [Nix Package Manager](https://nixos.org/download.html). No manual Python installation is required.

### Prerequisites

1.  Install **Nix**: [Instructions here](https://nixos.org/download.html).
2.  *(Optional but recommended)* Enable **Flakes** if using an older Nix version: [Instructions here](https://nixos.wiki/wiki/Flakes#Enable_flakes).

### 1\. Run Instantly (Temporary)

Download and run the tool for a one-off conversion without installing it permanently.

> **⚠️ Important:** Notice the double dash (`--`) before the input arguments. This is required.

```bash

# Syntax: nix run github:yourusername/google-photos-pdf -- [options]

# Example 1: Convert a zip, output PDF in the same location

nix run github:andrey-stepantsov/google-photos-pdf -- -i ./takeout-2023.zip

# Example 2: Convert a zip, specify a different output directory

nix run github:andrey-stepantsov/google-photos-pdf -- -i ./takeout-2023.zip -o \~/Documents/ArchivedPhotos/
```

### 2\. Install Permanently

Add the tool to your system environment for frequent use.

```bash

# 1\. Install

nix profile install github:andrey-stepantsov/google-photos-pdf

# 2\. Run (no double dash needed)

google-photos-to-pdf -i ./takeout-2023.zip
```

-----

## 🛠️ Development

This project uses **Devbox** for reproducible system dependencies and **Poetry** for Python package management.

### Prerequisites

  * [Devbox](https://www.jetify.com/devbox)
  * [direnv](https://direnv.net/) (Recommended for automatic environment loading)

### Setup Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/andrey-stepantsov/google-photos-pdf.git
    cd google-photos-pdf
    ```
    *If you have `direnv` set up, the Devbox environment will load automatically.*

2.  **Install Python dependencies:**
    You must run this manually the first time to set up the virtual environment.
    ```bash
    poetry install
    ```

3.  **Run the tool:**
    You can execute the script using Poetry to ensure it runs within the correct virtual environment.
    ```bash
    poetry run python main.py -i /path/to/your/input.zip
    ```

## 📄 License

[MIT](LICENSE)
