import os

from PIL import Image


class Compressor:
    def __init__(
        self,
        size_factor: float = 0.8,
        quality: int = 85,
        file_format: "list[str]" = [".jpg"],
    ):
        """Instantiate an image compressor object."""
        self.size_factor = size_factor
        self.quality = quality
        self.file_format = file_format

    def compress_image(self, inputFile: str, outputFile: str):
        """Compress a single image."""
        img = Image.open(inputFile)

        width, height = img.size
        newWidth = int(width * self.size_factor)
        newHeight = int(height * self.size_factor)

        img = img.resize((newWidth, newHeight), Image.Resampling.LANCZOS)
        img.save(outputFile, optimize=True, quality=self.quality)

    def compress(self, inputDirectory: str, outputDirectory: str):
        """Compress every image in the directory input_dir if the file extension has matches in the file_format."""
        try:
            os.makedirs(outputDirectory)
        except FileExistsError:
            pass

        for file in os.listdir(inputDirectory):
            _, ext = os.path.splitext(file)

            if ext not in self.file_format:
                continue

            inputFile = os.path.join(inputDirectory, file)
            outputFile = os.path.join(outputDirectory, file)

            self.compress_image(inputFile, outputFile)
