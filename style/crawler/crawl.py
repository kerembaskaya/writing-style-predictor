from abc import ABC, abstractmethod
from os import mkdir, path

import requests
from bs4 import BeautifulSoup
from urlpath import URL

from style.constants import FILE_PATH_BOOK_DS, GUTENBERG_BASE_URL
from style.utils.author_catalog import create_catalog
from style.utils.utils import sanitize_author_name


class DataWrangler:
    def __init__(self, baseurl):
        self.session = requests.Session()
        self.baseurl = baseurl

    @abstractmethod
    def crawl(self):
        raise NotImplementedError


class GutenbergWrangler(DataWrangler, ABC):
    def __init__(self, baseurl=GUTENBERG_BASE_URL):
        super().__init__(baseurl)

    def transform_book_id_to_url(self, book_id: str) -> str:
        """
        The function takes the book id and returns the book's regular url address.
        Args:
            book_id (str): The first and only argument.

        Returns:
            the book's url as a string.
        """
        book_id = str(book_id).strip()
        suffix = f"{book_id}/{book_id}.txt"

        if not (0 < len(book_id) < 6):
            raise ValueError(
                "Book's ID should be number between 1 and 65538. It was given {book_id}."
            )

        if len(book_id) == 1:
            infix = "0"
        else:
            infix = "/".join(book_id[:-1])

        return path.join(self.baseurl, infix, suffix)

    def get_book(self, book_id) -> str:
        """
        The function takes the book's URL and checks the correct URL was given,
        If it is not the valid URL, it goes to the URL's parent link and
        The function searches for the correct link if there is use that one.
        The function returns the book's text.

        Args:
            book_id (str): The first argument.
        Returns:
            Returns the book's text as string.
        """
        book_url = self.transform_book_id_to_url(book_id)
        response = self.session.get(book_url)
        if response.status_code == 200:
            return response.text
        elif response.status_code == 404:
            url = URL(book_url).parent
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            for link in soup.find_all("a"):
                current_link = link.get("href")
                if current_link.endswith(".txt"):
                    book_url = f"{url}/{current_link}"
                    response = self.session.get(book_url)
                    return response.text
        else:
            raise NotImplementedError(
                f"Not Implemented for {response.status_code}"
            )

    @staticmethod
    def _save_books_to_disk(book_text, author_name, book_id) -> None:
        """
        It takes the book's text and book's title and saves it on book db under the author's directory as a txt file.

        Returns:
            It returns None.
        """
        author_name = sanitize_author_name(author_name)
        book_name_full = f"{book_id}.txt"
        author_dir_path = FILE_PATH_BOOK_DS / author_name
        book_path = FILE_PATH_BOOK_DS / author_name / book_name_full

        if not path.isdir(author_dir_path):
            mkdir(author_dir_path)

        with open(book_path, "w") as f:
            f.write(book_text)

    def crawl(self) -> None:
        """
        The purpose of the function is to create a book database for the selected authors.
        The function first checks the book database directory exists or not.
        If the directory doesn't exist, it creates the directory then
        The function creates the catalog that contains the selected authors
        and the related book ids.
        After that, the function iterates through this catalog and saves the books to
        the database.

        Returns:
            It returns None.
        """
        if not path.isdir(FILE_PATH_BOOK_DS):
            mkdir(FILE_PATH_BOOK_DS)

        authors_catalog = create_catalog()

        for author, books in authors_catalog.items():
            for book in books:
                book_id = book.book_id
                book_author = book.author
                book_text = self.get_book(book_id)
                self._save_books_to_disk(book_text, book_author, book_id)


if __name__ == "__main__":
    gutenberg = GutenbergWrangler()
    gutenberg.crawl()
