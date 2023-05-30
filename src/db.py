import itertools
import os
import pinecone
import pandas as pd
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

model = SentenceTransformer("average_word_embeddings_glove.6B.300d")
data = {
    "ticketno": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010],
    "complains": [
        "Broken navigation button on the website",
        "Incorrect pricing displayed for a product",
        "Unable to reset password",
        "App crashes on the latest iOS update",
        "Payment processing error during checkout",
        "Wrong product delivered",
        "Delayed response from customer support",
        "Excessive delivery time for an order",
        "Difficulty in finding a specific product",
        "Error in applying a discount coupon",
    ],
}


def connect_to_pinecone(api_key, environment, index_name):
    pinecone.init(api_key=api_key, environment=environment)
    index = pinecone.Index(index_name=index_name)
    return index


def explore_indexes(index_name, index):
    index_description = pinecone.describe_index(index_name)
    index_stats = index.describe_index_stats()
    print(index_description)
    print(index_stats)


def prepare_data(data):
    df = pd.DataFrame(data)
    df["question_vector"] = df.complains.apply(lambda x: model.encode(str(x)).tolist())
    return df


def chunks(iterable, batch_size=100):
    it = iter(iterable)
    chunk = tuple(itertools.islice(it, batch_size))
    while chunk:
        yield chunk
        chunk = tuple(itertools.islice(it, batch_size))


def upsert_vectors(index, data):
    for batch in chunks(
        [(str(t), v) for t, v in zip(data.ticketno, data.question_vector)]
    ):
        index.upsert(vectors=batch)


def fetch_vectors(index, IDs):
    print(index.fetch(IDs))


def semantic_search(index, question, mainDF):
    # Query the question
    query_questions = [question]
    query_vectors = [
        model.encode(str(question)).tolist() for question in query_questions
    ]
    query_results = index.query(queries=query_vectors, top_k=5, include_values=False)

    # Extract matches and scores from the results
    matches = []
    scores = []
    for match in query_results["results"][0]["matches"]:
        matches.append(match["id"])
        scores.append(match["score"])

    # Create DataFrame with only matches and scores
    matches_df = pd.DataFrame({"id": matches, "score": scores})

    # Match the result dataframe to main dataframe
    print(mainDF)
    mainDF["ticketno"] = mainDF["ticketno"].astype(str)
    matches_df.merge(mainDF, left_on="id", right_on="ticketno")

    return matches_df


def main():
    index = connect_to_pinecone(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
        index_name=PINECONE_INDEX_NAME,
    )
    explore_indexes(index_name=PINECONE_INDEX_NAME, index=index)

    # preprocess data
    df = prepare_data(data=data)
    # C - upsert data
    # upsert_vectors(index=index, data=df)
    # R - fetch vectors
    # fetch_vectors(index=index, IDs=["1010", "1009"])
    # semantic search
    result = semantic_search(index=index, question="navigation button", mainDF=df)
    print(result)


if __name__ == "__main__":
    main()
