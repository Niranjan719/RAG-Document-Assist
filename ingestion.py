from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.text_splitter import TokenTextSplitter
import tiktoken

# Setup
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
ENCODER = tiktoken.encoding_for_model("text-embedding-3-small")

def num_tokens_from_string(text: str) -> int:
    """Returns the number of tokens in a text string."""
    return len(ENCODER.encode(text))

def safe_split(documents, max_tokens=500):
    """Ensure each document is below the Pinecone size limit."""
    splitter = TokenTextSplitter(encoding_name="cl100k_base", chunk_size=max_tokens, chunk_overlap=50)
    safe_docs = []
    for doc in documents:
        split_docs = splitter.split_documents([doc])
        safe_docs.extend(split_docs)
    return safe_docs

def ingest_docs():
    loader = ReadTheDocsLoader("langchain-docs/api.python.langchain.com/en/latest", encoding='utf-8')
    raw_documents = loader.load()
    print(f"Loaded {len(raw_documents)} raw documents")

    # Safe splitting
    documents = safe_split(raw_documents, max_tokens=500)
    print(f"After splitting, {len(documents)} documents to embed")

    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print("Uploading in batches to avoid size limits...")
    batch_size = 50
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        PineconeVectorStore.from_documents(
            batch, embeddings, index_name="langchain-doc-index"
        )
        print(f"Uploaded batch {i // batch_size + 1}")

    print("**** Loading to vectorstore done ***")

    # Loaded 344 raw documents
    # After splitting, 1885 documents to embed

if __name__ == "__main__":
    ingest_docs()
