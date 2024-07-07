"""
This file contains the forms for the API.
"""

from django import forms


class UploadFileForm(forms.Form):
    """
    Form for uploading a file.
    """
    file = forms.FileField()
