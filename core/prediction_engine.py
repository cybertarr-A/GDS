from collections import defaultdict
from core.prediction_branch_engine import GDSPredictionBranchEngine

class GDSPredictionEngine:
    """
    Cognitive state prediction manager. delegating to GDSPredictionBranchEngine
    to generate alternate probabilistic branches.
    """

    def __init__(self):
        self.transitions = defaultdict(list)

    def learn_path(self, reasoning_path):
        """Records reasoning sequence patterns."""
        for i in range(len(reasoning_path) - 1):
            current = reasoning_path[i]["id"]
            next_node = reasoning_path[i + 1]["id"]
            self.transitions[current].append(next_node)

    def predict_next(self, current_node):
        candidates = self.transitions.get(current_node, [])
        if not candidates:
            return None
        counts = {}
        for c in candidates:
            counts[c] = counts.get(c, 0) + 1
        return max(counts, key=counts.get)

    def predict_alternate_futures(self, manifold, current_node, max_branches=3, depth=3):
        """Asynchronously projects alternate futures using the Prediction Branch Engine."""
        return GDSPredictionBranchEngine.generate_branches(
            manifold, 
            self.transitions, 
            current_node, 
            max_branches=max_branches, 
            depth=depth
        )