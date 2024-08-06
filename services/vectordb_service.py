import os
from time import sleep
from werkzeug.utils import secure_filename
from typing import Dict, Tuple, IO, List
from app import app
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
import openai
from config import PINECONE_API_KEY, PINECONE_CLOUD, PINECONE_REGION
from config import INDEX_NAME
from pathlib import Path


pinecone = Pinecone(api_key=PINECONE_API_KEY)
spec = ServerlessSpec(cloud=PINECONE_CLOUD, region=PINECONE_REGION)


def save_file(file: Dict[str, Tuple[str, IO, str]]) -> str:
    """
    Save the given file to the server.

    Args:
        file (Dict[str, Tuple[str, IO, str]]): The file to be saved.

    Returns:
        str: The filename of the saved file.
    """

    print('Saving file...')
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    return filename


def split_text(filename: str, username: str, department: str) -> List:
    """
    Splits a text file or PDF into smaller chunks of text.

    Args:
        filename (str): The name of the file to be split.
        username (str): The username of the logged in user.
        department (str): The department of the logged in user.

    Returns:
        list: A list of documents, where each document is a chunk of text.
    """

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    # Assuming that the file is a PDF if it is not a text file
    if Path(filename).suffix == '.txt':
        loader = TextLoader(filepath)
    else:
        loader = PyPDFLoader(filepath)

    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)

    docs = text_splitter.split_documents(data)

    # Add metadata to each document
    for doc in docs:
        doc.metadata = {'username': username, 'department': department}

    return docs


def add_to_vectordb(docs: List[str]) -> PineconeVectorStore:
    """
    Adds documents to a VectorDB index.

    Args:
        docs (List[str]): A list of documents to be added to the index.

    Returns:
        PineconeVectorStore: A PineconeVectorStore object representing the index.

    Raises:
        PineconeException: If there is an error during index creation or document addition.
    """

    existing_indexes = [
        index_info["name"] for index_info in pinecone.list_indexes()
    ]

    # Create the index if it does not exist
    if INDEX_NAME not in existing_indexes:
        pinecone.create_index(
            INDEX_NAME,
            dimension=1536,
            metric='dotproduct',
            spec=spec
        )
        # wait for index to be initialized
        while not pinecone.describe_index(INDEX_NAME).status['ready']:
            sleep(1)

    embeddings = OpenAIEmbeddings()

    vector_store = PineconeVectorStore.from_documents(docs, index_name=INDEX_NAME, embedding=embeddings)
    
    return vector_store


def vectordb_query(input_text: str, username: str, department: str) -> str:
    """
    Queries a VectorDB index with the given input text and returns the processed results.

    Args:
        input_text (str): The input text to query the VectorDB index with.
        username (str): The username of the logged in user.
        department (str): The department of the logged in user.

    Returns:
        str: The processed results as a string.
    """
    # Create an embedding for the input text using OpenAI's text-embedding-ada-002 model
    response = openai.embeddings.create(
        input=input_text,
        model="text-embedding-ada-002"
    )
    query_embedding = response.data[0].embedding

    num_results = 5
    index = pinecone.Index(INDEX_NAME)

    # Create a filter allowing for querying by Username & Department
    metadata_filter = {
        "username": username,
        "department": department
    }

    # Query the VectorDB index with the query embedding and retrieve the results
    results = index.query(vector=query_embedding, top_k=num_results, include_metadata=True, filter=metadata_filter)

    processed_results = ''
    for match in results['matches']:
        processed_results += match['metadata'].get('text', 'No text available') + '\n'

    return processed_results
