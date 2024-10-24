# models/magazine_information.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from database import Base
#Base = declarative_base()


class MagazineInformation(Base):
    __tablename__ = "magazine_information"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    publication_date = Column(DateTime, index=True)
    category = Column(String, index=True)



    