import numpy as np


class VectorUtils:

    @staticmethod
    def cosine_similarity(v1, v2):

        denominator = (
            np.linalg.norm(v1)
            * np.linalg.norm(v2)
        )

        if denominator == 0:
            return 0

        return np.dot(v1, v2) / denominator


    @staticmethod
    def euclidean_distance(v1, v2):

        return np.linalg.norm(
            v1-v2
        )


    @staticmethod
    def normalize(v):

        norm = np.linalg.norm(v)

        if norm == 0:
            return v

        return v / norm