from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str
    top_k: int = 3


class AskResponse(BaseModel):
    answer: str
    sources: list[dict]
    

class IngestRequest(BaseModel):
    file_path: str
    chunk_size: int = 500
    overlap: int = 100


class IngestResponse(BaseModel):
    status: str
    file_path: str
    chunks_created: int
    chunks_inserted: int