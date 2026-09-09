from pathlib import Path

class FileStorageService:
    DOCUMENTS_FOLDER = "documents"
    
    def save_file(self, file_name:str, content:bytes) -> str:
        # Ensure the documents folder exists
        folder_path = Path(self.DOCUMENTS_FOLDER)
        folder_path.mkdir(parents=True, exist_ok=True)
        
        # Define the full path for the file
        file_path = folder_path / file_name
        
        # Write the content to the file
        with open(file_path, "wb") as f:
            f.write(content)
        
        return str(file_path)