from core.node import GDSNode
from core.vector_utils import VectorUtils


class GDSManifold:

    def __init__(self):

        self.nodes = {}


    def add_node(
        self,
        node_id,
        content,
        vector
    ):

        node = GDSNode(
            node_id,
            content,
            vector
        )

        self.nodes[node_id] = node


    def build_connections(
        self,
        threshold=0.02
    ):

        # Clear previous graph
        for node in self.nodes.values():

            node.connections=[]


        node_ids=list(
            self.nodes.keys()
        )


        for i in range(
            len(node_ids)
        ):

            for j in range(
                i+1,
                len(node_ids)
            ):

                node1=(
                    self.nodes[
                        node_ids[i]
                    ]
                )

                node2=(
                    self.nodes[
                        node_ids[j]
                    ]
                )


                similarity=(

                    VectorUtils.cosine_similarity(

                        node1.vector,
                        node2.vector
                    )
                )


                if similarity>=threshold:

                    node1.add_connection(

                        node2.id,
                        similarity
                    )

                    node2.add_connection(

                        node1.id,
                        similarity
                    )


    def show_graph(self):

        print(
            "\n=== GDS MANIFOLD ==="
        )


        for node in self.nodes.values():

            print("\n")

            print(
                f"Node {node.id}"
            )

            print(
                f"Content: "
                f"{node.content}"
            )

            print(
                "Connections:"
            )


            if len(
                node.connections
            )==0:

                print(
                    "None"
                )

            else:

                for connection in node.connections:

                    print(

                        f"→ Node "

                        f"{connection['target']} "

                        f"(weight="

                        f"{connection['weight']:.4f})"
                    )