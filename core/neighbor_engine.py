from core.vector_utils import VectorUtils

class GDSNeighborEngine:
    """
    Cognitive neighbor engine to manage dynamic graph edge connectivity.
    Solves edge explosion by enforcing a Top-K nearest-neighbor configuration.
    """

    @staticmethod
    def build_nearest_neighbors(nodes, max_connections=3, similarity_threshold=0.005):
        """
        Builds a sparse nearest-neighbor graph representation.
        For each node, links it only to the Top-K semantically closest nodes.
        """
        # Clear existing connections first
        for node in nodes.values():
            node.connections = []

        node_ids = list(nodes.keys())
        all_similarities = {}

        # 1. Compute similarity matrix
        for i in range(len(node_ids)):
            for j in range(i + 1, len(node_ids)):
                id1 = node_ids[i]
                id2 = node_ids[j]
                node1 = nodes[id1]
                node2 = nodes[id2]

                score = VectorUtils.cosine_similarity(node1.vector, node2.vector)
                all_similarities[(id1, id2)] = score

        # 2. Assign Top-K neighbors per node
        for current_id, node in nodes.items():
            candidates = []
            
            for other_id in nodes.keys():
                if current_id == other_id:
                    continue

                # Fetch pre-calculated similarity from lookup
                key = tuple(sorted((current_id, other_id)))
                score = all_similarities.get(key, 0.0)

                if score >= similarity_threshold:
                    candidates.append((other_id, score))

            # Sort by cosine similarity score descending
            candidates.sort(key=lambda x: x[1], reverse=True)

            # Cap connections at Max Connections
            top_neighbors = candidates[:max_connections]

            for neighbor_id, score in top_neighbors:
                # Add directional edge (rendered as undirected visually)
                node.add_connection(neighbor_id, score)

                # Ensure mutual connection (undirected graph representation)
                neighbor_node = nodes[neighbor_id]
                already_connected = any(c["target"] == current_id for c in neighbor_node.connections)
                
                # Check neighbor constraints: only add if neighbor is below capacity or if mutual relation is highly semantic
                if not already_connected and len(neighbor_node.connections) < max_connections:
                    neighbor_node.add_connection(current_id, score)

    @staticmethod
    def prune_weak_connections(nodes, min_weight=0.005):
        """
        Prunes weak connections whose similarity falls below absolute minimum.
        """
        for node in nodes.values():
            node.connections = [c for c in node.connections if c["weight"] >= min_weight]
