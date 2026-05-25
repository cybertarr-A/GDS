class GDSPathEngine:

    @staticmethod
    def find_path(
        manifold,
        start_node,
        target_node
    ):

        visited = set()

        queue = [

            (
                start_node,
                [start_node]
            )
        ]

        while queue:

            current, path = queue.pop(0)

            if current == target_node:

                return path

            if current in visited:

                continue

            visited.add(current)

            node = manifold.nodes[current]

            for connection in node.connections:

                next_node = (
                    connection["target"]
                )

                if next_node not in visited:

                    queue.append(

                        (
                            next_node,
                            path + [next_node]
                        )
                    )

        return None