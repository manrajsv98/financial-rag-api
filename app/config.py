from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    chroma_db_path: str = "./chroma_db"
    chroma_collection_name: str = "financial_documents"

    class Config:
        env_file = ".env"

settings = Settings()