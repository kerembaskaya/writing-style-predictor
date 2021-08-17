from pathlib import PosixPath

from sklearn import metrics
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from style.constants import FILE_PATH_BOOK_DB
from style.constants import MODEL_EXPORT_PATH
from style.dataset.reader import Dataset
from style.dataset.reader import DatasetReader
from style.predict.servable.base import SklearnBasedClassifierServable


class TextNormalizer:
    pass


def split_dataset(
    dataset: Dataset,
    test_percentage: float = 0.2,
    random_state: int = 42,
):
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data,
        dataset.target,
        test_size=test_percentage,
        random_state=random_state,
    )
    return docs_train, docs_test, y_train, y_test, dataset.target


def train_sklearn_classification_model(
    docs_train,
    docs_test,
    y_train,
    y_test,
    dataset_target,
    pipeline: Pipeline,
    grid_search_params: dict,
):
    """This method trains multiple models via GridSearchCV and it creates a servable
    from the best model.

    See https://scikit-learn.org/stable/tutorial/statistical_inference/putting_together.html for more details.


    """

    grid_search = GridSearchCV(pipeline, grid_search_params, n_jobs=-1, cv=2)
    grid_search.fit(docs_train, y_train)
    y_predicted = grid_search.predict(docs_test)

    report_ = metrics.classification_report(
        y_test, y_predicted, target_names=set(dataset_target)
    )
    confusion_matrix = metrics.confusion_matrix(y_test, y_predicted)

    return grid_search.best_estimator_, report_, confusion_matrix


# Q: burayi a yapmayinca eklemiyor. w ile sadece ustunu yazip eziyor.


def report(report_, confusion_matrix, export_path: PosixPath):
    with open(export_path / "report.txt", "a") as f:
        f.write(report_)
    with open(export_path / "cm.txt", "a") as f:
        f.write(f"{str(confusion_matrix)}\n")


def export(model, export_path):
    """
        # When the model is ready, initiate it and return at the end.
    # from style.predict.servable.base import SklearnBasedClassifierServable
    # servable = SklearnBasedClassifierServable(model=model).export(export_path)
    Returns:

    """
    SklearnBasedClassifierServable(model=model).export(export_path)


def create_pipeline(clf_name, estimator, normalize=False, reduction=False):
    steps = [("vectorize", TfidfVectorizer(analyzer="word", use_idf=True))]

    if normalize:
        steps.insert(0, ("normalize", TextNormalizer()))

    if reduction:
        steps.append(("reduction", TruncatedSVD(n_components=10000)))

    # Add the estimator
    steps.append((clf_name, estimator))
    return Pipeline(steps)


def run():
    classifiers = [
        ("clf_svc", LinearSVC),
        ("clf_nb", MultinomialNB),
        ("clf_lg", LogisticRegression),
        ("clf_sgd", SGDClassifier),
    ]

    parameters = [
        {"vectorize__ngram_range": [(1, 1), (1, 2)]},
        {"vectorize__ngram_range": [(1, 1), (1, 2)]},
        {"vectorize__ngram_range": [(1, 1), (1, 2)]},
        {"vectorize__ngram_range": [(1, 1), (1, 2)]},
    ]

    dataset = DatasetReader.load_files(FILE_PATH_BOOK_DB)
    print(len(dataset))
    dataset.shuffle()
    small_dataset = dataset[:200]
    docs_train, docs_test, y_train, y_test, dataset_target = split_dataset(
        small_dataset
    )

    for (name, clf), params in zip(classifiers, parameters):
        pipeline = create_pipeline(name, clf())
        model, report_, cm = train_sklearn_classification_model(
            docs_train, docs_test, y_train, y_test, dataset_target, pipeline, params
        )
        report(report_, cm, MODEL_EXPORT_PATH)


if __name__ == "__main__":
    run()
