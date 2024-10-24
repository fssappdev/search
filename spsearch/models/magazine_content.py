# models/magazine_information.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector  # Import Vector from pgvector
from database import Base

class MagazineContent(Base):
    __tablename__ = "magazine_content"

    id = Column(Integer, primary_key=True, index=True)
    magazine_id = Column(Integer, ForeignKey('magazine_information.id'))
    content = Column(String, index=True)
    vector_representation = Column(Vector(384))




  


