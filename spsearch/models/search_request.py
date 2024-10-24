from enum import Enum
from pydantic import BaseModel

class SearchType(str, Enum):
    keyword = "keyword"
    vector = "vector"
    hybrid = "hybrid"

class SearchRequest(BaseModel):
    query: str
    search_type: str  # "keyword", "vector", or "hybrid"