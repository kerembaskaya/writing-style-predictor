from typing import List

import dill
from sklearn import metrics
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from style.constants import FILE_PATH_BOOK_DB
from style.dataset.reader import Dataset
from style.dataset.reader import DatasetReader
from style.predict.servable.base import BaseServable


def train_sklearn_classification_model(
    dataset: Dataset,
    export_path: str,
    pipeline: Pipeline,
    grid_search_params: dict,
    test_percentage: float = 0.2,
) -> BaseServable:
    """This method trains multiple models via GridSearchCV and it creates a servable
    from the best model.



    See https://scikit-learn.org/stable/tutorial/statistical_inference/putting_together.html for more details.
    """
    servable = None
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=test_percentage
    )
    grid_search = GridSearchCV(pipeline, grid_search_params, n_jobs=-1)
    print(len(docs_train), len(docs_test))
    grid_search.fit(docs_train, y_train)
    y_predicted = grid_search.predict(docs_test)
    # print(y_predicted)
    metrics.classification_report(y_test, y_predicted, target_names=set(dataset.target))

    #    cm = metrics.confusion_matrix(y_test, y_predicted)
    #    print(cm)

    # When the model is ready, initiate it and return at the end.
    # from style.predict.servable.base import SklearnBasedClassifierServable
    # servable = SklearnBasedClassifierServable(model=model).export(export_path)
    return servable


def run():
    pipeline = Pipeline(
        [
            (
                "vect",
                TfidfVectorizer(ngram_range=(1, 3), analyzer="char", use_idf=False),
            ),
            ("clf", LinearSVC(C=1)),
        ]
    )

    parameters = {"vect__ngram_range": [(1, 1), (1, 2)]}

    dataset = DatasetReader.load_files(FILE_PATH_BOOK_DB)
    print(len(dataset))
    # dataset = load_files(FILE_PATH_BOOK_DB)
    dataset.shuffle()

    train_sklearn_classification_model(dataset, "/tmp/models", pipeline, parameters)


if __name__ == "__main__":
    run()
