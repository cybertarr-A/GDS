import sqlite3
import json
import numpy as np
from datetime import datetime

class GDSPersistenceEngine:
    """
    Relational and vector persistence manager for the Living Intelligence Universe.
    Utilizes SQLite as the core database engine and implements numpy-based cosine memory search.
    """

    def __init__(self, db_path="data/gds_universe.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initializes database schema tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. Nodes Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS nodes (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                vector TEXT NOT NULL,
                energy REAL DEFAULT 0.5,
                importance REAL DEFAULT 0.5,
                attention REAL DEFAULT 0.05,
                cluster INTEGER DEFAULT 0,
                x REAL DEFAULT 0.0,
                y REAL DEFAULT 0.0,
                z REAL DEFAULT 0.0
            )
        """)

        # 2. Edges Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS edges (
                source INTEGER,
                target INTEGER,
                weight REAL,
                PRIMARY KEY (source, target)
            )
        """)

        # 3. Snapshots (Temporal History) Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS snapshots (
                frame INTEGER PRIMARY KEY,
                timestamp TEXT,
                event TEXT,
                nodes_data TEXT,
                edges_data TEXT
            )
        """)

        # 4. Episodic Memories Table (Semantic Memory Vectors)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                vector TEXT NOT NULL,
                timestamp TEXT
            )
        """)

        conn.commit()
        conn.close()

    def save_universe(self, manifold, timeline):
        """Persists the entire active universe state to SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Clear existing graph nodes and edges
        cursor.execute("DELETE FROM nodes")
        cursor.execute("DELETE FROM edges")

        # Save Nodes
        for node in manifold.nodes.values():
            vector_str = json.dumps(node.vector.tolist() if isinstance(node.vector, np.ndarray) else list(node.vector))
            cursor.execute("""
                INSERT INTO nodes (id, content, vector, energy, importance, attention, cluster, x, y, z)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                node.id,
                node.content,
                vector_str,
                getattr(node, "energy", 0.5),
                getattr(node, "importance", 0.5),
                getattr(node, "attention", 0.05),
                getattr(node, "cluster", 0),
                getattr(node, "x", 0.0),
                getattr(node, "y", 0.0),
                getattr(node, "z", 0.0)
            ))

        # Save Edges
        saved_edges = set()
        for node in manifold.nodes.values():
            for conn_edge in node.connections:
                source = node.id
                target = conn_edge["target"]
                weight = conn_edge["weight"]
                
                # Deduplicate undirected edges
                key = tuple(sorted((source, target)))
                if key not in saved_edges:
                    cursor.execute("""
                        INSERT OR REPLACE INTO edges (source, target, weight)
                        VALUES (?, ?, ?)
                    """, (source, target, weight))
                    saved_edges.add(key)

        # Clear and Save Snapshots (Timeline)
        cursor.execute("DELETE FROM snapshots")
        for snap in timeline:
            cursor.execute("""
                INSERT INTO snapshots (frame, timestamp, event, nodes_data, edges_data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                snap["frame"],
                snap["timestamp"],
                snap["event"],
                json.dumps(snap["nodes"]),
                json.dumps(snap["edges"])
            ))

        conn.commit()
        conn.close()

    def load_universe(self, manifold, temporal_engine):
        """Loads persistent database states into active memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. Load Nodes
        cursor.execute("SELECT id, content, vector, energy, importance, attention, cluster, x, y, z FROM nodes")
        nodes_rows = cursor.fetchall()
        
        if not nodes_rows:
            conn.close()
            return False

        manifold.nodes.clear()
        for row in nodes_rows:
            node_id, content, vector_str, energy, importance, attention, cluster, x, y, z = row
            vector = np.array(json.loads(vector_str))
            
            # Reconstruct node
            manifold.add_node(node_id, content, vector)
            node = manifold.nodes[node_id]
            node.energy = energy
            node.importance = importance
            node.attention = attention
            node.cluster = cluster
            node.x = x
            node.y = y
            node.z = z

        # 2. Load Edges
        cursor.execute("SELECT source, target, weight FROM edges")
        edges_rows = cursor.fetchall()
        for row in edges_rows:
            source, target, weight = row
            if source in manifold.nodes and target in manifold.nodes:
                manifold.nodes[source].add_connection(target, weight)
                manifold.nodes[target].add_connection(source, weight)

        # 3. Load Timeline Snapshots
        cursor.execute("SELECT frame, timestamp, event, nodes_data, edges_data FROM snapshots ORDER BY frame ASC")
        snap_rows = cursor.fetchall()
        temporal_engine.timeline.clear()
        for row in snap_rows:
            frame, timestamp, event, nodes_str, edges_str = row
            temporal_engine.timeline.append({
                "frame": frame,
                "timestamp": timestamp,
                "event": event,
                "nodes": json.loads(nodes_str),
                "edges": json.loads(edges_str)
            })

        conn.close()
        return True

    def store_memory(self, content, vector):
        """Saves a semantic experience memory to SQLite."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        vector_str = json.dumps(vector.tolist() if isinstance(vector, np.ndarray) else list(vector))
        timestamp = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO memories (content, vector, timestamp)
            VALUES (?, ?, ?)
        """, (content, vector_str, timestamp))

        conn.commit()
        conn.close()
        print(f"[INFO] Persisted memory: '{content}'")

    def search_memory(self, query_vector, top_k=5):
        """Performs optimized vector search with Cosine distance indexing in NumPy."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, content, vector, timestamp FROM memories")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            return []

        q_vec = np.array(query_vector)
        q_norm = np.linalg.norm(q_vec)
        
        if q_norm == 0:
            return []

        results = []
        for row in rows:
            mem_id, content, vector_str, timestamp = row
            m_vec = np.array(json.loads(vector_str))
            
            # Compute cosine similarity
            m_norm = np.linalg.norm(m_vec)
            if m_norm == 0:
                continue

            similarity = np.dot(q_vec, m_vec) / (q_norm * m_norm)
            results.append({
                "id": mem_id,
                "content": content,
                "score": float(similarity),
                "timestamp": timestamp
            })

        # Sort similarity descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

    def get_memory_history(self):
        """Returns all memories stored sequentially."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, timestamp FROM memories ORDER BY id DESC")
        rows = cursor.fetchall()
        conn.close()

        return [{"id": r[0], "content": r[1], "timestamp": r[2]} for r in rows]
