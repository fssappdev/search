from pydantic import BaseModel
from datetime import datetime
from typing import List,Annotated,Optional


class MagazineInfomationBase(BaseModel):
    title: str
    author: str
    publication_date: datetime
    category: str

    class Config:
        orm_mode=True

class MagazineInfomationCreate(MagazineInfomationBase):
    pass  

class MagazineInfomation(MagazineInfomationBase):
    id:int

    class Config:
        orm_mode=True
