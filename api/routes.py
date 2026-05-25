from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.shared import universe

router = APIRouter()


class SpeedRequest(BaseModel):
    speed: float


@router.get("/")
def get_status():
    return {
        "status": "online",
        "universe_running": universe.is_running,
        "nodes_count": len(universe.manifold.nodes),
        "snapshots_count": len(universe.temporal_engine.timeline),
        "current_frame": universe.temporal_engine.current_frame,
        "latest_event": universe.latest_event,
        "playback": {
            "is_playing": universe.temporal_engine.is_playing,
            "speed": universe.temporal_engine.playback_speed,
            "direction": universe.temporal_engine.play_direction
        }
    }


# ==========================================
# Temporal Timeline Routes
# ==========================================

@router.get("/timeline")
def get_timeline():
    # Return list of snapshots (summary)
    summary = []
    for snap in universe.temporal_engine.timeline:
        summary.append({
            "frame": snap["frame"],
            "timestamp": snap["timestamp"],
            "event": snap["event"],
            "nodes_count": len(snap["nodes"]),
            "edges_count": len(snap["edges"])
        })
    return summary


@router.get("/timeline/{frame}")
def get_timeline_frame(frame: int):
    snapshot = universe.temporal_engine.get_snapshot(frame)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Frame snapshot not found")
    # Set current frame index to requested frame for scrubbing synchronization
    universe.temporal_engine.current_frame = frame
    return snapshot


@router.post("/timeline/play")
def play_timeline():
    universe.temporal_engine.set_playing(True)
    return {"status": "playing", "frame": universe.temporal_engine.current_frame}


@router.post("/timeline/pause")
def pause_timeline():
    universe.temporal_engine.set_playing(False)
    return {"status": "paused", "frame": universe.temporal_engine.current_frame}


@router.post("/timeline/reverse")
def reverse_timeline():
    # Toggle play direction
    new_dir = -1 if universe.temporal_engine.play_direction == 1 else 1
    universe.temporal_engine.set_direction(new_dir)
    return {"status": "direction_toggled", "direction": new_dir}


@router.post("/timeline/speed")
def speed_timeline(req: SpeedRequest):
    universe.temporal_engine.set_speed(req.speed)
    return {"status": "speed_updated", "speed": universe.temporal_engine.playback_speed}
