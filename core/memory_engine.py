from core.vector_utils import VectorUtils


class GDSMemoryEngine:

    def __init__(self):

        self.memory_store=[]


    def store(
        self,
        node_id,
        content,
        vector
    ):

        self.memory_store.append({

            "id":node_id,

            "content":content,

            "vector":vector

        })


    def recall(
        self,
        query_vector,
        top_k=3,
        similarity_threshold=0.05
    ):

        results=[]


        for memory in self.memory_store:

            score=(
                VectorUtils.cosine_similarity(
                    query_vector,
                    memory["vector"]
                )
            )

            # Ignore irrelevant matches
            if score >= similarity_threshold:

                results.append({

                    "id":memory["id"],

                    "content":
                    memory["content"],

                    "score":
                    score

                })


        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )

        return results[:top_k]