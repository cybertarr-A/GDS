import numpy as np
from sklearn.cluster import KMeans


class GDSClusteringEngine:

    @staticmethod
    def cluster_manifold(manifold, num_clusters=3):
        if not manifold.nodes:
            return

        node_ids = list(manifold.nodes.keys())
        vectors = []

        for nid in node_ids:
            node = manifold.nodes[nid]
            vectors.append(node.vector)

        vectors = np.array(vectors)

        # Handle small graph sizes
        n_clusters = min(num_clusters, len(node_ids))
        if n_clusters < 1:
            n_clusters = 1

        if n_clusters > 1:
            try:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                labels = kmeans.fit_predict(vectors)
            except Exception as e:
                print(f"[WARNING] KMeans failed: {e}. Falling back to default clustering.")
                labels = [i % n_clusters for i in range(len(node_ids))]
        else:
            labels = [0] * len(node_ids)

        # Galaxy Centers in 3D Space
        galaxy_centers = {
            0: np.array([0.0, 0.0, 0.0]),
            1: np.array([12.0, 4.0, -8.0]),
            2: np.array([-12.0, -4.0, 8.0]),
            3: np.array([5.0, -10.0, -5.0]),
            4: np.array([-5.0, 10.0, 5.0])
        }

        # Ensure all possible clusters have a center
        for c in range(n_clusters):
            if c not in galaxy_centers:
                galaxy_centers[c] = np.random.uniform(-15, 15, 3)

        # Position nodes in their respective galaxies
        cluster_counts = {}
        for idx, nid in enumerate(node_ids):
            node = manifold.nodes[nid]
            cluster_id = int(labels[idx])
            node.cluster = cluster_id

            if cluster_id not in cluster_counts:
                cluster_counts[cluster_id] = 0
            count = cluster_counts[cluster_id]
            cluster_counts[cluster_id] += 1

            # Circular/Spiral positioning around galaxy center
            center = galaxy_centers[cluster_id]
            angle = (count * 137.5) * (np.pi / 180.0)  # Golden angle
            radius = 1.5 + 0.6 * np.sqrt(count)

            # Orbit coordinates in orbital plane
            dx = radius * np.cos(angle)
            dz = radius * np.sin(angle)
            dy = (np.random.rand() - 0.5) * 0.8  # Slight dispersion in thickness

            # Assign 3D positions
            node.x = float(center[0] + dx)
            node.y = float(center[1] + dy)
            node.z = float(center[2] + dz)

        return n_clusters
