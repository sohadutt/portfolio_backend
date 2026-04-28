from __future__ import annotations

import io
from typing import BinaryIO

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile
from pillow_heif import register_heif_opener

register_heif_opener()

def compress_to_webp(uploaded_file: UploadedFile, quality: int = 75) -> InMemoryUploadedFile:
    img = Image.open(uploaded_file)

    max_size = (1000, 1000)
    if img.width > 1000 or img.height > 1000:
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
    else:
        img = img.convert("RGB")

    output_stream: BinaryIO = io.BytesIO()
    img.save(output_stream, format="WEBP", quality=quality, method=6)
    output_stream.seek(0)

    return InMemoryUploadedFile(
        output_stream,
        'ImageField',
        f"{uploaded_file.name.split('.')[0]}.webp",
        'image/webp',
        output_stream.getbuffer().nbytes,
        None
    )
