from core.vector_utils import VectorUtils


class GDSEnergyEngine:

    @staticmethod
    def calculate_energy(
        source_vector,
        target_vector,
        weight
    ):

        distance = (
            VectorUtils.euclidean_distance(
                source_vector,
                target_vector
            )
        )

        energy = (
            weight *
            (distance ** 2)
        )

        return energy


    @staticmethod
    def find_lowest_energy_path(
        manifold,
        node_id
    ):

        current_node = (
            manifold.nodes[node_id]
        )

        results = []

        for connection in current_node.connections:

            target_node = (
                manifold.nodes[
                    connection["target"]
                ]
            )

            energy = (
                GDSEnergyEngine.calculate_energy(
                    current_node.vector,
                    target_node.vector,
                    connection["weight"]
                )
            )

            results.append({

                "target":
                target_node.id,

                "content":
                target_node.content,

                "energy":
                energy

            })

        results.sort(
            key=lambda x: x["energy"]
        )

        return results