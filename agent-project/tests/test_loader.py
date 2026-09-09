from services.document_loader import DocumentLoader
from services.text_splitter import TextSplitter

# Test Document Loader
loader = DocumentLoader()
docs = loader.load_documents(str("documents"))
for doc in docs:
    print(f"Filename: {doc['filename']}")
    print(f"Content: {doc['content'][:100]}...")  # Print first 100 characters of content
    print()
    
    
# Test Chunks    
splitter = TextSplitter()
#chunks = splitter.split(docs[0]['content'], 50)  # Split the first document into chunks of size 50
chunks = splitter.split("A" * 1500, 400)
print(f"Number of chunks: {len(chunks)}")