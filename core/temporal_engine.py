import time


class GDSTemporalEngine:

    def __init__(self):
        self.timeline = []  # List of snapshots
        self.is_playing = True
        self.playback_speed = 1.0
        self.play_direction = 1  # 1 = forward, -1 = reverse
        self.current_frame = 0
        self.max_snapshots = 100

    def record_snapshot(self, manifold, event_desc=""):
        nodes = []
        edges = []

        for node in manifold.nodes.values():
            nodes.append({
                "id": node.id,
                "content": node.content,
                "energy": getattr(node, "energy", 0.5),
                "importance": getattr(node, "importance", 0.5),
                "attention": getattr(node, "attention", 0.05),
                "cluster": getattr(node, "cluster", 0),
                "x": getattr(node, "x", 0.0),
                "y": getattr(node, "y", 0.0),
                "z": getattr(node, "z", 0.0)
            })

            for conn in node.connections:
                edges.append({
                    "source": node.id,
                    "target": conn["target"],
                    "weight": conn["weight"]
                })

        snapshot = {
            "frame": len(self.timeline),
            "timestamp": time.time(),
            "event": event_desc,
            "nodes": nodes,
            "edges": edges,
            "reasoning_path": getattr(manifold, "reasoning_path", [])
        }

        self.timeline.append(snapshot)

        # Limit size
        if len(self.timeline) > self.max_snapshots:
            self.timeline.pop(0)
            # Re-index frames
            for idx, snap in enumerate(self.timeline):
                snap["frame"] = idx

        self.current_frame = len(self.timeline) - 1
        return snapshot

    def get_snapshot(self, frame_idx):
        if not self.timeline:
            return None
        frame_idx = max(0, min(frame_idx, len(self.timeline) - 1))
        return self.timeline[frame_idx]

    def set_playing(self, playing: bool):
        self.is_playing = playing

    def set_direction(self, direction: int):
        self.play_direction = direction  # 1 or -1

    def set_speed(self, speed: float):
        self.playback_speed = max(0.1, min(speed, 10.0))

    def step(self):
        """Advance or rewind the playback frame pointer."""
        if not self.timeline or not self.is_playing:
            return self.current_frame

        delta = self.play_direction
        self.current_frame = (self.current_frame + delta) % len(self.timeline)
        return self.current_frame