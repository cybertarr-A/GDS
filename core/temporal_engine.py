import time


class GDSTemporalEngine:

    def __init__(self):

        self.timeline=[]


    def record_event(
        self,
        node_id,
        content
    ):

        event={

            "timestamp":time.time(),

            "node_id":node_id,

            "content":content

        }

        self.timeline.append(
            event
        )


    def get_recent_events(
        self,
        limit=5
    ):

        return sorted(

            self.timeline,

            key=lambda x:
            x["timestamp"],

            reverse=True

        )[:limit]