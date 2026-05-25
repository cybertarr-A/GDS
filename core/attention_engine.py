class GDSAttentionEngine:

    @staticmethod
    def initialize_attention(manifold):
        for node in manifold.nodes.values():
            if not hasattr(node, "attention"):
                node.attention = 0.05

    @staticmethod
    def decay_attention(manifold, decay_rate=0.15, min_attention=0.05):
        for node in manifold.nodes.values():
            if not hasattr(node, "attention"):
                node.attention = min_attention
            else:
                node.attention = max(min_attention, node.attention * (1 - decay_rate))

    @staticmethod
    def propagate_attention(manifold, start_node_id, amount=1.0, visited=None):
        if visited is None:
            visited = set()

        if start_node_id not in manifold.nodes or start_node_id in visited:
            return

        visited.add(start_node_id)
        node = manifold.nodes[start_node_id]

        if not hasattr(node, "attention"):
            node.attention = 0.05
        node.attention = min(1.0, node.attention + amount)

        # Propagate to connected neighbors
        for connection in node.connections:
            target_id = connection["target"]
            weight = connection["weight"]
            propagation_amount = amount * weight * 0.5

            if propagation_amount > 0.02:
                GDSAttentionEngine.propagate_attention(
                    manifold, 
                    target_id, 
                    propagation_amount, 
                    visited
                )
