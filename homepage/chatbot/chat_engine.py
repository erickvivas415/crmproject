from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.chains import RetrievalQA


def load_and_index_data():
    # Resolve the path to knowledge.txt inside chatbot/data/
    base_dir = Path(__file__).resolve().parent
    file_path = base_dir / "data" / "knowledge.txt"

    # Load and split the document
    loader = TextLoader(str(file_path))
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Generate embeddings and store vectors in Chroma
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=str(base_dir / "db")
    )
    db.persist()  # Save the database


def get_qa_chain():
    # Load the persisted vector store
    base_dir = Path(__file__).resolve().parent
    db = Chroma(
        persist_directory=str(base_dir / "db"),
        embedding_function=OpenAIEmbeddings()
    )
    retriever = db.as_retriever()

    # Create a Retrieval QA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=OpenAI(temperature=0),
        retriever=retriever
    )
    return qa_chain


def ask_question(query):
    qa_chain = get_qa_chain()
    return qa_chain.invoke(query)
    