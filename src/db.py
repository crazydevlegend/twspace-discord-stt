import os
import pinecone
import pandas as pd
from sentence_transformers import SentenceTransformer

from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")


def connect_to_pinecone(api_key, environment, index_name):
    pinecone.init(api_key=api_key, environment=environment)
    index = pinecone.Index(index_name=index_name)
    return index


def explore_indexes(index_name, index):
    index_description = pinecone.describe_index(index_name)
    index_stats = index.describe_index_stats()
    print(index_description)
    print(index_stats)


def prepare_data():
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
    df = pd.DataFrame(data)
    model = SentenceTransformer("average_word_embeddings_glove.6B.300d")
    df["question_vector"] = df.complains.apply(lambda x: model.encode(str(x)).tolist())
    print(df)


def main():
    index = connect_to_pinecone(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
        index_name=PINECONE_INDEX_NAME,
    )
    explore_indexes(index_name=PINECONE_INDEX_NAME, index=index)
    prepare_data()


if __name__ == "__main__":
    main()
