import random
import numpy as np
from core.vector_utils import VectorUtils


class GDSGraphEngine:

    @staticmethod
    def synthesize_thoughts(node1, node2):
        """Combine two concepts into an emergent synthesis node."""
        templates = [
            "Synthesized: {c1} correlates with {c2}",
            "Synthesis shows {c1} which leads to {c2}",
            "Integrating {c1} and {c2} forms an emergent intelligence framework",
            "Emergent manifold: {c1} directly shapes the evolution of {c2}"
        ]
        
        # Clean content (strip prefixes if any)
        c1 = node1.content.replace("Synthesized: ", "").replace("Synthesis shows ", "")
        c2 = node2.content.replace("Synthesized: ", "").replace("Synthesis shows ", "")
        
        # Mix templates
        template = random.choice(templates)
        return template.format(c1=c1.lower(), c2=c2.lower())

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
        discovered_edges = 0

        # Scan pairs
        for _ in range(5):  # check 5 random pairs
            u, v = random.sample(node_ids, 2)
            node_u = manifold.nodes[u]
            node_v = manifold.nodes[v]

            # Check if already connected
            already_connected = False
            for conn in node_u.connections:
                if conn["target"] == v:
                    already_connected = True
                    break

            if not already_connected:
                sim = VectorUtils.cosine_similarity(node_u.vector, node_v.vector)
                if sim > 0.05:  # High enough similarity
                    node_u.add_connection(v, float(sim))
                    node_v.add_connection(u, float(sim))
                    discovered_edges += 1
                    event_logs.append(f"Discovered relationship: Node {u} ↔ Node {v}")

        # ----------------------------------------------------
        # 2. Autonomous Node Synthesis (Emergent Thoughts)
        # ----------------------------------------------------
        # Occasional synthesis (20% chance per evolution cycle)
        if random.random() < 0.25 and len(manifold.nodes) < 30:
            # Pick 2 nodes with reasonable similarity to combine
            best_pair = None
            best_sim = -1

            for _ in range(10):
                u, v = random.sample(node_ids, 2)
                sim = VectorUtils.cosine_similarity(manifold.nodes[u].vector, manifold.nodes[v].vector)
                if sim > best_sim:
                    best_sim = sim
                    best_pair = (u, v)

            if best_pair and best_sim > 0.02:
                u, v = best_pair
                node_u = manifold.nodes[u]
                node_v = manifold.nodes[v]

                synthesized_text = GDSGraphEngine.synthesize_thoughts(node_u, node_v)
                new_id = len(manifold.nodes)
                
                # Make sure ID is unique
                while new_id in manifold.nodes:
                    new_id += 1

                # Encode
                vector = embedding_engine.encode(synthesized_text)[0]

                manifold.add_node(new_id, synthesized_text, vector)
                new_node = manifold.nodes[new_id]
                new_node.energy = float((node_u.energy + node_v.energy) / 2)
                new_node.importance = float((node_u.importance + node_v.importance) / 2 + 0.1)

                memory_engine.store(new_id, synthesized_text, vector)

                # Connect to parents
                new_node.add_connection(u, float(best_sim))
                new_node.add_connection(v, float(best_sim))
                node_u.add_connection(new_id, float(best_sim))
                node_v.add_connection(new_id, float(best_sim))

                # Re-build connections with manifold
                manifold.build_connections(threshold=0.02)

                event_logs.append(f"Synthesized Node {new_id}: '{synthesized_text}' from Nodes {u} & {v}")

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
