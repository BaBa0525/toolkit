# Toolkits for media research

Before starting, we recommend you to create an virtual environment and download the dependencies:
```sh
virtualenv -p python3 venv
source venv/bin/activate

pip install -r requirements.txt
```

## Packages

### `utils`

All shared utility functions, currently basic csv operations and decorators.

### `file_processing`

Contains a specific parser class `DetectionResultParser` for YOLO detection results.

### `img_processing`

A simple package that contains an image compressor class `Compressor`.

### `analysis`

Lots of functionalites that are needed for model performance evaluation including data preprocessing and curve representation.

### `text_detection`

Make calls to Google OCR API.
Before using this package, it's needed to setup your credential:

1. Put your own credential JSON file in a directory you prefer.

    (e.g. `/toolkit/credentials/your-credential.json`)

2. Create a `.env` file in the toolkit directory as follows:

    ```.env
    GOOGLE_APPLICATION_CREDENTIALS=path/to/your-credential.json
    ```
