from pathlib import Path


DOCUMENTS_DIR = Path("documents")


def load_documents() -> list[dict[str, str]]:
    documents: list[dict[str, str]] = []
    
    for file_path in DOCUMENTS_DIR.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() != ".txt":
            continue

        content = file_path.read_text(encoding="utf-8")
        documents.append(
            {
                "filename": file_path.name,
                "content": content,
            }
        )

    return documents