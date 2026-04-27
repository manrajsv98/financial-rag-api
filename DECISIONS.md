## Chunking Strategy

Used word-based chunking with overlap for the MVP.

- Chunk size: 500 words
- Overlap: 100 words

This balances context preservation and retrieval accuracy. Overlap ensures important context is not lost between chunks.


## Embeddings and Vector Store

Used OpenAI `text-embedding-3-small` for embeddings because it is cost-effective and suitable for semantic retrieval in the MVP.

Used ChromaDB as the initial vector database because it is simple to run locally, supports persistent storage, and allows fast iteration before adding a production cloud option such as Azure AI Search.