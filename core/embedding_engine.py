from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from typing import Union, List


class GDSEmbeddingEngine:
    """
    Lightweight embedding engine for GDS.
    Converts text into vector representations.
    """

    def __init__(self):

        self.vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=1000,
    ngram_range=(1,2),
    lowercase=True
    )

        self.is_fitted = False


    def fit(self, texts: List[str]):

        try:
            self.vectorizer.fit(texts)
            self.is_fitted = True

        except Exception as e:
            raise RuntimeError(
                f"Fit error: {e}"
            )


    def encode(
        self,
        texts: Union[str, List[str]]
    ):

        try:

            if not self.is_fitted:
                raise RuntimeError(
                    "Vectorizer not fitted."
                )

            if isinstance(texts, str):
                texts = [texts]

            vectors = self.vectorizer.transform(
                texts
            )

            return vectors.toarray()

        except Exception as e:
            raise RuntimeError(
                f"Encoding error: {e}"
            )


    def embedding_dimension(self):

        return len(
            self.vectorizer.get_feature_names_out()
        )