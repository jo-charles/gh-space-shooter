"""Tests for WebP data URL output provider."""

from PIL import Image
import pytest
from gh_space_shooter.output.webp_dataurl_provider import WebpDataUrlOutputProvider
import tempfile
import os


def create_test_frame(color="red"):
    """Helper to create a test frame."""
    img = Image.new("RGB", (10, 10), color)
    return img


def test_provider_creates_new_file():
    """Provider should create file and write data URL when file doesn't exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = os.path.join(tmpdir, "output.txt")
        provider = WebpDataUrlOutputProvider(output_path)
        frames = [create_test_frame("red"), create_test_frame("blue")]

        result = provider.encode(iter(frames), frame_duration=100)

        # File should exist and contain data URL
        assert os.path.exists(output_path)
        with open(output_path, "r") as f:
            content = f.read()
        assert content.startswith("data:image/webp;base64,")
        # Should return bytes as well
        assert result == content.encode("utf-8")
