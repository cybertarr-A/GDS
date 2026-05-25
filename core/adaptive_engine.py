class GDSAdaptiveEngine:

    @staticmethod
    def strengthen_connections(
        manifold,
        reasoning_path,
        learning_rate=0.10
    ):

        for i in range(
            len(reasoning_path)-1
        ):

            current = (
                reasoning_path[i]["id"]
            )

            nxt = (
                reasoning_path[i+1]["id"]
            )


            node = (
                manifold.nodes[
                    current
                ]
            )


            for connection in node.connections:

                if connection["target"] == nxt:

                    connection["usage"] += 1


                    connection["weight"] *= (

                        1 + learning_rate
                    )


    @staticmethod
    def decay_connections(
        manifold,
        decay_rate=0.02
    ):

        for node in manifold.nodes.values():

            # FIX:
            for connection in node.connections:

                if connection["usage"] == 0:

                    connection["weight"] *= (

                        1-decay_rate
                    )


                # reset usage for next cycle
                connection["usage"] = 0