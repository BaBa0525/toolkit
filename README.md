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

### `fileprocessing`

Contains a specific parser class `DetectionResultParser` for YOLO detection results.

### `imgprocessing`

A simple package that contains an image compressor class `Compressor`.

### `analysis`

Lots of functionalites that are needed for model performance evaluation including data preprocessing and curve representation.

