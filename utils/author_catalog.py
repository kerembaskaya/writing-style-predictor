import collections
import csv
from pathlib import Path


catalog_file_path = str(Path(__file__).parents[1]) + "/resources/" + "pg_catalog.csv"

author_list = (
    "Jefferson, Thomas, 1743-1826",
    "Stevenson, Robert Louis, 1850-1894",
)  # sirasiyla 1, 2, sonuc cikmasi gerekiyor.


def read_csv(filepath=catalog_file_path):
    lines = csv.reader(open(filepath), delimiter=",")
    next(lines)  # skip the header.
    for line in lines:
        # data has some random new lines. Replace them with white space, then strip it.
        yield list(map(lambda s: s.replace("\n", " ").strip(), line))


def parse_data_row(row: list):

    return (
        row[0],  # book number
        row[3],  # title
        row[4],  # language
        row[5],  # authors
    )


def list_author_data(row, list_of_author=author_list, language="en"):
    authors_set = set(
        list_of_author
    )  # Q burada tuple'i set'e cevirdim hizlansin diye yoksa gereksiz bir hamle mi?
    book_number, book_title, book_lang, authors = row[:]
    if authors in authors_set and book_lang == "en":
        return row


def create_catalog(filepath=catalog_file_path):
    author_book_catalog = collections.defaultdict(dict)
    for row in read_csv(filepath):
        parsed_row = parse_data_row(row)
        if list_author_data(parsed_row) is not None:
            author_book_catalog[row[3]][row[1]] = row[0]

    return author_book_catalog


create_catalog()
