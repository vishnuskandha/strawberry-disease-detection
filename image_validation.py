from io import BytesIO

from PIL import Image, UnidentifiedImageError

MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 20_000_000


def validate_image_bytes(data: bytes) -> None:
    if len(data) > MAX_UPLOAD_BYTES:
        raise ValueError("Image is too large; maximum size is 10 MB.")

    try:
        with Image.open(BytesIO(data)) as image:
            width, height = image.size
            if width * height > MAX_IMAGE_PIXELS:
                raise ValueError("Image dimensions are too large; maximum is 20 megapixels.")
            image.verify()
    except (UnidentifiedImageError, OSError) as exc:
        raise ValueError("The uploaded file is not a valid image.") from exc
