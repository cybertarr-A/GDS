import asyncio
import traceback
from core.clustering_engine import GDSClusteringEngine
from core.attention_engine import GDSAttentionEngine
from core.graph_engine import GDSGraphEngine
from core.export_engine import GDSExportEngine

class GDSOrchestrator:
    """
    Central Asynchronous Universe Orchestrator.
    Manages non-blocking simulation loops, WebSocket broadcasts, and temporal captures.
    """

    def __init__(self, universe):
        self.universe = universe
        self.sim_task = None
        self.lock = asyncio.Lock()
        self.step_count = 0

    def start(self, interval_seconds=4.0, broadcast_callback=None):
        """Starts the cognitive evolution cycle inside the active asyncio loop."""
        if self.sim_task and not self.sim_task.done():
            print("[WARNING] Asynchronous simulation is already active.")
            return

        self.universe.is_running = True
        self.sim_task = asyncio.create_task(
            self._simulation_loop(interval_seconds, broadcast_callback)
        )
        print("[INFO] Asynchronous Universe Orchestrator Loop Active.")

    def stop(self):
        """Halts the cognitive simulation cleanly."""
        self.universe.is_running = False
        if self.sim_task:
            self.sim_task.cancel()
            print("[INFO] Asynchronous Universe Orchestrator Loop Halted.")

    async def _simulation_loop(self, interval_seconds, broadcast_callback):
        while self.universe.is_running:
            try:
                # Dynamic speed calculation
                speed = self.universe.temporal_engine.playback_speed
                sleep_duration = max(0.1, interval_seconds / speed)
                await asyncio.sleep(sleep_duration)

                # Skip execution if play head is paused
                if not self.universe.temporal_engine.is_playing:
                    continue

                async with self.lock:
                    self.step_count += 1
                    event = None

                    # 1. Decay attention zones
                    GDSAttentionEngine.decay_attention(self.universe.manifold)

                    # 2. Graph dynamic synthesis (every 3 steps)
                    if self.step_count % 3 == 0:
                        event = GDSGraphEngine.evolve_universe(
                            self.universe.manifold,
                            self.universe.embedding_engine,
                            self.universe.memory_engine
                        )
                        if event:
                            self.universe.latest_event = event

                    # 3. Dynamic clustering constellation alignment (every 5 steps)
                    if self.step_count % 5 == 0:
                        GDSClusteringEngine.cluster_manifold(self.universe.manifold, num_clusters=3)

                    # 4. Capture state snapshot frame
                    self.universe.temporal_engine.record_snapshot(
                        self.universe.manifold,
                        event or "Manifold state decayed/synchronized"
                    )

                    # 5. SQLite state persistences
                    GDSExportEngine.save_graph(self.universe.manifold)
                    GDSExportEngine.save_memory(self.universe.memory_engine.memory_store)

                # 6. Low-latency WebSocket broadcasts
                if broadcast_callback:
                    payload = {
                        "type": "state_update",
                        "event": event or "Continuous simulation drift",
                        "frame": self.universe.temporal_engine.current_frame,
                        "timeline_size": len(self.universe.temporal_engine.timeline),
                        "nodes": self.universe.get_serializable_nodes(),
                        "edges": self.universe.get_serializable_edges()
                    }
                    if asyncio.iscoroutinefunction(broadcast_callback):
                        await broadcast_callback(payload)
                    else:
                        broadcast_callback(payload)

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[ERROR] Exception in Orchestrator loop: {e}")
                traceback.print_exc()
                await asyncio.sleep(1.0)
