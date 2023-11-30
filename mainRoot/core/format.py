import base64
from django.core.files.base import ContentFile


def decode_base64_and_save(data, filename):
    # Add padding if needed
    padding = '=' * (4 - len(data) % 4) if len(data) % 4 != 0 else ''
    data = data + padding

    image_data = base64.b64decode(data)
    return ContentFile(image_data, filename)
