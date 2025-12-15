#!/usr/bin/env python3
"""Generate test data for the Google Photos ZIP to PDF converter."""

from pathlib import Path
import zipfile
from PIL import Image
from pillow_heif import register_heif_opener
import shutil

# Register HEIF opener
register_heif_opener()

def generate_test_data():
    """Create test images and zip them."""
    test_dir = Path("test_data_temp")
    test_dir.mkdir(exist_ok=True)
    
    print("🎨 Generating test images...")
    
    # Create 3 JPGs
    for i in range(1, 4):
        img = Image.new('RGB', (800, 600), color=(i*80, 100, 150))
        img.save(test_dir / f"photo_{i:03d}.jpg", "JPEG")
    
    # Create 1 PNG
    img = Image.new('RGB', (800, 600), color=(200, 50, 100))
    img.save(test_dir / "screenshot_001.png", "PNG")
    
    # Create 2 HEICs (save as JPEG first, then we'll handle HEIC in main)
    # Note: Creating actual HEIC files requires libheif encoder
    # For testing, we'll create JPEGs with .heic extension to simulate
    for i in range(1, 3):
        img = Image.new('RGB', (800, 600), color=(100, i*100, 200))
        # Save as JPEG but with HEIC extension for testing filter logic
        img.save(test_dir / f"IMG_{i:04d}.HEIC", "JPEG")
    
    # Create junk files
    (test_dir / "metadata.json").write_text('{"version": "1.0"}')
    (test_dir / "movie.mp4").write_bytes(b"fake mp4 data")
    (test_dir / "video.mov").write_bytes(b"fake mov data")
    
    print("📦 Creating test_input.zip...")
    
    # Create ZIP
    with zipfile.ZipFile("test_input.zip", "w", zipfile.ZIP_DEFLATED) as zf:
        for file in test_dir.iterdir():
            zf.write(file, file.name)
    
    # Cleanup temp directory
    shutil.rmtree(test_dir)
    
    print("✅ test_input.zip created successfully!")

if __name__ == "__main__":
    generate_test_data()
