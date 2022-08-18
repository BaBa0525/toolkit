from google.cloud import vision
import dotenv

import errno
import os

from .exceptions import EnvironmentVariableNotFoundError


def setup_credential():
    """Load credentail into environment variable and check whether the credentail file exists.

    Raises:
        text_detection.exceptions.EnvironmentVariableNotFoundError:
            If neither the environment variable nor .env file contains `GOOGLE_APPLICATION_CREDENTIALS`.

        FileNotFoundError: If the credential file specified in `GOOGLE_APPLICATION_CREDENTIALS` does not exist.
    """

    dotenv.load_dotenv()

    if (cred := os.getenv("GOOGLE_APPLICATION_CREDENTIALS")) is None:
        raise EnvironmentVariableNotFoundError("GOOGLE_APPLICATION_CREDENTIALS")
    elif not os.path.exists(cred):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), cred)


def detect_image(image_filename: str) -> vision.AnnotateImageResponse:
    """Make an API call to Google OCR API with the image file.

    Args:
        image_filename: The filename of the image to be detected.

    Returns:
        google.cloud.vision.AnnotateImageResponse: Response to Google OCR API request.
    """

    client = vision.ImageAnnotatorClient()

    with open(image_filename, mode="rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    return client.document_text_detection(image=image)
