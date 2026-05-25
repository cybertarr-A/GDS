from collections import defaultdict
from core.vector_utils import VectorUtils


class GDSPredictionEngine:

    def __init__(self):
        self.transitions = defaultdict(list)

    def learn_path(self, reasoning_path):
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

        best = max(counts, key=counts.get)
        return best

    def predict_alternate_futures(self, manifold, current_node, max_branches=3, depth=3):
        """Predict branching future pathways with confidence weights."""
        if current_node not in manifold.nodes:
            return []

        candidates = self.transitions.get(current_node, [])
        
        # Calculate transition frequencies
        counts = {}
        for c in candidates:
            if c in manifold.nodes:
                counts[c] = counts.get(c, 0) + 1

        # Fallback to high-similarity neighbors if no recorded transitions exist
        if not counts:
            node = manifold.nodes[current_node]
            for conn in node.connections:
                target = conn["target"]
                counts[target] = conn["weight"] * 5  # weight similarity scale

        if not counts:
            return []

        # Find top branches
        sorted_branches = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:max_branches]
        total_weight = sum(w for _, w in sorted_branches) or 1.0

        branching_futures = []

        for branch_id, weight in sorted_branches:
            confidence = float(weight / total_weight)
            path = [current_node, branch_id]
            
            # Predict ahead up to 'depth' steps
            curr = branch_id
            for _ in range(depth - 1):
                nxt = self.predict_next(curr)
                if nxt is None or nxt in path or nxt not in manifold.nodes:
                    # Fallback to high similarity next connection
                    conn_candidates = manifold.nodes[curr].connections
                    if conn_candidates:
                        # pick best similarity not already in path
                        avail = [c for c in conn_candidates if c["target"] not in path]
                        if avail:
                            nxt = sorted(avail, key=lambda x: x["weight"], reverse=True)[0]["target"]
                
                if nxt is not None and nxt in manifold.nodes:
                    path.append(nxt)
                    curr = nxt
                else:
                    break

            branching_futures.append({
                "confidence": confidence,
                "path": path
            })

        return branching_futures