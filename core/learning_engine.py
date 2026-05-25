class GDSLearningEngine:

    @staticmethod
    def learn(
        text,
        engine,
        manifold,
        memory
    ):

        new_id = len(
            manifold.nodes
        )

        vector = (
            engine.encode(
                text
            )[0]
        )

        manifold.add_node(

            node_id=new_id,

            content=text,

            vector=vector
        )

        memory.store(

            node_id=new_id,

            content=text,

            vector=vector
        )

        manifold.build_connections(
            threshold=0.02
        )


        # -------- Bridge creation --------

        node = manifold.nodes[
            new_id
        ]

        if len(
            node.connections
        ) == 0:

            similarities=[]

            for existing in manifold.nodes.values():

                if existing.id == new_id:

                    continue

                score = 0.05

                similarities.append(

                    (
                        existing.id,
                        score
                    )
                )


            similarities.sort(
                reverse=True,
                key=lambda x:x[1]
            )

            bridge=similarities[0]

            node.add_connection(

                bridge[0],

                bridge[1]
            )

            manifold.nodes[
                bridge[0]
            ].add_connection(

                new_id,

                bridge[1]
            )

        return new_id