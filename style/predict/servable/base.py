from abc import ABC
from abc import abstractmethod

import dill

from style.constants import MODEL_EXPORT_PATH


class BaseServable(ABC):
    SCHEMA_SLUG = "schema.json"
    MODEL_TYPE: str
    MODEL_VARIANT: str

    @abstractmethod
    def export(self, path):
        raise NotImplementedError

    @abstractmethod
    def run_inference(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def load(cls, path):
        raise NotImplementedError


class SklearnBasedClassifierServable(BaseServable):

    MODEL_VARIANT = "sklearn-classification"

    def __init__(self, model):
        self.model = model

    def export(self, path):
        with open(path, "wb") as f:
            dill.dump(self.model, f)

    def run_inference(self, texts):
        pass

    @classmethod
    def load(cls, path):
        dill.load(path)
