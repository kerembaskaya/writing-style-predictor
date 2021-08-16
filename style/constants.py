from pathlib import Path

# Constants for utils.world_languages


WORLD_LANG_FILENAME = "world-lang.json"
WORLD_LANG_PATH = Path(__file__).parents[1] / "/resources/"
WORLD_LANG_PATH_AND_NAME = (
    Path(__file__).parents[1] / "/resources/" / WORLD_LANG_FILENAME
)

# Constants for style.crawler, style.reader
GUTENBERG_BASE_URL = "http://aleph.gutenberg.org/"
FILE_PATH_BOOK_DB = Path(__file__).parents[1] / "book_db"
FILE_PATH_MOCK_DB = Path(__file__).parents[1] / "mock_db"

# Constants for utils.author_catalog
CATALOG_FILE_PATH = Path(__file__).parents[1] / "resources" / "pg_catalog.csv"

# Constants for tests.style.crawler.test_crawler
TEST_DATA_FILENAME = Path(__file__).parents[1] / "resources" / "test_page.html"

# Constants for style.train.classifier_trainer
MODEL_EXPORT_PATH = Path("/tmp") / "models/"
