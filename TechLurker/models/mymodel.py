"""Model for our database."""
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
    String
)

from .meta import Base


class AllData(Base):
    __tablename__ = 'alldata'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    score = Column(String)


class PyjobData(Base):
    __tablename__ = 'pyjob'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    descrip = Column(String)
    loc = Column(String)
    job_type = Column(String)
    url = Column(String)
