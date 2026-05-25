from core.persistence_engine import GDSPersistenceEngine

class GDSExportEngine:
    """
    Deprecated file-based export module. Maintains exact backward-compatible 
    interfaces by delegating storage writes internally to the SQLite Persistence Engine.
    """
    db = GDSPersistenceEngine()

    @staticmethod
    def save_graph(manifold, filepath=None):
        # We delegate straight to SQLite save
        # temporal_engine reference has to be resolved or passed
        # Here we mock temporal timeline as empty if not reachable globally
        from core.shared import universe
        timeline = universe.temporal_engine.timeline if hasattr(universe, "temporal_engine") else []
        GDSExportEngine.db.save_universe(manifold, timeline)

    @staticmethod
    def load_graph(manifold, filepath=None):
        from core.shared import universe
        temp_engine = universe.temporal_engine if hasattr(universe, "temporal_engine") else None
        
        class MockTemporalEngine:
            timeline = []
            
        return GDSExportEngine.db.load_universe(manifold, temp_engine or MockTemporalEngine())

    @staticmethod
    def save_timeline(timeline, filepath=None):
        from core.shared import universe
        GDSExportEngine.db.save_universe(universe.manifold, timeline)

    @staticmethod
    def save_memory(memory_store, filepath=None):
        # Persist memory array entries
        for mem in memory_store:
            content = mem.get("content", "")
            vector = mem.get("vector")
            if content and vector is not None:
                GDSExportEngine.db.store_memory(content, vector)
