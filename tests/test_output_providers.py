"""Tests for output providers."""

import pytest
from PIL import Image
from gh_space_shooter.output.base import OutputProvider


def test_output_provider_is_abstract():
    """OutputProvider cannot be instantiated directly."""
    with pytest.raises(TypeError):
        OutputProvider(fps=30)


def test_output_provider_has_required_attributes():
    """Concrete OutputProvider should have fps, watermark, frame_duration."""
    class DummyProvider(OutputProvider):
        def encode(self, frames):
            return b""

    provider = DummyProvider(fps=30, watermark=True)
    assert provider.fps == 30
    assert provider.watermark is True
    assert provider.frame_duration == 33  # 1000 // 30
