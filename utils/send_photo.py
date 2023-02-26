import urllib.request
from io import BytesIO

from aiogram import types


async def send_image(chat_id: int, image_url: str, caption: str = None):
    with urllib.request.urlopen(image_url) as url:
        content_type = url.info().get_content_type()
        if content_type.startswith('image/'):
            image_bytes = BytesIO(url.read())
            photo = types.InputFile(image_bytes, filename='image.jpg')
            return photo
        elif content_type == 'application/octet-stream':
            # Check file header or signature to determine file type
            file_header = url.read(16)
            if file_header.startswith(b'\xff\xd8'):
                # JPEG file
                image_bytes = BytesIO(file_header + url.read())
                photo = types.InputFile(image_bytes, filename='image.jpg')
                return photo
            elif file_header.startswith(b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a'):
                # PNG file
                image_bytes = BytesIO(file_header + url.read())
                photo = types.InputFile(image_bytes, filename='image.png')
                return photo
            else:
                raise TypeError('Unsupported file type.')
        else:
            raise TypeError('Not an image file.')