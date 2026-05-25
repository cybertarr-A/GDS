class GDSAttentionFieldEngine:
    """
    Advanced cognitive attention and energy field orchestrator.
    Manages active influence zones, dynamic propagation waves, and cognitive heat regions.
    """

    @staticmethod
    def propagate_attention_field(manifold, start_node_id, amount=1.0, visited=None):
        """
        Recursively propagates an active attention signal through connections.
        Decays the amplitude proportionally based on similarity link weights.
        """
        if visited is None:
            visited = set()

        if start_node_id not in manifold.nodes or start_node_id in visited:
            return

        visited.add(start_node_id)
        node = manifold.nodes[start_node_id]
        
        # Boost current node's active attention
        node.attention = min(1.0, getattr(node, "attention", 0.05) + amount)

        # Propagate recursively to neighbors with signal attenuation
        for conn in node.connections:
            neighbor_id = conn["target"]
            weight = conn["weight"]
            
            # Attenuation factor: weight-dependent decay
            attenuation = amount * weight * 0.7
            if attenuation > 0.08:
                GDSAttentionFieldEngine.propagate_attention_field(
                    manifold, 
                    neighbor_id, 
                    amount=attenuation, 
                    visited=visited
                )

    @staticmethod
    def decay_attention_field(manifold, decay_rate=0.15, base_level=0.05):
        """
        Decays active attention states across all manifold nodes down to base levels.
        """
        for node in manifold.nodes.values():
            curr = getattr(node, "attention", 0.05)
            node.attention = max(base_level, curr - decay_rate)

    @staticmethod
    def calculate_heat_regions(manifold, min_attention=0.3):
        """
        Groups nodes that exceed a specified attention threshold,
        calculating high-attention 3D center zones (influence centroids).
        """
        regions = []
        visited = set()

        for node_id, node in manifold.nodes.items():
            if node_id in visited or getattr(node, "attention", 0.05) < min_attention:
                continue

            # Formulate local heat cluster (BFS/DFS traversal of high attention)
            cluster = []
            queue = [node_id]
            visited.add(node_id)

            while queue:
                curr_id = queue.pop(0)
                curr_node = manifold.nodes[curr_id]
                cluster.append(curr_node)

                for conn in curr_node.connections:
                    target_id = conn["target"]
                    target_node = manifold.nodes[target_id]
                    if target_id not in visited and getattr(target_node, "attention", 0.05) >= min_attention:
                        visited.add(target_id)
                        queue.append(target_id)

            # Calculate center coordinate of this high heat density region
            if cluster:
                coords = np = [(n.x, n.y, n.z) for n in cluster]
                xs, ys, zs = zip(*coords)
                center_x = sum(xs) / len(cluster)
                center_y = sum(ys) / len(cluster)
                center_z = sum(zs) / len(cluster)
                
                regions.append({
                    "region_id": len(regions),
                    "center": {"x": center_x, "y": center_y, "z": center_z},
                    "density": len(cluster),
                    "average_attention": sum(getattr(n, "attention", 0.05) for n in cluster) / len(cluster)
                })

        return regions
