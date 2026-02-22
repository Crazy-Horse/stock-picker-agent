from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

def ingest():
    loader = DirectoryLoader('data/raw', glob="./*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=OpenAIEmbeddings(),
        persist_directory="./chroma_db"
    )
    print("Ingestion complete. Vector store saved to ./chroma_db")

def ingest_with_metadata():
    # 1. Setup paths and model
    raw_data_path = "data/raw"
    persist_directory = "./chroma_db"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    documents = []
    
    # 2. Iterate through files in your raw data folder
    for filename in os.listdir(raw_data_path):
        if filename.endswith(".pdf"):
            # Simple convention: Filename starts with TICKER_ (e.g., AAPL_report.pdf)
            ticker = filename.split('_')[0].upper()
            
            print(f"Processing {filename} for ticker: {ticker}...")
            
            loader = PyPDFLoader(os.path.join(raw_data_path, filename))
            file_docs = loader.load()
            
            # Attach ticker to metadata of every page/document
            for doc in file_docs:
                doc.metadata["ticker"] = ticker
                doc.metadata["source_file"] = filename
                
            documents.extend(file_docs)

    # 3. Split into chunks
    # Chunking keeps the metadata intact for every fragment!
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)

    # 4. Save to Chroma
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
        collection_name="research_pack"
    )
    
    print(f"Successfully ingested {len(chunks)} chunks across {len(documents)} documents.")

if __name__ == "__main__":
    ingest_with_metadata()