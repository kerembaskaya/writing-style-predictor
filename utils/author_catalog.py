import collections
import csv
from dataclasses import dataclass
from typing import Dict

from style.constants import CATALOG_FILE_PATH

selected_authors = {
    "Jefferson, Thomas, 1743-1826",
    "Stevenson, Robert Louis, 1850-1894",
    "Lincoln, Abraham, 1809-1865",
    "Dickens, Charles, 1812-1870",
    "Douglass, Frederick, 1818-1895",
}  # respectively it should returns 1, 2.


def read_csv(filepath=CATALOG_FILE_PATH):
    lines = csv.reader(open(filepath), delimiter=",")
    next(lines)  # skip the header.
    for line in lines:
        # data has some random new lines. Replace them with white space, then strip it.
        yield list(map(lambda s: s.replace("\n", " ").strip(), line))


@dataclass
class Book:
    book_id: str
    title: str
    language: str
    author: str


def parse_data_row(row: list):

    return Book(
        row[0],  # book number
        row[3],  # title
        row[4],  # language
        row[5],  # author
    )


def is_selected_author(book: Book, language="en"):
    if book.author in selected_authors and book.language == language:
        return True
    return False


def create_catalog(filepath: str = CATALOG_FILE_PATH) -> Dict:
    """

    Note:
        If there are different versions of the same book in the source catalog, it takes only the last version
    since it saves by title (the last one overwrites the previous version).


    Args:
        filepath (str): The first argument. The filepath of the source catalog of the related database.

    Returns:

        Return a dictionary contains authors' dictionaries that contain book title and book id pairs.

    """
    author_book_catalog = collections.defaultdict(list)
    for row in read_csv(filepath):
        book = parse_data_row(row)
        if is_selected_author(book):
            author_book_catalog[book.author].append(book)

    return author_book_catalog
