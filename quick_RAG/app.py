import os

import streamlit as st
from dotenv import load_dotenv
from langchain import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader


def main():
    from dotenv import dotenv_values, load_dotenv 
    load_dotenv()

    token = os.getenv("HF_TOKEN")

    st.set_page_config(page_title='Streamlit App')
    st.header("Ask a question")

    pdf = st.file_uploader("Upload a PDF file", type=["pdf"])

    # Create knowledge base
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )

        chunks = text_splitter.split_text(text)

        embeddings = HuggingFaceEmbeddings()
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        user_question = st.text_input("Ask a question:")

        # Question answering logic
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            llm = HuggingFaceHub(repo_id="declare-lab/flan-alpaca-large", model_kwargs={"temperature":0.0, "max_length":1024}, huggingfacehub_api_token=token)
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=user_question)

            st.write(response)

if __name__ == '__main__':
    main()