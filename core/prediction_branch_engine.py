import numpy as np

class GDSPredictionBranchEngine:
    """
    Advanced prediction engine capable of generating alternate timeline paths,
    confidence metrics, and branched trajectory trees.
    """

    @staticmethod
    def generate_branches(manifold, transition_history, start_node_id, max_branches=3, depth=3):
        """
        Calculates distinct alternate future branches starting from a node.
        Uses transition weights combined with node energy levels to assign confidence scores.
        """
        if start_node_id not in manifold.nodes:
            return []

        # Find historical transitions
        candidates = transition_history.get(start_node_id, [])
        counts = {}
        for c in candidates:
            if c in manifold.nodes:
                counts[c] = counts.get(c, 0) + 1.0

        # Fallback to high-similarity neighbor connections if no transition history
        if not counts:
            start_node = manifold.nodes[start_node_id]
            for conn in start_node.connections:
                target = conn["target"]
                counts[target] = conn["weight"] * 3.0

        if not counts:
            return []

        # Sort and take top branches
        sorted_targets = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:max_branches]
        total_counts = sum(w for _, w in sorted_targets) or 1.0

        futures = []
        for idx, (target_id, weight) in enumerate(sorted_targets):
            # Calculate branch probability / confidence
            confidence = float(weight / total_counts)
            
            # Formulate alternate timeline path
            path = [start_node_id, target_id]
            curr = target_id

            # Project alternate pathway ahead
            for _ in range(depth - 1):
                # Check target connection list
                curr_node = manifold.nodes[curr]
                conns = [c for c in curr_node.connections if c["target"] not in path]
                
                if conns:
                    # Pick target based on highest similarity weight * energy
                    conns_sorted = sorted(
                        conns, 
                        key=lambda x: x["weight"] * getattr(manifold.nodes[x["target"]], "energy", 0.5), 
                        reverse=True
                    )
                    nxt = conns_sorted[0]["target"]
                    path.append(nxt)
                    curr = nxt
                else:
                    break

            futures.append({
                "branch_id": idx,
                "confidence": confidence,
                "path": path,
                "outcome_label": f"Timeline Branch {chr(65 + idx)}" # Branch A, B, C...
            })

        return futures
