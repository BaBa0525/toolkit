from toolkitpkg.parser import DetectionResultParser
from toolkitpkg.compressor import Compressor

def main() -> None:

    parser = DetectionResultParser(inputFile='/path/to/input.txt')
    df = parser.to_df()                         # getting a pandas.DataFreame object
    parser.to_csv(ouptut='/path/to/output.csv') # or, alternatively, output to a .csv file


    compressor = Compressor(size_factor=0.8, quality=75, file_format=['.jpg', '.png'])
    compressor.compressImage('/path/to/a/image.jpg', '/path/to/destination.jpg') # compress one image
    compressor.compress('/path/to/input/directory', '/path/to/output/directory') # compress all images in a directory


if __name__ == "__main__":
    main()