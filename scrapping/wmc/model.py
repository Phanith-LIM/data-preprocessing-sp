from pydantic import BaseModel

class ContentModel(BaseModel):
    title: str
    content: str
    audio: str
    
class ArticleModel(BaseModel):
    title: str
    date: str
    author: str
    link: str
