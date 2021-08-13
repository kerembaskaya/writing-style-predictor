import pytest

from style.constants import FILE_PATH_BOOK_DB
from style.dataset.reader import DatasetReader


@pytest.fixture
def dataset():
    return DatasetReader.load_files(FILE_PATH_BOOK_DB)


# class TestDatasetReader:
#
#     def test_load_files(self, dataset):
#         # assert dataset.target == ['robert_louis_stevenson', 'robert_louis_stevenson', 'thomas_jefferson']
#         # assert len(dataset.data) == 3
#         # assert len(dataset.data[0]) == 163020
#         assert dataset.data[0][:300] == 'bla'
#         assert len(dataset.data[1].split()) == 500


# class TestDataset:
#
#     def test_slice(self, dataset):
#         small_dataset = dataset[:2]
#         assert len(small_dataset) == 2
