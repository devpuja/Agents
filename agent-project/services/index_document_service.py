from services.document_loader import DocumentLoader
from services.text_splitter import TextSplitter
from services.chroma_service import add_document_chunk, reset_collection

loader = DocumentLoader()
splitter = TextSplitter()

# Reset the ChromaDB collection before adding new documents
reset_collection()
print("Collection has been reset.")

documents = loader.load_documents("documents")
for doc in documents:
    chunks = splitter.split(doc['content'], 500)
    for idx, chunk in enumerate(chunks):
        add_document_chunk(chunk, doc['filename'], idx)

print("Documents have been indexed into ChromaDB.")