<img width="1536" height="1024" alt="ChatGPT Image May 25, 2026, 03_48_40 PM" src="https://github.com/user-attachments/assets/446344a5-084f-4214-b200-def2eb614f61" />

# 🌌 Geometric Data Synthesis (GDS) — Living Intelligence Universe

```text
      .      *                  .               .       .
  .         .           .         *      .              .
        .        .    _ ___ ___ _ _ ___ ___ _ _    .
  *        .         | | . | . | | | -_|  _|_'_|      .      *
     .        .      |_|_  |___|\_/|___|_| |_,_|    .
   .       *           |___|      UNIVERSE v1.0.0
      .            .              .         .               .
```

Welcome to the **Geometric Data Synthesis (GDS)** repository, evolved into a **Living Intelligence Universe**. This platform models knowledge as a multi-dimensional spatial manifold in 3D space, mapping concepts to distinct semantic galaxies, propagating real-time attention fields, predicting alternate branching futures, and synchronizing state over bi-directional WebSocket streams.

---

## 🔮 Core GDS Concepts

1. **Knowledge as Manifolds**: Information exists as high-dimensional coordinates. Proximity indicates vector alignment and semantic similarity.
2. **Reasoning as Traversals**: Moving along paths of lowest energy between knowledge structures.
3. **Memory as Constellations**: Episodic thoughts are grouped into K-Means coordinate galaxies using Golden Angle orbital projections.
4. **Prediction as Evolution**: Alternate future pathways are simulated using transition weights and vector proximity.
5. **Attention as Fields**: Triggered thoughts radiate concentric waves of interest that decay over time.

---

## 🚀 Key Features

* **Three.js Cosmic Ambiance**: Custom starfields with additive blending, space nebulae dust, and soft glow HSL energies.
* **Bi-directional WebSockets**: Low-latency stream synchronizing backend autonomous loops and frontend canvas views.
* **Temporal Scrubber**: Full history snapshots supporting Pause, Resume, Reverse playback, Time-Warp speed modulations ($0.5\times$ to $5.0\times$), and scrubber scrubber frame navigation.
* **Multi-thought Traversals**: Concurrent thought particles splitting along branching pathways based on confidence metrics.
* **Autonomous Evolution**: An asynchronous thread continuously synthesizes emergent concepts, pairs newly aligned nodes, and prunes decayed links.
* **Semantic Search & Filters**: Zoom-to-node camera transitions with smooth LERPs, filter sliders, and text search overlays.

---

## 📂 Project Directory Structure

```text
gds/
├── app.py                      # FastAPI Web Entrypoint & CLI Fallback Run
├── api/                        # HTTP & WebSocket Router Layers
│   ├── routes.py               # Temporal timeline & speed warp controls
│   ├── graph_routes.py         # Graph CRUD, searches, and traversals
│   └── websocket_routes.py     # Low-latency bi-directional sync pool
│
├── core/                       # Cognitive Processing Engines
│   ├── shared.py               # Global orchestrator singleton provider
│   ├── universe_engine.py      # Simulation loops & master coordination
│   ├── embedding_engine.py     # TF-IDF Vector mappings
│   ├── memory_engine.py        # Vector cosine similarity recalls
│   ├── reasoning_engine.py     # Multi-path traversals & confidence scores
│   ├── prediction_engine.py    # Probabilistic alternate future projections
│   ├── temporal_engine.py      # Playback state frames & snapshots
│   ├── graph_engine.py         # Autonomous synthesis & decayed edge pruning
│   ├── clustering_engine.py    # K-Means spatial galaxy positioning
│   ├── attention_engine.py     # Attention wave projections & decays
│   ├── node.py                 # Graph node objects
│   └── vector_utils.py         # Cosine similarities & distance calculations
│
├── data/                       # Local State Databases
│   ├── graph.json              # Current manifest of nodes & edges
│   ├── timeline.json           # Historical frames database
│   └── memory.json             # Serialized vector memory indexes
│
└── frontend/                   # Three.js Web Dashboard (Vite + JS)
    ├── index.html              # Futuristic Glassmorphic HTML template
    ├── package.json            # WebGL dependencies (axios, postprocessing, three, vite)
    ├── src/
    │   ├── main.js             # App setup, lights, LERP zooms & render loops
    │   ├── style.css           # Premium glassmorphic space themes & animations
    │   ├── graph_renderer.js   # Glowing spheres, beams, and ring wave objects
    │   ├── universe_engine.js  # Additive starfield and cosmic clouds
    │   ├── temporal_controls.js# Timeline scrub handles
    │   └── websocket_client.js # Resilient WS connection state manager
    └── public/
        └── graph.json          # Baseline fallback graph
```

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**

### 1. Backend Setup
1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependency requirements:
   ```bash
   pip install -r requirements.txt
   # Install API dependencies:
   pip install fastapi uvicorn pydantic websockets scikit-learn numpy
   ```

### 2. Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install Node modules:
   ```bash
   npm install
   ```

---

## 🚦 Execution

You need to run both the FastAPI Backend and the Vite Frontend in separate terminal windows:

### 1. Launch FastAPI Core Server
Starts the API endpoints and spins up the background drift/thought simulation loop:
```bash
# From workspace root
venv/bin/python app.py
```
*Server runs on: **`http://127.0.0.1:8000/`***

### 2. Launch Vite Visualizer
```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
*Visualizer runs on: **`http://127.0.0.1:5173/`***

---

## 🔌 API Endpoints Summary

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Retrieve overall GDS Status, current frame, & speed configs. |
| `/graph` | `GET` | Get current full graph JSON for backward compatibility. |
| `/api/graph/search` | `GET` | Query nodes semantically, boosting matching attentions. |
| `/api/graph/inject` | `POST` | Manually insert a thought, spawning an attention wave. |
| `/api/graph/reason` | `POST` | Trigger traversals & branching paths starting from a node. |
| `/api/graph/predict` | `POST` | Generate alternate branching predicted futures. |
| `/timeline` | `GET` | Extract full historical list of frame snapshots. |
| `/timeline/{frame}` | `GET` | Jump/Scrub timeline playhead directly to specific frame. |
| `/timeline/play` | `POST` | Resume the cosmic drift simulation. |
| `/timeline/pause` | `POST` | Pause the simulation loop. |
| `/timeline/reverse` | `POST` | Toggle temporal direction (Forward ↔ Reverse). |
| `/timeline/speed` | `POST` | Warps simulation speed factors (`0.5x` - `5.0x`). |

---

## 🛰️ WebSocket Sync Packet Protocol (`/api/ws`)

When connected, clients receive real-time JSON packets:

```json
{
  "type": "state_update",
  "event": "Synthesized Node 12: 'Deep learning leads to emergent reasoning'",
  "frame": 24,
  "timeline_size": 25,
  "playback": {
    "is_playing": true,
    "speed": 1.0,
    "direction": 1
  },
  "nodes": [
    { "id": 0, "content": "AI learns patterns", "energy": 0.8, "attention": 0.45, "cluster": 0, "x": 0.45, "y": -0.22, "z": 1.2 }
  ],
  "edges": [
    { "source": 0, "target": 1, "weight": 0.85 }
  ],
  "reasoning_path": [0, 1, 3]
}
```
Client actions sent via WebSocket:
- `{"action": "ping"}`
- `{"action": "inject", "content": "..."}`
- `{"action": "reason", "start_node": 0}`
- `{"action": "predict", "start_node": 0}`
- `{"action": "timeline_scrub", "frame": 12}`
- `{"action": "timeline_play"}`
- `{"action": "timeline_pause"}`
