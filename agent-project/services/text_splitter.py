class TextSplitter:
    def split(self, text: str, chunk_size: int) -> list[str]:
        """
        Splits the input text into chunks of specified size.

        Args:
            text (str): The input text to be split.
            chunk_size (int): The maximum size of each chunk.

        Returns:
            list[str]: A list of text chunks.
        """
        if chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer.")

        chunks: list[str] = []
        for i in range(0, len(text), chunk_size):
            chunks.append(text[i:i + chunk_size])
        return chunks