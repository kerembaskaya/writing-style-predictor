import collections
from pathlib import Path


catalog_file_path = str(Path(__file__).parents[1]) + "/resources/" + "pg_catalog.csv"

author_list = (
    "Jefferson, Thomas, 1743-1826",
    "Stevenson, Robert Louis, 1850-1894",
)  # sirasiyla 1, 2, sonuc cikmasi gerekiyor.


def read_csv(filepath=catalog_file_path):
    with open(filepath) as f:
        next(f)
        full_line = ""
        while True:
            try:
                line = next(f).strip()
                try:
                    int(line.split(",", 1)[0])
                    if full_line != "":
                        yield full_line
                    full_line = ""
                except ValueError:
                    pass
                full_line = f"{full_line} {line}"
            except StopIteration:
                if full_line != "":
                    yield full_line
                    break


def parse_data_row(row):
    row_parsed = row.split(",")

    return (
        row_parsed[0],
        row_parsed[3],
        row_parsed[4],
        row_parsed[5],
    )  # respectively: book number, title, language, authors


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
