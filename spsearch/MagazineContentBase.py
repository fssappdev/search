from pydantic import BaseModel
from datetime import datetime
from typing import List,Annotated,Optional


class MagazineContentBase(BaseModel):
    magzine_id: int
    content: str
    vector_representation: str

    class Config:
        orm_mode=True


class MagazineContentCreate(MagazineContentBase):
    pass

class MagazineContent(MagazineContentBase):
    id:int
    magazine_id:int

    class Config:
        orm_mode=True