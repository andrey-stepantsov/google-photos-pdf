#!/usr/bin/env python3
"""Convert Google Photos ZIP exports to a single PDF."""

import argparse
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import List
import img2pdf
from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm

# Register HEIF opener for Pillow
register_heif_opener()

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.webp'}
IGNORE_EXTENSIONS = {'.json', '.mp4', '.mov', '.gif'}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert Google Photos ZIP export to PDF"
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        required=True,
        help="Input ZIP file path"
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output PDF path or directory (default: same as input ZIP)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    return parser.parse_args()


def validate_input(input_path: Path) -> None:
    """Validate input file exists and is a ZIP."""
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    if input_path.suffix.lower() != '.zip':
        print(f"❌ Error: Input must be a ZIP file, got: {input_path.suffix}", file=sys.stderr)
        sys.exit(1)


def determine_output_path(input_path: Path, output_arg: Path | None) -> Path:
    """Determine the final output PDF path."""
    if output_arg is None:
        # Default: same name as ZIP but with .pdf extension
        return input_path.with_suffix('.pdf')
    
    if output_arg.is_dir():
        # If output is a directory, use input filename with .pdf
        return output_arg / input_path.with_suffix('.pdf').name
    
    # Use the specified path
    return output_arg


def extract_zip(zip_path: Path, extract_dir: Path, verbose: bool = False) -> None:
    """Extract ZIP contents with progress bar."""
    with zipfile.ZipFile(zip_path, 'r') as zf:
        members = zf.namelist()
        
        if verbose:
            print(f"📂 Extracting {len(members)} files...")
        
        for member in tqdm(members, desc="Extracting", disable=not sys.stdout.isatty()):
            zf.extract(member, extract_dir)


def filter_and_sort_images(extract_dir: Path, verbose: bool = False) -> List[Path]:
    """Filter for image files and sort alphanumerically."""
    all_files = list(extract_dir.rglob('*'))
    
    image_files = []
    for file in all_files:
        if not file.is_file():
            continue
        
        ext = file.suffix.lower()
        
        if ext in IMAGE_EXTENSIONS:
            image_files.append(file)
        elif verbose and ext in IGNORE_EXTENSIONS:
            print(f"⏭️  Skipping: {file.name}", file=sys.stderr)
    
    # Sort alphanumerically
    image_files.sort(key=lambda p: p.name.lower())
    
    if verbose:
        print(f"✅ Found {len(image_files)} image files")
    
    return image_files


def prepare_image(image_path: Path, temp_dir: Path, verbose: bool = False) -> Path | None:
    """
    Prepare image for PDF conversion.
    Convert HEIC to JPG if needed.
    Returns path to prepared image, or None if image is corrupt.
    """
    try:
        ext = image_path.suffix.lower()
        
        # HEIC/HEIF needs conversion
        if ext in {'.heic', '.heif'}:
            if verbose:
                print(f"🔄 Converting HEIC: {image_path.name}", file=sys.stderr)
            
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode not in ('RGB', 'L'):
                img = img.convert('RGB')
            
            # Save as JPEG in temp directory
            output_path = temp_dir / f"{image_path.stem}.jpg"
            img.save(output_path, "JPEG", quality=95)
            return output_path
        
        # Verify other images can be opened
        with Image.open(image_path) as img:
            img.verify()
        
        return image_path
    
    except Exception as e:
        print(f"⚠️  Skipping corrupt image {image_path.name}: {e}", file=sys.stderr)
        return None


def generate_pdf(image_paths: List[Path], output_path: Path, verbose: bool = False) -> None:
    """Generate PDF from image paths using img2pdf."""
    if not image_paths:
        print("❌ Error: No valid images to convert", file=sys.stderr)
        sys.exit(1)
    
    if verbose:
        print(f"📄 Generating PDF with {len(image_paths)} images...")
    
    try:
        # Convert images to PDF bytes
        pdf_bytes = img2pdf.convert([str(p) for p in image_paths])
        
        # Write to output file
        output_path.write_bytes(pdf_bytes)
        
        if verbose:
            print(f"✅ PDF saved to: {output_path}")
    
    except Exception as e:
        print(f"❌ Error generating PDF: {e}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    args = parse_args()
    
    # Validate input
    validate_input(args.input)
    
    # Determine output path
    output_path = determine_output_path(args.input, args.output)
    
    if args.verbose:
        print(f"📥 Input: {args.input}")
        print(f"📤 Output: {output_path}")
    
    # Create temporary directory for extraction and conversion
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        extract_path = temp_path / "extracted"
        convert_path = temp_path / "converted"
        extract_path.mkdir()
        convert_path.mkdir()
        
        # Extract ZIP
        extract_zip(args.input, extract_path, args.verbose)
        
        # Filter and sort images
        image_files = filter_and_sort_images(extract_path, args.verbose)
        
        if not image_files:
            print("❌ Error: No image files found in ZIP", file=sys.stderr)
            sys.exit(1)
        
        # Prepare images (convert HEIC, validate)
        prepared_images = []
        for img_path in tqdm(image_files, desc="Processing", disable=not sys.stdout.isatty()):
            prepared = prepare_image(img_path, convert_path, args.verbose)
            if prepared:
                prepared_images.append(prepared)
        
        # Generate PDF
        generate_pdf(prepared_images, output_path, args.verbose)
    
    print(f"✅ Success! PDF created: {output_path}")


if __name__ == "__main__":
    main()
