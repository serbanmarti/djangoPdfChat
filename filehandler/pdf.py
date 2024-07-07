"""
This module contains functions to handle PDF files.
"""

from typing import List

from PIL import Image
from pdf2image import convert_from_path


def convert_file_to_images(file_path: str) -> List[Image.Image]:
    """
    Convert a PDF file to a list of images.
    :param file_path: path to the PDF file
    :return: list of images
    """
    return convert_from_path(file_path)
