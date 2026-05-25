from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from core.shared import universe
from core.path_engine import GDSPathEngine

router = APIRouter()


class InjectionRequest(BaseModel):
    content: str


class ReasoningRequest(BaseModel):
    start_node: int
    max_depth: Optional[int] = 5


class PathRequest(BaseModel):
    start_node: int
    target_node: int


# ==========================================
# Graph & Node Query Endpoints
# ==========================================

@router.get("/graph")
def get_graph():
    # Return full graph structure for visualizer (matches backward compatibility)
    return {
        "nodes": universe.get_serializable_nodes(),
        "edges": universe.get_serializable_edges(),
        "reasoning_path": getattr(universe.manifold, "reasoning_path", [])
    }


@router.get("/api/graph/search")
def search_graph(q: str = Query(..., description="Query string to search in nodes")):
    # Filter nodes by text content
    results = []
    query_lower = q.lower()
    
    # Optional vector search if matching query is processed
    try:
        query_vector = universe.embedding_engine.encode(q)[0]
        recalled = universe.memory_engine.recall(query_vector, top_k=5, similarity_threshold=0.01)
        recalled_ids = {item["id"] for item in recalled}
    except Exception:
        recalled_ids = set()

    for node in universe.manifold.nodes.values():
        score = 0.0
        is_match = False
        
        if query_lower in node.content.lower() or str(node.id) == q:
            is_match = True
            score = 1.0
        elif node.id in recalled_ids:
            is_match = True
            score = 0.5

        if is_match:
            # Boost attention of matches visually
            node.attention = min(1.0, getattr(node, "attention", 0.05) + 0.3)
            results.append({
                "id": node.id,
                "content": node.content,
                "score": score,
                "energy": getattr(node, "energy", 0.5),
                "importance": getattr(node, "importance", 0.5),
                "cluster": getattr(node, "cluster", 0)
            })

    # Record event in timeline
    if results:
        universe.latest_event = f"Searched graph for: '{q}' ({len(results)} matches)"
        universe.temporal_engine.record_snapshot(universe.manifold, universe.latest_event)

    return sorted(results, key=lambda x: x["score"], reverse=True)


@router.post("/api/graph/inject")
def inject_thought(req: InjectionRequest):
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Content cannot be empty")
        
    node_id = universe.inject_thought(req.content)
    return {
        "status": "success",
        "injected_node_id": node_id,
        "content": req.content,
        "event": universe.latest_event
    }


@router.post("/api/graph/reason")
def trigger_reasoning(req: ReasoningRequest):
    if req.start_node not in universe.manifold.nodes:
        raise HTTPException(status_code=404, detail="Start node not found")
        
    result = universe.trigger_reasoning(req.start_node, req.max_depth)
    return {
        "status": "success",
        "path": result["path"],
        "branches": result["branches"],
        "total_energy": result["total_energy"],
        "confidence": result["confidence"],
        "event": universe.latest_event
    }


@router.post("/api/graph/predict")
def trigger_prediction(req: ReasoningRequest):
    if req.start_node not in universe.manifold.nodes:
        raise HTTPException(status_code=404, detail="Start node not found")
        
    futures = universe.trigger_prediction(req.start_node)
    return {
        "status": "success",
        "branches": futures,
        "event": universe.latest_event
    }


@router.post("/api/graph/find-path")
def find_goal_path(req: PathRequest):
    if req.start_node not in universe.manifold.nodes or req.target_node not in universe.manifold.nodes:
        raise HTTPException(status_code=404, detail="Start or target node not found")
        
    path = GDSPathEngine.find_path(universe.manifold, req.start_node, req.target_node)
    if not path:
        return {"status": "no_path", "path": []}
        
    universe.manifold.reasoning_path = path
    universe.latest_event = f"Path discovered from Node {req.start_node} to Node {req.target_node}"
    universe.temporal_engine.record_snapshot(universe.manifold, universe.latest_event)
    
    return {
        "status": "success",
        "path": path,
        "event": universe.latest_event
    }
