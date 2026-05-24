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

        return new_id