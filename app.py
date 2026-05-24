from core.embedding_engine import GDSEmbeddingEngine
from core.manifold import GDSManifold
from core.reasoning_engine import GDSReasoningEngine
from core.memory_engine import GDSMemoryEngine
from core.prediction_engine import GDSPredictionEngine
from core.learning_engine import GDSLearningEngine
from core.temporal_engine import GDSTemporalEngine


training_data = [

    "Artificial intelligence learns patterns",
    "Machine learning discovers relationships",
    "Artificial intelligence builds models",
    "Geometry represents knowledge",
    "Knowledge creates reasoning",
    "Reasoning creates predictions"

]


def main():

    print("\n" + "=" * 50)
    print("GDS V0.3")
    print("Geometric Data Synthesis")
    print("=" * 50)

    # ===================================
    # Initialize Engines
    # ===================================

    engine = GDSEmbeddingEngine()

    manifold = GDSManifold()

    memory = GDSMemoryEngine()

    predictor = GDSPredictionEngine()

    temporal = GDSTemporalEngine()


    # ===================================
    # Train Embedding Model
    # ===================================

    print("\n[INFO] Training engine...")

    engine.fit(
        training_data
    )

    print(
        f"[INFO] Embedding dimensions: "
        f"{engine.embedding_dimension()}"
    )


    # ===================================
    # Create Initial Knowledge
    # ===================================

    print(
        "\n[INFO] Building nodes..."
    )


    for i, text in enumerate(
        training_data
    ):

        vector = (
            engine.encode(
                text
            )[0]
        )

        manifold.add_node(
            node_id=i,
            content=text,
            vector=vector
        )

        memory.store(
            node_id=i,
            content=text,
            vector=vector
        )

        temporal.record_event(
            i,
            text
        )


    manifold.build_connections(
        threshold=0.02
    )

    print(
        "[INFO] Knowledge loaded"
    )


    # ===================================
    # Dynamic Learning
    # ===================================

    print(
        "\n=== DYNAMIC LEARNING ==="
    )


    new_knowledge = [

        "Deep learning improves pattern recognition",

        "Neural networks discover representations",

        "Reasoning evolves through memory"

    ]


    for knowledge in new_knowledge:

        node_id = (

            GDSLearningEngine.learn(

                text=knowledge,

                engine=engine,

                manifold=manifold,

                memory=memory
            )
        )

        temporal.record_event(
            node_id,
            knowledge
        )

        print(
            f"Added Node: "
            f"{node_id}"
        )


    # ===================================
    # Show Graph
    # ===================================

    manifold.show_graph()


    # ===================================
    # Reasoning
    # ===================================

    print(
        "\n=== REASONING ==="
    )


    result = (

        GDSReasoningEngine.traverse(

            manifold=manifold,

            start_node=0,

            max_depth=5
        )
    )


    for step in result["path"]:

        print()

        print(
            f"Node: "
            f"{step['id']}"
        )

        print(
            step["content"]
        )


    print(
        f"\nTotal Energy: "
        f"{result['total_energy']:.4f}"
    )


    # ===================================
    # Learn Traversal
    # ===================================

    predictor.learn_path(
        result["path"]
    )


    # ===================================
    # Memory Recall
    # ===================================

    print(
        "\n=== MEMORY RECALL ==="
    )


    query = "Deep learning"

    query_vector = (

        engine.encode(
            query
        )[0]
    )


    recalled = (

        memory.recall(

            query_vector,

            top_k=3
        )
    )


    if len(recalled) == 0:

        print(
            "No memories found"
        )

    else:

        for item in recalled:

            print()

            print(
                f"Memory ID: "
                f"{item['id']}"
            )

            print(
                item["content"]
            )

            print(
                f"Score: "
                f"{item['score']:.4f}"
            )


    # ===================================
    # Temporal History
    # ===================================

    print(
        "\n=== TEMPORAL HISTORY ==="
    )


    recent = (

        temporal.get_recent_events()
    )


    for event in recent:

        print()

        print(
            f"Node: "
            f"{event['node_id']}"
        )

        print(
            event["content"]
        )


    # ===================================
    # Prediction
    # ===================================

    print(
        "\n=== PREDICTION ==="
    )


    prediction = (

        predictor.predict_next(
            current_node=0
        )
    )


    if prediction is not None:

        predicted = (

            manifold.nodes[
                prediction
            ]
        )

        print()

        print(
            "Predicted Future State:"
        )

        print(
            predicted.content
        )

    else:

        print(
            "No prediction available"
        )


    print("\n" + "=" * 50)
    print("GDS EXECUTION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()