import asyncio
import traceback
from core.manifold import GDSManifold
from core.embedding_engine import GDSEmbeddingEngine
from core.memory_engine import GDSMemoryEngine
from core.reasoning_engine import GDSReasoningEngine
from core.prediction_engine import GDSPredictionEngine
from core.temporal_engine import GDSTemporalEngine
from core.attention_engine import GDSAttentionEngine
from core.clustering_engine import GDSClusteringEngine
from core.export_engine import GDSExportEngine


class GDSUniverseEngine:
    """
    Central Cognitive Orchestrator for GDS.
    Maintains thread-safe and async-safe states using non-blocking asyncio context locks.
    """

    def __init__(self):
        self.manifold = GDSManifold()
        self.embedding_engine = GDSEmbeddingEngine()
        self.memory_engine = GDSMemoryEngine()
        self.prediction_engine = GDSPredictionEngine()
        self.temporal_engine = GDSTemporalEngine()
        
        self.is_running = False
        self.lock = asyncio.Lock()  # Migrated to asyncio.Lock to avoid thread-mix race conditions
        self.latest_event = "Universe initialized"

    def initialize(self, training_data):
        """Standard baseline knowledge mapping during server startup."""
        # 1. Fit tf-idf vectors
        self.embedding_engine.fit(training_data)
        
        # 2. Build initial nodes
        for i, text in enumerate(training_data):
            vector = self.embedding_engine.encode(text)[0]
            self.manifold.add_node(i, text, vector)
            node = self.manifold.nodes[i]
            node.energy = 0.5 + (i * 0.05) % 0.5
            node.importance = 0.5 + (i * 0.07) % 0.5
            node.attention = 0.05
            self.memory_engine.store(i, text, vector)
        
        # 3. Build top-K semantic edges
        self.manifold.build_connections(threshold=0.005)
        
        # 4. Cluster manifold spatial coordinates
        GDSClusteringEngine.cluster_manifold(self.manifold, num_clusters=3)
        
        # 5. Persist to DB and timeline
        GDSExportEngine.save_graph(self.manifold)
        self.temporal_engine.record_snapshot(self.manifold, "Knowledge Base Initialized")

    def get_serializable_nodes(self):
        nodes = []
        for node in self.manifold.nodes.values():
            nodes.append({
                "id": node.id,
                "content": node.content,
                "energy": float(getattr(node, "energy", 0.5)),
                "importance": float(getattr(node, "importance", 0.5)),
                "attention": float(getattr(node, "attention", 0.05)),
                "cluster": int(getattr(node, "cluster", 0)),
                "x": float(getattr(node, "x", 0.0)),
                "y": float(getattr(node, "y", 0.0)),
                "z": float(getattr(node, "z", 0.0))
            })
        return nodes

    def get_serializable_edges(self):
        edges = []
        for node in self.manifold.nodes.values():
            for conn in node.connections:
                edges.append({
                    "source": node.id,
                    "target": conn["target"],
                    "weight": float(conn["weight"])
                })
        return edges

    async def trigger_reasoning(self, start_node_id, max_depth=5):
        """Asynchronously triggers reasoning traverse path."""
        async with self.lock:
            if start_node_id not in self.manifold.nodes:
                return None
                
            res = GDSReasoningEngine.traverse(self.manifold, start_node_id, max_depth)
            
            # Propagate attention waves
            for step in res["path"]:
                GDSAttentionEngine.propagate_attention(self.manifold, step["id"], amount=0.8)
                
            # Predict branches
            self.prediction_engine.learn_path(res["path"])
            self.manifold.reasoning_path = [step["id"] for step in res["path"]]
            self.latest_event = f"Reasoning path generated from Node {start_node_id}"
            
            GDSExportEngine.save_graph(self.manifold)
            self.temporal_engine.record_snapshot(self.manifold, self.latest_event)
            return res

    async def trigger_prediction(self, start_node_id):
        """Asynchronously projects alternate futures."""
        async with self.lock:
            if start_node_id not in self.manifold.nodes:
                return None
            
            futures = self.prediction_engine.predict_alternate_futures(self.manifold, start_node_id)
            self.latest_event = f"Predicted branching futures from Node {start_node_id}"
            self.temporal_engine.record_snapshot(self.manifold, self.latest_event)
            return futures

    async def inject_thought(self, text):
        """Asynchronously injects a manual semantic concept."""
        async with self.lock:
            new_id = len(self.manifold.nodes)
            while new_id in self.manifold.nodes:
                new_id += 1
                
            vector = self.embedding_engine.encode(text)[0]
            self.manifold.add_node(new_id, text, vector)
            node = self.manifold.nodes[new_id]
            node.energy = 0.8
            node.importance = 0.7
            node.attention = 1.0
            
            self.memory_engine.store(new_id, text, vector)
            self.manifold.build_connections(threshold=0.005)
            GDSClusteringEngine.cluster_manifold(self.manifold, num_clusters=3)
            GDSAttentionEngine.propagate_attention(self.manifold, new_id, amount=1.0)
            
            self.latest_event = f"Injected Manual Thought: Node {new_id}"
            
            GDSExportEngine.save_graph(self.manifold)
            self.temporal_engine.record_snapshot(self.manifold, self.latest_event)
            return new_id
