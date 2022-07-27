from dataclasses import dataclass, field
from typing import List
from PIL import Image
import os

@dataclass
class Compressor:
    size_factor: float = 0.8
    quality: int = 85
    file_format: List[str] = field(default_factory=['.jpg'])


    def compressImage(self, pathIn: str, pathOut: str):
        img = Image.open(pathIn)
        height, width = img.size
        height = int(height * self.size_factor)
        width = int(width * self.size_factor)
        img = img.resize((height, width), Image.Resampling.LANCZOS)
        img.save(pathOut, optimize=True, quality=self.quality)

    def compress(self, dirIn: str, dirOut: str):
        try:
            os.makedirs(dirOut)
        except FileExistsError:
            pass

        for file in os.listdir(dirIn):
            _, ext = os.path.splitext(file)
            if ext not in self.file_format: continue
            self.compressImage(os.path.join(dirIn, file), os.path.join(dirOut, file))


if __name__ == '__main__':
    compressor = Compressor(size_factor=0.8, quality=75, file_format=['.jpg', '.png'])
    compressor.compress('./2022-05-30', './compressed')