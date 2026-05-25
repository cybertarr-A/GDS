from fastapi import FastAPI
import json
from pathlib import Path

app = FastAPI()


@app.get("/")
def root():

    return {
        "status": "running"
    }


@app.get("/graph")
def graph():

    graph_file = Path("../gds/graph.json")

    if not graph_file.exists():

        return {
            "error":"graph.json not found"
        }

    with open(
        graph_file,
        "r"
    ) as f:

        return json.load(f)