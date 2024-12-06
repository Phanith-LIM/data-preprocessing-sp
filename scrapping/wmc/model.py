from pydantic import BaseModel
from typing import Optional

class ContentModel(BaseModel):
    title: str
    content: str
    audio: Optional[str]
    
class ArticleModel(BaseModel):
    title: str
    date: str
    author: str
    link: str
