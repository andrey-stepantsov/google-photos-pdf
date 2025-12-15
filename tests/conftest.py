"""Pytest configuration and shared fixtures."""

import pytest
from pathlib import Path


@pytest.fixture
def sample_zip(tmp_path):
    """Create a sample ZIP file with test images."""
    import zipfile
    from PIL import Image
    import io
    
    zip_path = tmp_path / "test_photos.zip"
    
    with zipfile.ZipFile(zip_path, 'w') as zf:
        # Create 3 test JPG images
        for i in range(3):
            img = Image.new('RGB', (100, 100), color=['red', 'green', 'blue'][i])
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG')
            zf.writestr(f"photo_{i+1}.jpg", img_buffer.getvalue())
        
        # Add a JSON file to ignore
        zf.writestr("metadata.json", '{"test": "data"}')
    
    return zip_path
