from core.energy_engine import GDSEnergyEngine
from core.vector_utils import VectorUtils


class GDSReasoningEngine:

    @staticmethod
    def traverse(manifold, start_node, max_depth=5):
        if start_node not in manifold.nodes:
            return {"path": [], "branches": [], "total_energy": 0.0, "confidence": 0.0}

        visited = set()
        reasoning_path = []
        branches = []
        current = start_node
        total_energy = 0.0

        for depth in range(max_depth):
            if current in visited:
                break

            visited.add(current)
            node = manifold.nodes[current]
            reasoning_path.append({
                "id": node.id,
                "content": node.content
            })

            # Calculate energy paths to all connections
            paths = GDSEnergyEngine.find_lowest_energy_path(manifold, current)
            if not paths:
                break

            # Best next node
            best = paths[0]
            
            # Check for Branching: if second best is within 15% of best energy
            if len(paths) > 1:
                second = paths[1]
                # Avoid dividing by zero
                denom = best["energy"] if best["energy"] != 0 else 0.001
                percentage_diff = (second["energy"] - best["energy"]) / denom
                
                if percentage_diff <= 0.25 and second["target"] not in visited:
                    # Spawn a branch!
                    branch_visited = set(visited)
                    branch_path = []
                    branch_curr = second["target"]
                    branch_energy = second["energy"]
                    
                    for _ in range(max_depth - depth - 1):
                        if branch_curr in branch_visited or branch_curr not in manifold.nodes:
                            break
                        branch_visited.add(branch_curr)
                        branch_path.append({
                            "id": branch_curr,
                            "content": manifold.nodes[branch_curr].content
                        })
                        
                        b_paths = GDSEnergyEngine.find_lowest_energy_path(manifold, branch_curr)
                        if not b_paths:
                            break
                        branch_curr = b_paths[0]["target"]
                        branch_energy += b_paths[0]["energy"]
                    
                    if branch_path:
                        # Confidence of branch relative to connection weight
                        sim = VectorUtils.cosine_similarity(node.vector, manifold.nodes[second["target"]].vector)
                        branches.append({
                            "split_node": current,
                            "path": branch_path,
                            "energy": float(branch_energy),
                            "confidence": float(sim)
                        })

            total_energy += best["energy"]
            current = best["target"]

        # Calculate main confidence score
        confidence = 1.0
        if len(reasoning_path) > 1:
            similarities = []
            for i in range(len(reasoning_path) - 1):
                n1 = manifold.nodes[reasoning_path[i]["id"]]
                n2 = manifold.nodes[reasoning_path[i+1]["id"]]
                sim = VectorUtils.cosine_similarity(n1.vector, n2.vector)
                similarities.append(sim)
            confidence = float(sum(similarities) / len(similarities))

        return {
            "path": reasoning_path,
            "branches": branches,
            "total_energy": float(total_energy),
            "confidence": confidence
        }