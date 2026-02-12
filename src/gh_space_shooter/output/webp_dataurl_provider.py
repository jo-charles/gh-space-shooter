"""WebP data URL output provider."""

import base64
import os
from io import BytesIO
from typing import Iterator
from PIL import Image
from .base import OutputProvider


# Marker to search for in files for injection mode
_MARKER = "<!-- space-shooter -->"


class WebpDataUrlOutputProvider(OutputProvider):
    """Output provider that generates WebP as a data URL and writes to a text file."""

    def __init__(self, output_path: str):
        """
        Initialize the provider with an output file path.

        Args:
            output_path: Path to the text file where the data URL will be written
        """
        self.output_path = output_path

    def encode(self, frames: Iterator[Image.Image], frame_duration: int) -> bytes:
        """
        Encode frames as a WebP data URL.

        Args:
            frames: Iterator of PIL Images
            frame_duration: Duration of each frame in milliseconds

        Returns:
            The data URL string as bytes (for consistency with other providers)
        """
        frame_list = list(frames)

        if not frame_list:
            data_url = ""
        else:
            # Encode as WebP using same settings as WebPOutputProvider
            buffer = BytesIO()
            frame_list[0].save(
                buffer,
                format="webp",
                save_all=True,
                append_images=frame_list[1:],
                duration=frame_duration,
                loop=0,
                lossless=True,
                quality=100,
                method=4,
            )

            # Convert to data URL
            webp_bytes = buffer.getvalue()
            base64_data = base64.b64encode(webp_bytes).decode("ascii")
            data_url = f"data:image/webp;base64,{base64_data}"

        # Return data URL as bytes
        return data_url.encode("utf-8")

    def write(self, path: str, data: bytes) -> None:
        """
        Write data URL to file with injection or append mode.

        This handles text mode properly with newlines.

        Args:
            path: Path to the output file
            data: Data URL as bytes (will be decoded as UTF-8 text)
        """
        data_url = data.decode("utf-8")

        # Try to create new file exclusively (avoids TOCTOU race condition)
        try:
            with open(path, "x") as f:
                f.write(data_url + "\n")
            return
        except FileExistsError:
            # File exists - read contents
            with open(path, "r") as f:
                content = f.read()

        # Check for marker
        if _MARKER in content:
            # Injection mode: replace the line containing the marker
            lines = content.splitlines(keepends=True)
            for i, line in enumerate(lines):
                if _MARKER in line:
                    lines[i] = data_url + "\n"
                    break
            content = "".join(lines)
        else:
            # Append mode: add to end
            if content and not content.endswith("\n"):
                content += "\n"
            content += data_url + "\n"

        # Write back
        with open(path, "w") as f:
            f.write(content)
