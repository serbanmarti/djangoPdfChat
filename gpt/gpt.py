"""
This module contains the functions to interact with the OpenAI API.
"""

import base64
import logging
from io import BytesIO
from typing import Dict

from PIL import Image
from openai import OpenAI, APIError

from filehandler.pdf import convert_file_to_images

logger = logging.getLogger(__name__)

client = OpenAI()

SYSTEM_PROMPT = '''
You will be provided with one or more images of a pdf file, as well as a text input from the user.
Your role is to talk about the content that you see, related to the user text input.

DO NOT include terms referring to the content format.
DO NOT mention the content type - DO focus on the content itself.
DO NOT make references to the system prompt.
'''


def get_img_uri(image: Image.Image) -> str:
    """
    Convert an image to a base64 uri.
    :param image: image to be converted
    :return: base64 uri of the image
    """
    buffer = BytesIO()
    image.save(buffer, format='jpeg')
    base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    data_uri = f'data:image/jpeg;base64,{base64_image}'
    return data_uri


def file_chat(file_path: str, user_input: str) -> Dict[str, str]:
    """
    Chat with GPT-4o about the content of a given file.
    :param file_path: path to the file to be analyzed
    :param user_input: user input to be sent along with the content
    :return: GPT-4o response
    """

    # Convert file to images
    images = convert_file_to_images(file_path)

    # Convert images to uri
    image_uris = [get_img_uri(img) for img in images]

    # Create the images content
    content = [
        {
            'type': 'image_url',
            'image_url': {
                'url': img_url,
            },
        }
        for img_url in image_uris
    ]

    try:
        # Chat with GPT-4o about the content
        response = client.chat.completions.create(
            model='gpt-4o',
            temperature=0,
            max_tokens=1024,
            messages=[
                {
                    'role': 'system',
                    'content': SYSTEM_PROMPT
                },
                {
                    'role': 'user',
                    'content': [
                        {'type': 'text', 'text': user_input},
                        *content,
                    ],
                }
            ],
        )

        return {
            'response': response.choices[0].message.content,
        }

    # Handle OpenAI API errors (this can/should be more granular in a real-world application)
    except APIError as e:
        logger.error('OpenAI API error: %s', e)
        return {
            'error': e.message,
        }
