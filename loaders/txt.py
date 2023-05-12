import tempfile
import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document



def process_txt(vector_store, file):
    documents = []
    file_sha = ""
    with tempfile.NamedTemporaryFile(delete=True, suffix=".txt") as tmp_file:
        tmp_file.write(file.getvalue())
        tmp_file.flush()

        loader = TextLoader(tmp_file.name)
        documents = loader.load()
        file_sha1 = compute_sha1_from_file(tmp_file.name)
    
    ## Load chunk size and overlap from sidebar
    chunk_size = st.session_state['chunk_size']
    chunk_overlap = st.session_state['chunk_overlap']

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    docs = text_splitter.split_documents(documents)

    # Add the document sha1 as metadata to each document
    docs_with_metadata = [Document(page_content=doc.page_content, metadata={"file_sha1": file_sha1}) for doc in docs]
    

    # We're using the default `documents` table here. You can modify this by passing in a `table_name` argument to the `from_documents` method.
    vector_store.add_documents(docs_with_metadata)
    return 