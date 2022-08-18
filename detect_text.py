from text_detection import setup_credential, detect_image
from text_detection.response_processing import split_posts_by_height


def main():
    setup_credential()

    response = detect_image("text_detection/image/test-image-eng.png")
    document = response.full_text_annotation

    postList = split_posts_by_height(document, [265, 495])

    print(*postList, sep="\n\n")


if __name__ == "__main__":
    main()
