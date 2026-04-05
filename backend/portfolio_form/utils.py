import io
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from pillow_heif import register_heif_opener

# CRITICAL: This allows PIL.Image.open to identify and read .heic files
register_heif_opener()

def compress_to_webp(uploaded_file, quality=75):
    """
    Converts an uploaded image to WebP, resizes to 1K resolution, and compresses.
    """
    img = Image.open(uploaded_file)
    
    # --- 1K RESIZING LOGIC ---
    # Max dimension is 1000px. thumbnail() maintains aspect ratio automatically.
    max_size = (1000, 1000)
    if img.width > 1000 or img.height > 1000:
        # LANCZOS is the high-quality downsampling filter
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Handle transparency and color modes
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        # Use alpha channel as mask to paste onto white background
        background.paste(img, mask=img.split()[3]) 
        img = background
    else:
        img = img.convert("RGB")
    
    # Prepare the output stream
    output_stream = io.BytesIO()
    
    # Save as WebP
    # Reduced quality to 75 (industry standard for web) to save more space
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