from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import SentenceSplitter

from pydantic import BaseModel, Field

import fitz

from PIL import Image
import matplotlib.pyplot as plt

import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

import dotenv
import os

from openai import OpenAI

from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import Any

dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def chunker(chunk_size: int, overlap: int, documents: Any) -> tuple[list[str], list[int]]:
    text_parser = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
    )

    text_chunks = []
    doc_idxs = []
    for doc_idx, doc in enumerate(documents):
        cur_text_chunks = text_parser.split_text(doc.text)
        text_chunks.extend(cur_text_chunks)
        doc_idxs.extend([doc_idx] * len(cur_text_chunks))

    return text_chunks, doc_idxs


def load_template(template_filepath: str, arguments: dict[str, Any]) -> str:
    env = Environment(
        loader=FileSystemLoader(searchpath='./'),
        autoescape=select_autoescape()
    )
    template = env.get_template(template_filepath)
    return template.render(**arguments)


class DocumentDB:
    def __init__(self, name: str, model_name: str = "text-embedding-3-small", path: str = "./"):
        self.model_name = model_name
        self.client = chromadb.PersistentClient(path=path)
        self.embedding_function = OpenAIEmbeddingFunction(api_key=OPENAI_API_KEY, model_name=model_name)
        self.chat_db = self.client.get_or_create_collection(name=name, embedding_function=self.embedding_function, metadata={"hnsw:space": "cosine"})
        self.id_counter = 0


    def add_chunks_to_db(self, chunks: list[str], doc_idxs: list[int], metadata: dict = {}):
        """Add text chunks to the database.

        Args:
            chunks (list[str]): List of text chunks.
            doc_idxs (list[int]): List of corresponding document indices.
        """
        self.chat_db.add(
            documents=chunks,
            metadatas=[{"doc_idx": idx} for idx in doc_idxs],
            ids=[f"chunk_{self.id_counter + i}" for i in range(len(chunks))]
        )
        self.id_counter += len(chunks)


    def save_db(self):
        self.chat_db.persist()


    def get_all_entries(self) -> dict:
        """Grab all of the entries in the database.

        Returns:
            dict: All entries in the database.
        """
        return self.chat_db.get()
    

    def clear_db(self, reinitialize: bool = True):
        """Clear the database of all entries, and reinitialize it.

        Args:
            reinitialize (bool, optional): _description_. Defaults to True.
        """
        self.client.delete_collection(self.chat_db.name)
        # re-initialize the database
        if reinitialize:
            self.__init__(self.chat_db.name, self.model_name)


    def query_db(self, query_text: str, n_results: int = 2) -> dict:
        """Given some query text, return the n_results most similar entries in the database.

        Args:
            query_text (str): The text to query the database with.
            n_results (int): The number of results to return.

        Returns:
            dict: The most similar entries in the database.
        """
        return self.chat_db.query(query_texts=[query_text], n_results=n_results)


def combine_context(documents: list[str], scores: list[float]) -> str:
    string = ""
    for document, score in zip(documents, scores):
        string += f"{document}\nCosine distance: {score:.2f}\n{'-'*10}\n"
    return string


def rag_query(query: str, n_context, doc_db: chromadb.Collection, return_context=False):

    client = OpenAI()

    query_results = doc_db.query_db(query, n_results=n_context)
    context_list = query_results["documents"][0]
    combined_context = combine_context(context_list, query_results["distances"][0])
    if not combined_context:
        combined_context = "No relevant chat history found."


    system_prompt = load_template(
        template_filepath="prompts/rag_system_prompt.jinja",
        arguments={}
    )

    user_prompt = (
        f"Query: {query}\n\n"
        f"Context: {combined_context}"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        stream=False,
        temperature=0.0
    )
    
    if return_context:
        return response.choices[0].message.content, context_list
    else:
        return response.choices[0].message.content
