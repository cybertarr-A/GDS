import time
import threading
import traceback
from core.manifold import GDSManifold
from core.embedding_engine import GDSEmbeddingEngine
from core.memory_engine import GDSMemoryEngine
from core.reasoning_engine import GDSReasoningEngine
from core.prediction_engine import GDSPredictionEngine
from core.temporal_engine import GDSTemporalEngine
from core.attention_engine import GDSAttentionEngine
from core.graph_engine import GDSGraphEngine
from core.clustering_engine import GDSClusteringEngine
from core.export_engine import GDSExportEngine


class GDSUniverseEngine:

    def __init__(self):
        self.manifold = GDSManifold()
        self.embedding_engine = GDSEmbeddingEngine()
        self.memory_engine = GDSMemoryEngine()
        self.prediction_engine = GDSPredictionEngine()
        self.temporal_engine = GDSTemporalEngine()
        
        self.is_running = False
        self.lock = threading.Lock()
        self.step_count = 0
        self.latest_event = "Universe initialized"

    def initialize(self, training_data):
        with self.lock:
            # 1. Fit embeddings
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
            
            # 3. Build edges
            self.manifold.build_connections(threshold=0.02)
            
            # 4. Perform clustering
            GDSClusteringEngine.cluster_manifold(self.manifold, num_clusters=3)
            
            # 5. Save baseline
            GDSExportEngine.save_graph(self.manifold)
            self.temporal_engine.record_snapshot(self.manifold, "Knowledge Base Initialized")

    def run_simulation_loop(self, interval_seconds=3.0, broadcast_callback=None):
        self.is_running = True
        print("[INFO] GDS Universe simulation loop started.")
        
        while self.is_running:
            try:
                time.sleep(interval_seconds / self.temporal_engine.playback_speed)
                
                # Check play/pause state
                if not self.temporal_engine.is_playing:
                    continue

                event = None
                with self.lock:
                    self.step_count += 1
                    
                    # 1. Attention decay
                    GDSAttentionEngine.decay_attention(self.manifold)
                    
                    # 2. Graph evolution (every 3 steps)
                    if self.step_count % 3 == 0:
                        event = GDSGraphEngine.evolve_universe(
                            self.manifold, 
                            self.embedding_engine, 
                            self.memory_engine
                        )
                        if event:
                            self.latest_event = event

                    # 3. Re-cluster (every 5 steps)
                    if self.step_count % 5 == 0:
                        GDSClusteringEngine.cluster_manifold(self.manifold, num_clusters=3)

                    # 4. Record Snapshot
                    self.temporal_engine.record_snapshot(
                        self.manifold, 
                        event or "Manifold state decayed/synchronized"
                    )
                    
                    # 5. Export state
                    GDSExportEngine.save_graph(self.manifold)
                    GDSExportEngine.save_memory(self.memory_engine.memory_store)

                if broadcast_callback:
                    # Stream the latest update
                    broadcast_callback({
                        "type": "state_update",
                        "event": event or "Continuous simulation drift",
                        "frame": self.temporal_engine.current_frame,
                        "timeline_size": len(self.temporal_engine.timeline),
                        "nodes": self.get_serializable_nodes(),
                        "edges": self.get_serializable_edges()
                    })

            except Exception as e:
                print(f"[ERROR] Exception in GDS Universe loop: {e}")
                traceback.print_exc()

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

    def trigger_reasoning(self, start_node_id, max_depth=5):
        with self.lock:
            if start_node_id not in self.manifold.nodes:
                return None
                
            res = GDSReasoningEngine.traverse(self.manifold, start_node_id, max_depth)
            
            # Propagate attention waves along path
            for step in res["path"]:
                GDSAttentionEngine.propagate_attention(self.manifold, step["id"], amount=0.8)
                
            # Learn reasoning paths for predictions
            self.prediction_engine.learn_path(res["path"])
            
            # Record reasoning path on manifold
            self.manifold.reasoning_path = [step["id"] for step in res["path"]]
            
            self.latest_event = f"Reasoning path generated from Node {start_node_id}"
            
            GDSExportEngine.save_graph(self.manifold)
            self.temporal_engine.record_snapshot(self.manifold, self.latest_event)
            return res

    def trigger_prediction(self, start_node_id):
        with self.lock:
            if start_node_id not in self.manifold.nodes:
                return None
            
            futures = self.prediction_engine.predict_alternate_futures(self.manifold, start_node_id)
            self.latest_event = f"Predicted branching futures from Node {start_node_id}"
            self.temporal_engine.record_snapshot(self.manifold, self.latest_event)
            return futures

    def inject_thought(self, text):
        with self.lock:
            new_id = len(self.manifold.nodes)
            while new_id in self.manifold.nodes:
                new_id += 1
                
            vector = self.embedding_engine.encode(text)[0]
            self.manifold.add_node(new_id, text, vector)
            node = self.manifold.nodes[new_id]
            node.energy = 0.8
            node.importance = 0.7
            node.attention = 1.0  # Spike attention
            
            self.memory_engine.store(new_id, text, vector)
            self.manifold.build_connections(threshold=0.02)
            
            # Recalculate clusters
            GDSClusteringEngine.cluster_manifold(self.manifold, num_clusters=3)
            
            # Propagate attention wave
            GDSAttentionEngine.propagate_attention(self.manifold, new_id, amount=1.0)
            
            self.latest_event = f"Injected Manual Thought: Node {new_id}"
            
            GDSExportEngine.save_graph(self.manifold)
            self.temporal_engine.record_snapshot(self.manifold, self.latest_event)
            return new_id
