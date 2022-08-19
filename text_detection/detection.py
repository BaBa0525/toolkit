from google.cloud import vision
import dotenv

import errno
import os

from .helpers import filename_to_image
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


def detect_image(imageFile: str) -> vision.AnnotateImageResponse:
    """Make an API call to Google OCR API with the image file.

    Args:
        imageFile: The filename of the image to be detected.

    Returns:
        google.cloud.vision.AnnotateImageResponse: Response to Google OCR API request.
    """

    client = vision.ImageAnnotatorClient()

    image = filename_to_image(imageFile)
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    request = vision.AnnotateImageRequest(image=image, features=[feature])

    return client.annotate_image(request)


def batch_detect(filenames: "list[str]") -> "list[vision.AnnotateImageResponse]":
    """Make an API call to Google OCR API with all image files specified.

    Args:
        filenames: A list of filenames to be detected.

    Returns:
        list[google.cloud.vision.AnnotateImageResponse]: All responses to Google OCR API request.
    """

    client = vision.ImageAnnotatorClient()

    imageRequests = [
        vision.AnnotateImageRequest(
            image=filename_to_image(filename),
            features=[vision.Feature(type=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)],
        )
        for filename in filenames
    ]

    request = vision.BatchAnnotateImagesRequest(requests=imageRequests)

    return client.batch_annotate_images(request=request).responses


def dump_json(response: vision.AnnotateImageResponse, destination: str):
    """Write a new JSON file with the content of the response."""

    string = vision.AnnotateImageResponse.to_json(response)
    with open(destination, mode="w") as jsonfile:
        jsonfile.write(string)
