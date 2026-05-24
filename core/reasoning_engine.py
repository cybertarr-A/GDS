from core.energy_engine import GDSEnergyEngine


class GDSReasoningEngine:

    @staticmethod
    def traverse(
        manifold,
        start_node,
        max_depth=3
    ):

        visited = set()

        reasoning_path = []

        current = start_node

        total_energy = 0


        for _ in range(max_depth):

            if current in visited:
                break

            visited.add(current)

            node = manifold.nodes[current]

            reasoning_path.append({

                "id": node.id,
                "content": node.content
            })

            paths = (
                GDSEnergyEngine
                .find_lowest_energy_path(
                    manifold,
                    current
                )
            )

            if len(paths) == 0:
                break

            best = paths[0]

            total_energy += best["energy"]

            current = best["target"]

        return {

            "path": reasoning_path,
            "total_energy": total_energy
        }