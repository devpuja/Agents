from services.document_loader import DocumentLoader
from services.text_splitter import TextSplitter
from services.chroma_service import add_document_chunk, reset_collection

class IndexingService:
    def __init__(self):
        self.document_loader = DocumentLoader()
        self.text_splitter = TextSplitter()

    def index_documents(self, documents_path: str, chunk_size: int = 500):
        # Reset the ChromaDB collection before adding new documents
        reset_collection()
        print("Collection has been reset.")

        documents = self.document_loader.load_documents(documents_path)
        for doc in documents:
            chunks = self.text_splitter.split(doc['content'], chunk_size)
            for idx, chunk in enumerate(chunks):
                add_document_chunk(chunk, doc['filename'], idx)

        print("Documents have been indexed into ChromaDB.")