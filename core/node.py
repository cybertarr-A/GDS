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

        self.connections=[]


    def add_connection(
        self,
        target_id,
        similarity
    ):

        connection={

            "target":target_id,

            "weight":similarity,

            "usage":0

        }

        self.connections.append(
            connection
        )


    def update_usage(
        self,
        target_id
    ):

        for c in self.connections:

            if c["target"]==target_id:

                c["usage"]+=1

                return