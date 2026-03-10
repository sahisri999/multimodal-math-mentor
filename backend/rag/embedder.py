from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-large")


def embed_text(text):

    embedding = model.encode(text)

    return embedding.tolist()