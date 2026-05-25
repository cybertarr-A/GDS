import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
from core.shared import universe

router = APIRouter()

# Store of active connection streams
active_connections: Set[WebSocket] = set()


async def broadcast_to_all(payload: dict):
    """Utility to broadcast an update to all active visualizer sessions."""
    if not active_connections:
        return

    dead_connections = set()
    for websocket in active_connections:
        try:
            await websocket.send_json(payload)
        except Exception:
            dead_connections.add(websocket)

    for dead in dead_connections:
        active_connections.remove(dead)


@router.websocket("/api/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    print(f"[INFO] New WebSocket client connected. Active: {len(active_connections)}")

    # Immediately push current state
    try:
        await websocket.send_json({
            "type": "initial_state",
            "event": universe.latest_event,
            "frame": universe.temporal_engine.current_frame,
            "timeline_size": len(universe.temporal_engine.timeline),
            "playback": {
                "is_playing": universe.temporal_engine.is_playing,
                "speed": universe.temporal_engine.playback_speed,
                "direction": universe.temporal_engine.play_direction
            },
            "nodes": universe.get_serializable_nodes(),
            "edges": universe.get_serializable_edges(),
            "reasoning_path": getattr(universe.manifold, "reasoning_path", [])
        })
    except Exception as e:
        print(f"[ERROR] Failed to send initial state: {e}")
        active_connections.remove(websocket)
        return

    try:
        while True:
            # Wait for client payloads
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")

            if not action:
                continue

            response = None

            if action == "ping":
                response = {"type": "pong"}

            elif action == "inject":
                content = message.get("content", "")
                if content:
                    node_id = await universe.inject_thought(content)
                    response = {
                        "type": "thought_injected",
                        "node_id": node_id,
                        "content": content,
                        "event": universe.latest_event
                    }

            elif action == "reason":
                start_node = message.get("start_node")
                if start_node is not None and int(start_node) in universe.manifold.nodes:
                    res = await universe.trigger_reasoning(int(start_node))
                    response = {
                        "type": "reasoning_result",
                        "path": res["path"],
                        "branches": res["branches"],
                        "confidence": res["confidence"],
                        "total_energy": res["total_energy"],
                        "event": universe.latest_event
                    }

            elif action == "predict":
                start_node = message.get("start_node")
                if start_node is not None and int(start_node) in universe.manifold.nodes:
                    futures = await universe.trigger_prediction(int(start_node))
                    response = {
                        "type": "prediction_result",
                        "branches": futures,
                        "event": universe.latest_event
                    }

            elif action == "timeline_scrub":
                frame = message.get("frame")
                if frame is not None:
                    snapshot = universe.temporal_engine.get_snapshot(int(frame))
                    if snapshot:
                        universe.temporal_engine.current_frame = int(frame)
                        response = {
                            "type": "timeline_frame",
                            "snapshot": snapshot,
                            "event": f"Scrubbed timeline to frame {frame}"
                        }

            elif action == "timeline_play":
                universe.temporal_engine.set_playing(True)
                response = {
                    "type": "playback_change",
                    "playing": True,
                    "event": "Playback resumed"
                }

            elif action == "timeline_pause":
                universe.temporal_engine.set_playing(False)
                response = {
                    "type": "playback_change",
                    "playing": False,
                    "event": "Playback paused"
                }

            # Echo specific response or trigger a broadcast update
            if response:
                await websocket.send_json(response)
                
            # Broadcast the subsequent state update to synchronize all clients
            await broadcast_to_all({
                "type": "state_update",
                "event": universe.latest_event,
                "frame": universe.temporal_engine.current_frame,
                "timeline_size": len(universe.temporal_engine.timeline),
                "playback": {
                    "is_playing": universe.temporal_engine.is_playing,
                    "speed": universe.temporal_engine.playback_speed,
                    "direction": universe.temporal_engine.play_direction
                },
                "nodes": universe.get_serializable_nodes(),
                "edges": universe.get_serializable_edges(),
                "reasoning_path": getattr(universe.manifold, "reasoning_path", [])
            })

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"[INFO] WebSocket client disconnected. Remaining active: {len(active_connections)}")
    except Exception as e:
        print(f"[ERROR] Exception in WebSocket receiver: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)
