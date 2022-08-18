from dbm import dumb
from google.cloud import vision

from typing import Iterator


def pages(document: vision.TextAnnotation, /) -> Iterator[vision.Page]:
    for page in document.pages:
        yield page


def blocks(page: vision.Page, /) -> Iterator[vision.Block]:
    for block in page.blocks:
        yield block


def paragraphs(block: vision.Block, /) -> Iterator[vision.Paragraph]:
    for paragraph in block.paragraphs:
        yield paragraph


def words(paragraph: vision.Paragraph, /) -> Iterator[vision.Word]:
    for word in paragraph.words:
        yield word


def symbols(word: vision.Word, /) -> Iterator[vision.Symbol]:
    for symbol in word.symbols:
        yield symbol


def get_words_from_document(
    document: vision.TextAnnotation, /
) -> Iterator[vision.Word]:
    for page in pages(document):
        for block in blocks(page):
            for paragraph in paragraphs(block):
                for word in words(paragraph):
                    yield word
