"""Tests for main.py"""

import tempfile
import zipfile
from pathlib import Path
import pytest
from main import (
    validate_input,
    determine_output_path,
    filter_and_sort_images,
    prepare_image,
    IMAGE_EXTENSIONS,
)


class TestValidateInput:
    """Test input validation."""
    
    def test_validate_input_missing_file(self):
        """Should exit if file doesn't exist."""
        with pytest.raises(SystemExit):
            validate_input(Path("/nonexistent/file.zip"))
    
    def test_validate_input_wrong_extension(self, tmp_path):
        """Should exit if file is not a ZIP."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("not a zip")
        
        with pytest.raises(SystemExit):
            validate_input(txt_file)
    
    def test_validate_input_valid_zip(self, tmp_path):
        """Should pass for valid ZIP file."""
        zip_file = tmp_path / "test.zip"
        with zipfile.ZipFile(zip_file, 'w') as zf:
            zf.writestr("test.txt", "content")
        
        # Should not raise
        validate_input(zip_file)


class TestDetermineOutputPath:
    """Test output path determination."""
    
    def test_output_none_uses_input_name(self, tmp_path):
        """Should use input name with .pdf extension when output is None."""
        input_path = tmp_path / "photos.zip"
        result = determine_output_path(input_path, None)
        assert result == tmp_path / "photos.pdf"
    
    def test_output_directory(self, tmp_path):
        """Should use input filename in output directory."""
        input_path = Path("/some/path/photos.zip")
        output_dir = tmp_path
        result = determine_output_path(input_path, output_dir)
        assert result == output_dir / "photos.pdf"
    
    def test_output_explicit_path(self, tmp_path):
        """Should use explicit output path."""
        input_path = tmp_path / "photos.zip"
        output_path = tmp_path / "custom_name.pdf"
        result = determine_output_path(input_path, output_path)
        assert result == output_path


class TestFilterAndSortImages:
    """Test image filtering and sorting."""
    
    def test_filter_images_only(self, tmp_path):
        """Should only include image files."""
        # Create test files
        (tmp_path / "photo1.jpg").touch()
        (tmp_path / "photo2.png").touch()
        (tmp_path / "video.mp4").touch()
        (tmp_path / "metadata.json").touch()
        (tmp_path / "photo3.heic").touch()
        
        result = filter_and_sort_images(tmp_path, verbose=False)
        
        assert len(result) == 3
        assert all(f.suffix.lower() in IMAGE_EXTENSIONS for f in result)
    
    def test_sort_alphanumerically(self, tmp_path):
        """Should sort files alphanumerically."""
        (tmp_path / "photo_10.jpg").touch()
        (tmp_path / "photo_2.jpg").touch()
        (tmp_path / "photo_1.jpg").touch()
        
        result = filter_and_sort_images(tmp_path, verbose=False)
        
        names = [f.name for f in result]
        assert names == ["photo_1.jpg", "photo_10.jpg", "photo_2.jpg"]
    
    def test_recursive_search(self, tmp_path):
        """Should find images in subdirectories."""
        subdir = tmp_path / "subdir"
        subdir.mkdir()
        (tmp_path / "photo1.jpg").touch()
        (subdir / "photo2.jpg").touch()
        
        result = filter_and_sort_images(tmp_path, verbose=False)
        
        assert len(result) == 2


class TestPrepareImage:
    """Test image preparation."""
    
    def test_prepare_jpg_returns_original(self, tmp_path):
        """Should return original path for JPG files."""
        from PIL import Image
        
        jpg_file = tmp_path / "test.jpg"
        img = Image.new('RGB', (100, 100), color='red')
        img.save(jpg_file, 'JPEG')
        
        convert_dir = tmp_path / "convert"
        convert_dir.mkdir()
        
        result = prepare_image(jpg_file, convert_dir, verbose=False)
        
        assert result == jpg_file
    
    def test_prepare_corrupt_image_returns_none(self, tmp_path):
        """Should return None for corrupt images."""
        corrupt_file = tmp_path / "corrupt.jpg"
        corrupt_file.write_bytes(b"not a real image")
        
        convert_dir = tmp_path / "convert"
        convert_dir.mkdir()
        
        result = prepare_image(corrupt_file, convert_dir, verbose=False)
        
        assert result is None


class TestIntegration:
    """Integration tests."""
    
    def test_full_workflow_with_jpg(self, tmp_path):
        """Test complete workflow with JPG images."""
        from PIL import Image
        import img2pdf
        
        # Create a test ZIP with images
        zip_path = tmp_path / "photos.zip"
        with zipfile.ZipFile(zip_path, 'w') as zf:
            # Create test images in memory
            for i in range(3):
                img = Image.new('RGB', (100, 100), color=['red', 'green', 'blue'][i])
                img_bytes = img.tobytes()
                # Note: This is simplified; real test would save proper JPEG
                zf.writestr(f"photo_{i}.jpg", img_bytes)
        
        # Validate input works
        validate_input(zip_path)
        
        # Determine output
        output_path = determine_output_path(zip_path, None)
        assert output_path == tmp_path / "photos.pdf"
