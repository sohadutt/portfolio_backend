import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

def compress_to_webp(uploaded_file, quality=80):
    """
    Converts an uploaded image to WebP format and compresses it.
    """
    img = Image.open(uploaded_file)
    
    # Convert to RGB (WebP doesn't always handle indexed colors well)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    # Prepare the output stream
    output_stream = io.BytesIO()
    
    # Save as WebP with the specified quality
    img.save(output_stream, format="WEBP", quality=quality, method=6)
    output_stream.seek(0)
    
    # Return as a Django-friendly file object
    return InMemoryUploadedFile(
        output_stream,
        'ImageField',
        f"{uploaded_file.name.split('.')[0]}.webp",
        'image/webp',
        output_stream.getbuffer().nbytes,
        None
    )