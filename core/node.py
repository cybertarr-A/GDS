class GDSNode:

    def __init__(
        self,
        node_id,
        content,
        vector
    ):

        self.id = node_id

        self.content = content

        self.vector = vector

        self.connections = []


    def add_connection(
        self,
        target_id,
        similarity
    ):

        self.connections.append({

            "target": target_id,
            "weight": similarity

        })


    def __repr__(self):

        return (
            f"Node("
            f"id={self.id}, "
            f"connections={len(self.connections)})"
        )