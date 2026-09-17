import unittest
from io import BytesIO

from PIL import Image

from image_validation import MAX_IMAGE_PIXELS, MAX_UPLOAD_BYTES, validate_image_bytes


class ImageValidationTests(unittest.TestCase):
    def test_valid_image_is_accepted(self):
        output = BytesIO()
        Image.new("RGB", (32, 32)).save(output, format="PNG")
        validate_image_bytes(output.getvalue())

    def test_invalid_bytes_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "not a valid image"):
            validate_image_bytes(b"not an image")

    def test_oversized_payload_is_rejected_before_decode(self):
        with self.assertRaisesRegex(ValueError, "too large"):
            validate_image_bytes(b"0" * (MAX_UPLOAD_BYTES + 1))

    def test_oversized_dimensions_are_rejected(self):
        output = BytesIO()
        Image.new("RGB", (5001, 4001)).save(output, format="JPEG")
        with self.assertRaisesRegex(ValueError, "20 megapixels"):
            validate_image_bytes(output.getvalue())


if __name__ == "__main__":
    unittest.main()
