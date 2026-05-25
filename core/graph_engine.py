import random
from core.vector_utils import VectorUtils
from core.synthesis_engine import GDSSynthesisEngine

class GDSGraphEngine:
    """
    Manages autonomous graph edge evolutions, relationship discovery,
    and connection decays on the manifold.
    """

    @staticmethod
    def evolve_universe(manifold, embedding_engine, memory_engine):
        """Perform autonomous graph restructuring, node generation, and relationship discovery."""
        if len(manifold.nodes) < 2:
            return None

        event_logs = []

        # ----------------------------------------------------
        # 1. Autonomous Edge Generation & Similarity Discovery
        # ----------------------------------------------------
        node_ids = list(manifold.nodes.keys())

        # Scan 5 random pairs to see if new relationships emerge
        for _ in range(5):
            u, v = random.sample(node_ids, 2)
            node_u = manifold.nodes[u]

            # Check if already connected
            already_connected = any(conn["target"] == v for conn in node_u.connections)

            if not already_connected:
                sim = VectorUtils.cosine_similarity(node_u.vector, manifold.nodes[v].vector)
                if sim > 0.05:  # High enough similarity
                    node_u.add_connection(v, float(sim))
                    manifold.nodes[v].add_connection(u, float(sim))
                    event_logs.append(f"Discovered relationship: Node {u} ↔ Node {v}")

        # ----------------------------------------------------
        # 2. Autonomous Node Synthesis (Emergent Thoughts)
        # ----------------------------------------------------
        # Merges thoughts autonomously inside the active loop
        if random.random() < 0.25:
            event = GDSSynthesisEngine.synthesize_emergent_thought(
                manifold, 
                embedding_engine, 
                memory_engine
            )
            if event:
                event_logs.append(event)

        # ----------------------------------------------------
        # 3. Connection Decay & Restructuring
        # ----------------------------------------------------
        pruned_edges = 0
        for node in manifold.nodes.values():
            keep_connections = []
            for conn in node.connections:
                # Slowly decay connection weight if unused
                if conn.get("usage", 0) == 0:
                    conn["weight"] *= 0.98  # 2% decay
                
                # Reset usage
                conn["usage"] = 0

                # Pruning threshold
                if conn["weight"] >= 0.005:
                    keep_connections.append(conn)
                else:
                    pruned_edges += 1

            node.connections = keep_connections

        if pruned_edges > 0:
            event_logs.append(f"Pruned {pruned_edges} decayed connections from manifold")

        return event_logs[0] if event_logs else None
