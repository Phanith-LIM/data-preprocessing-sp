from pydantic import BaseModel
from typing import List

class AMSArticleModel(BaseModel):
    title: str
    audio_src: str
    date: str
    content: str
    categories: List[str]
    url: str
    
    
class LinkArticleModel(BaseModel):
    id: str
    title: str
    url: str
