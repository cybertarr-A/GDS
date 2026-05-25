from core.attention_field_engine import GDSAttentionFieldEngine

class GDSAttentionEngine:
    """
    Backward-compatible Attention Engine delegating to advanced
    GDSAttentionFieldEngine wave and propagation layers.
    """

    @staticmethod
    def initialize_attention(manifold):
        for node in manifold.nodes.values():
            if not hasattr(node, "attention"):
                node.attention = 0.05

    @staticmethod
    def decay_attention(manifold, decay_rate=0.15, min_attention=0.05):
        GDSAttentionFieldEngine.decay_attention_field(
            manifold, 
            decay_rate=decay_rate, 
            base_level=min_attention
        )

    @staticmethod
    def propagate_attention(manifold, start_node_id, amount=1.0, visited=None):
        GDSAttentionFieldEngine.propagate_attention_field(
            manifold, 
            start_node_id, 
            amount=amount, 
            visited=visited
        )
