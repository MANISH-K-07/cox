# We're creating a common format 
# so everything can be handled 
# by the same downstream pipeline.

from pydantic import BaseModel
from typing import Optional


class Document(BaseModel):
    id: str
    source: str
    source_type: str
    text: str
    timestamp: Optional[str] = None
    author: Optional[str] = None
    metadata: dict = {}
