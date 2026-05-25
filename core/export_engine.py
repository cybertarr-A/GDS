import json
import os
from pathlib import Path


class GDSExportEngine:

    @staticmethod
    def save_graph(manifold, filepath="data/graph.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        nodes = []
        edges = []

        for node in manifold.nodes.values():
            nodes.append({
                "id": node.id,
                "content": node.content,
                "energy": getattr(node, "energy", 0.5),
                "importance": getattr(node, "importance", 0.5),
                "cluster": getattr(node, "cluster", 0),
                "vector": list(node.vector) if node.vector is not None else []
            })

            for connection in node.connections:
                edges.append({
                    "source": node.id,
                    "target": connection["target"],
                    "weight": connection["weight"]
                })

        data = {
            "nodes": nodes,
            "edges": edges,
            "reasoning_path": getattr(manifold, "reasoning_path", [])
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_graph(manifold, filepath="data/graph.json"):
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            import numpy as np
            manifold.nodes = {}
            for n in data.get("nodes", []):
                import numpy as np
                vector = np.array(n["vector"]) if n.get("vector") else np.zeros(100)
                manifold.add_node(n["id"], n["content"], vector)
                node = manifold.nodes[n["id"]]
                node.energy = n.get("energy", 0.5)
                node.importance = n.get("importance", 0.5)
                node.cluster = n.get("cluster", 0)

            for e in data.get("edges", []):
                source = e["source"]
                target = e["target"]
                weight = e["weight"]
                if source in manifold.nodes and target in manifold.nodes:
                    manifold.nodes[source].add_connection(target, weight)

            manifold.reasoning_path = data.get("reasoning_path", [])
            return True
        except Exception as e:
            print(f"[ERROR] Error loading graph: {e}")
            return False

    @staticmethod
    def save_timeline(timeline, filepath="data/timeline.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(timeline, f, indent=4)

    @staticmethod
    def save_memory(memory_store, filepath="data/memory.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        serializable = []
        for mem in memory_store:
            serializable.append({
                "id": mem["id"],
                "content": mem["content"],
                "vector": list(mem["vector"]) if mem.get("vector") is not None else []
            })
        with open(filepath, "w") as f:
            json.dump(serializable, f, indent=4)
