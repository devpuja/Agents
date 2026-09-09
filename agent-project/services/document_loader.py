from pathlib import Path


class DocumentLoader:
    def load_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    def load_documents(self, folder_path: str) -> list[dict[str, str]]:
        documents: list[dict[str, str]] = []

        for file_path in Path(folder_path).glob('*.txt'):
            content = self.load_text(str(file_path))
            documents.append({
                "filename": file_path.name,
                "content": content
            })

        return documents
       