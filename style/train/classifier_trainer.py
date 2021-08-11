from typing import List

from sklearn.pipeline import Pipeline

from style.predict.servable.base import BaseServable


def train_sklearn_classification_model(
    data: List[str],
    export_path: str,
    pipeline: Pipeline,
    params: dict,
    train_percentage: float = 0.8,
    test_percentage: float = 0.2,
) -> BaseServable:
    """This method trains multiple models via GridSearchCV and it creates a servable
    from the best model.


    See https://scikit-learn.org/stable/tutorial/statistical_inference/putting_together.html for more details."""

    servable = None

    # When the model is ready, initiate it and return at the end.
    # from style.predict.servable.base import SklearnBasedClassifierServable
    # servable = SklearnBasedClassifierServable(model=model).export(export_path)

    return servable
