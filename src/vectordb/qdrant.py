from __future__ import annotations

import qdrant_client
from langchain.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient

from src.llm import openai
from src.utils import common

URL = common.config()["vectordb"]["url"]
# if URL == "localhost":
#     URL = common.config()["vectordb"]["localhost_ip"]
PORT = common.config()["vectordb"]["port"]

CLIENT: QdrantClient = None


def get_client(connector: str = "langchain", collection: str = None):
    """
    Get the Qdrant client instance.

    Args:
        connector (str, optional): The connector to use. Defaults to "langchain".
        collection (str, optional): The name of the collection. Required if connector is "langchain".

    Returns:
        QdrantClient: The Qdrant client instance.

    Raises:
        ValueError: If the collection name is not provided when using the "langchain" connector.
    """
    global CLIENT
    if CLIENT is None:
        if connector == "langchain":
            if collection is None:
                raise ValueError("Collection name must be provided.")
            return Qdrant(
                client=QdrantClient(URL, port=PORT),
                collection_name=collection,
                embeddings=openai.get_embeddings(),
            )
        else:
            CLIENT = QdrantClient(URL, port=PORT)
    return CLIENT


def create_collection(collection: str):
    """
    Create a collection.

    Args:
        collection (str): The name of the collection.
    """
    get_client().create_collection(collection_name=collection)


def insert_documents(collection: str, documents: list[str]):
    """
    Insert documents into the collection.

    Args:
        collection (str): The name of the collection.
        documents (list): The documents to insert.
    """
    try:
        get_client(collection=collection).add_documents(documents=documents)
    except qdrant_client.http.exceptions.ResponseHandlingException as e:
        raise ValueError("Check your client URL and port.") from e


def query_collection(collection: str, query: str):
    """
    Query the collection.

    Args:
        collection (str): The name of the collection.
        query (str): The query.

    Returns:
        dict: The results of the query.
    """
    return get_client(collection=collection).query(
        query=query,
        collection_name=collection,
    )
