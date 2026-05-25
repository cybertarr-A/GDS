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
        threshold=0.005,
        min_connections=3
    ):
        from core.neighbor_engine import GDSNeighborEngine
        GDSNeighborEngine.build_nearest_neighbors(
            self.nodes,
            max_connections=min_connections,
            similarity_threshold=threshold
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

                for c in node.connections:

                    print(

                        f"→ Node "

                        f"{c['target']} "

                        f"(weight="

                        f"{c['weight']:.4f})"
                    )