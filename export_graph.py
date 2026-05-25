import json


class GDSExporter:

    @staticmethod
    def export(manifold):

        nodes=[]
        edges=[]


        for node in manifold.nodes.values():

            nodes.append({

                "id":node.id,

                "content":node.content

            })


            for connection in node.connections:

                edges.append({

                    "source":node.id,

                    "target":connection["target"],

                    "weight":connection["weight"]

                })


        data={

            "nodes":nodes,

            "edges":edges

        }


        with open(

            "graph.json",

            "w"

        ) as f:

            json.dump(

                data,
                f,
                indent=4
            )