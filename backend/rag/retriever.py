from backend.rag.embedder import embed_text
from backend.rag.pinecone_client import get_index
from sentence_transformers import util


def expand_query(query: str):
    """
    Expand query to improve retrieval for math concepts.
    """
    expansions = [
        query,
        f"{query} mathematics explanation",
        f"{query} formula definition",
        f"{query} equation derivation"
    ]

    return expansions


def rerank(query: str, contexts: list):
    """
    Re-rank retrieved contexts using cosine similarity.
    """

    query_embedding = embed_text(query)

    scores = []

    for ctx in contexts:
        ctx_embedding = embed_text(ctx)
        score = util.cos_sim(query_embedding, ctx_embedding)
        scores.append((ctx, score.item()))

    # sort by similarity
    scores.sort(key=lambda x: x[1], reverse=True)

    return [s[0] for s in scores]


def retrieve_context(query: str, top_k: int = 8):
    """
    Retrieve relevant context from Pinecone using
    query expansion + reranking.
    """

    index = get_index()

    expanded_queries = expand_query(query)

    all_contexts = []

    for q in expanded_queries:

        embedding = embed_text(q)

        results = index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )

        for match in results["matches"]:
            text = match["metadata"]["text"]
            all_contexts.append(text)

    # remove duplicates
    unique_contexts = list(set(all_contexts))

    # rerank contexts
    ranked_contexts = rerank(query, unique_contexts)

    return ranked_contexts[:top_k]