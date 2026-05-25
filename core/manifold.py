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
        threshold=0.02,
        min_connections=2
    ):

        # Clear previous graph
        for node in self.nodes.values():

            node.connections=[]


        node_ids=list(
            self.nodes.keys()
        )


        similarities={}


        # -----------------------------
        # Compute all similarities
        # -----------------------------

        for i in range(len(node_ids)):

            for j in range(
                i+1,
                len(node_ids)
            ):

                node1=self.nodes[
                    node_ids[i]
                ]

                node2=self.nodes[
                    node_ids[j]
                ]

                score=(

                    VectorUtils.cosine_similarity(

                        node1.vector,
                        node2.vector
                    )
                )


                similarities[

                    (
                        node1.id,
                        node2.id
                    )

                ]=score


                if score>=threshold:

                    node1.add_connection(

                        node2.id,
                        score
                    )

                    node2.add_connection(

                        node1.id,
                        score
                    )


        # -----------------------------
        # Force bridge creation
        # -----------------------------

        for node in self.nodes.values():

            if len(
                node.connections
            )<min_connections:

                candidates=[]

                for other in self.nodes.values():

                    if other.id==node.id:

                        continue


                    key=tuple(

                        sorted(

                            (
                                node.id,
                                other.id
                            )
                        )
                    )


                    score=similarities.get(
                        key,
                        0
                    )


                    candidates.append(

                        (
                            other.id,
                            score
                        )
                    )


                candidates.sort(

                    key=lambda x:x[1],

                    reverse=True
                )


                needed=(

                    min_connections
                    -
                    len(node.connections)
                )


                for target,score in candidates[:needed]:

                    already=False


                    for c in node.connections:

                        if c["target"]==target:

                            already=True
                            break


                    if not already:

                        node.add_connection(

                            target,
                            score
                        )

                        self.nodes[
                            target
                        ].add_connection(

                            node.id,
                            score
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