from google.cloud import vision

from typing import Iterator


def pages(document: vision.TextAnnotation, /) -> Iterator[vision.Page]:
    yield from document.pages


def blocks(page: vision.Page, /) -> Iterator[vision.Block]:
    yield from page.blocks


def paragraphs(block: vision.Block, /) -> Iterator[vision.Paragraph]:
    yield from block.paragraphs


def words(paragraph: vision.Paragraph, /) -> Iterator[vision.Word]:
    yield from paragraph.words


def symbols(word: vision.Word, /) -> Iterator[vision.Symbol]:
    yield from word.symbols


def get_words_from_document(
    document: vision.TextAnnotation, /
) -> Iterator[vision.Word]:
    for page in pages(document):
        for block in blocks(page):
            for paragraph in paragraphs(block):
                yield from words(paragraph)
