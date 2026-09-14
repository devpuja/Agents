from pathlib import Path
from pypdf import PdfReader

class DocumentLoader:
    def load_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()


    def load_documents(self, folder_path: str) -> list[dict[str, str]]:
        documents: list[dict[str, str]] = []

        for file_path in Path(folder_path).glob('*.txt'):
            document = self.load_file(str(file_path))
            documents.append(document)
        return documents


    def load_pdf(self, file_path: str) -> str:
        reader = PdfReader(file_path)
        pages: list[str] = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        return "\n\n".join(pages)


    def load_file(self, file_path: str) -> dict[str, str]:
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        extension = path.suffix.lower()

        content = ""
        if extension == ".txt":
            content = self.load_text(str(path))
        elif extension == ".pdf":
            content = self.load_pdf(str(path))
        else:
            raise ValueError(f"Unsupported file type: {extension}. Supported types: .txt, .pdf")

        return {
            "filename": path.name,
            "content": content
        }