from collections import defaultdict


class GDSPredictionEngine:

    def __init__(self):

        self.transitions = defaultdict(list)


    def learn_path(self, reasoning_path):

        for i in range(
            len(reasoning_path)-1
        ):

            current = (
                reasoning_path[i]["id"]
            )

            next_node = (
                reasoning_path[i+1]["id"]
            )

            self.transitions[
                current
            ].append(next_node)


    def predict_next(
        self,
        current_node
    ):

        candidates = (
            self.transitions.get(
                current_node,
                []
            )
        )

        if not candidates:

            return None


        counts = {}

        for c in candidates:

            counts[c] = (
                counts.get(c,0)+1
            )

        best = max(
            counts,
            key=counts.get
        )

        return best