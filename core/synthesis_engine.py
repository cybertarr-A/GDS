import random
from core.vector_utils import VectorUtils

class GDSSynthesisEngine:
    """
    Autonomous Synthesis Engine.
    Enables self-evolving memory systems by merging existing concepts into emergent thoughts.
    """

    @staticmethod
    def synthesize_emergent_thought(manifold, embedding_engine, memory_engine, max_nodes=40):
        """
        Autonomously discovers and merges semantically aligned parent concepts.
        Restructures the graph by injecting emergent hypothesis nodes.
        """
        if len(manifold.nodes) < 2 or len(manifold.nodes) >= max_nodes:
            return None

        node_ids = list(manifold.nodes.keys())
        best_pair = None
        best_sim = -1.0

        # Scan pairs to find highly aligned thoughts to merge
        for _ in range(15):
            u, v = random.sample(node_ids, 2)
            sim = VectorUtils.cosine_similarity(manifold.nodes[u].vector, manifold.nodes[v].vector)
            if sim > best_sim:
                best_sim = sim
                best_pair = (u, v)

        if best_pair and best_sim > 0.05:
            u, v = best_pair
            node_u = manifold.nodes[u]
            node_v = manifold.nodes[v]

            # Merge concepts
            templates = [
                "Synthesized: {c1} correlates with {c2}",
                "Synthesis shows {c1} which leads to {c2}",
                "Integrating {c1} and {c2} forms an emergent intelligence framework",
                "Emergent manifold: {c1} directly shapes the evolution of {c2}"
            ]
            
            c1 = node_u.content.replace("Synthesized: ", "").replace("Synthesis shows ", "")
            c2 = node_v.content.replace("Synthesized: ", "").replace("Synthesis shows ", "")
            
            synthesized_text = random.choice(templates).format(c1=c1.lower(), c2=c2.lower())
            
            # Find unique new ID
            new_id = len(manifold.nodes)
            while new_id in manifold.nodes:
                new_id += 1

            # Encode emergent concept vector
            vector = embedding_engine.encode(synthesized_text)[0]

            # Inject node
            manifold.add_node(new_id, synthesized_text, vector)
            new_node = manifold.nodes[new_id]
            new_node.energy = float((node_u.energy + node_v.energy) / 2.0)
            new_node.importance = float((node_u.importance + node_v.importance) / 2.0 + 0.1)
            new_node.attention = 1.0  # Spikes active attention

            # Store in local memory
            memory_engine.store(new_id, synthesized_text, vector)

            # Discover semantic links
            new_node.add_connection(u, float(best_sim))
            new_node.add_connection(v, float(best_sim))
            node_u.add_connection(new_id, float(best_sim))
            node_v.add_connection(new_id, float(best_sim))

            # Restructure manifold relationships
            manifold.build_connections(threshold=0.005)
            
            return f"Synthesized Node {new_id}: '{synthesized_text}' from Nodes {u} & {v}"

        return None
