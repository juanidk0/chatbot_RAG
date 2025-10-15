# Run this file for initialize the company_db

import os
import numpy as np
import glob
from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma


load_dotenv()
# Read documents using LangChain loaders
# Take everythin in all the sub-folder of the data
db_name = 'company_db'

folders = [f for f in glob.glob(r"data/*") if not f.endswith('.ipynb')]

print(folders)

def add_metadata(doc, doc_type):
    doc.metadata['doc_type'] = doc_type
    return doc

text_loader_kwargs = {'encoding': 'utf-8'}

documents = []
for folder in folders:
    doc_type = os.path.basename(folder)
    loader = DirectoryLoader(folder, glob= "**/*.md", loader_cls= TextLoader, loader_kwargs= text_loader_kwargs, show_progress= True)
    folder_docs = loader.load()
    print(folder_docs)
    documents.extend([add_metadata(doc, doc_type) for doc in folder_docs])

text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1500, 
                                      chunk_overlap = 200,
                                      separators= ["\n\n","\n","." ," ", ""])
chunks = text_splitter.split_documents(documents)


# Put the chuncks of data into a Vector Store that associates a Vector Embedding with each chunk

embeddings = OpenAIEmbeddings()

if os.path.exists(db_name):
    Chroma(persist_directory= db_name, embedding_function= embeddings).delete_collection()

# Create vector store
vectorstore = Chroma.from_documents(documents=chunks, embedding= embeddings, persist_directory= db_name)
collection = vectorstore._collection
print(f"Vectorstore created with {vectorstore._collection.count()} documents")