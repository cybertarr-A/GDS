import asyncio
import threading
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as core_router
from api.graph_routes import router as graph_router
from api.websocket_routes import router as ws_router
from core.shared import universe

# Default baseline thoughts for initial knowledge synthesis
training_data = [
    "Artificial intelligence learns patterns",
    "Machine learning discovers relationships",
    "Artificial intelligence builds models",
    "Geometry represents knowledge",
    "Knowledge creates reasoning",
    "Reasoning creates predictions",
    "Deep learning improves pattern recognition",
    "Neural networks discover representations",
    "Reasoning evolves through memory"
]

app = FastAPI(
    title="GDS Living Intelligence Universe Backend",
    description="Geometric Data Synthesis real-time AI and simulation backend.",
    version="1.0.0"
)

# Enable CORS for Vite visualizer connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routes
app.include_router(core_router)
app.include_router(graph_router)
app.include_router(ws_router)

main_loop = None


@app.on_event("startup")
def startup_event():
    global main_loop
    main_loop = asyncio.get_event_loop()

    # 1. Initialize universe graph and embeddings
    print("[INFO] Initializing Living Intelligence Universe...")
    universe.initialize(training_data)

    # 2. Run simulation loop inside background daemon thread
    def run_simulation():
        from api.websocket_routes import broadcast_to_all

        def sync_broadcast(payload):
            if main_loop and main_loop.is_running():
                asyncio.run_coroutine_threadsafe(broadcast_to_all(payload), main_loop)

        # Run continuous background drift & thought synthesis
        universe.run_simulation_loop(interval_seconds=4.0, broadcast_callback=sync_broadcast)

    sim_thread = threading.Thread(target=run_simulation, daemon=True)
    sim_thread.start()
    print("[INFO] GDS Simulation Background Loop Started.")


@app.on_event("shutdown")
def shutdown_event():
    print("[INFO] Stopping simulation loops...")
    universe.is_running = False


# ==========================================
# Legacy Offline Executable CLI
# ==========================================

def run_legacy_cli():
    print("\n" + "=" * 50)
    print("GDS V0.6 (CLI Mode)")
    print("Geometric Data Synthesis")
    print("=" * 50)

    universe.initialize(training_data)
    print(f"[INFO] Embedding Dimensions: {universe.embedding_engine.embedding_dimension()}")
    print("[INFO] Knowledge Loaded")

    # Reasoning Walk
    print("\n=== REASONING ===")
    reasoning_result = universe.trigger_reasoning(start_node_id=0, max_depth=5)
    for step in reasoning_result["path"]:
        print(f"\nNode {step['id']}")
        print(step["content"])

    print(f"\nTotal Energy: {reasoning_result['total_energy']:.4f}")
    print(f"Confidence: {reasoning_result['confidence']:.4f}")

    # Memory Recall
    print("\n=== MEMORY RECALL ===")
    query = "Deep learning representation"
    query_vector = universe.embedding_engine.encode(query)[0]
    recalled = universe.memory_engine.recall(query_vector, top_k=3)
    for item in recalled:
        print(f"\nMemory {item['id']} (score={item['score']:.4f})")
        print(item["content"])

    # Prediction
    print("\n=== PREDICTION ===")
    futures = universe.trigger_prediction(start_node_id=0)
    if futures:
        print("\nAlternate predicted paths:")
        for idx, fut in enumerate(futures):
            print(f"Track {idx} (confidence={fut['confidence']:.2f}): {' -> '.join(map(str, fut['path']))}")

    print("\n" + "=" * 50)
    print("GDS OFFLINE EXECUTION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    import sys
    # If run directly with no web requests, execute local synthesis test
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        run_legacy_cli()
    else:
        # Run local server
        import uvicorn
        uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)