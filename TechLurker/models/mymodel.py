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
    title = Column(String(1000))
    content = Column(String(1000))
    score = Column(String(1000))

    def __repr__(self):
        return "<AllData: id='%d', title='%s', content='%s', score='%s'>" % (self.id, self.title, self.content, self.score)

# class TechModel(Base):
#     """Create a TechModel class."""

#     __tablename__ = 'jobs'
#     id = Column(Integer, primary_key=True)
#     title = Column(Unicode)
#     loc = Column(Unicode)
#     description = Column(Unicode)
#     url = Column(Unicode)
#     compensation = Column(Unicode)
#     address = Column(Unicode)
#     employment = Column(Unicode)

#     def __init__(self, *args, **kwargs):
#         """Modify the method to do new things."""
#         super(TechModel, self).__init__(*args, **kwargs)

#     def to_dict(self):
#         """Take all model attributes and renders them as a dict."""
#         return {
#             'id': self.id,
#             'title': self.title,
#             'location': self.loc,
#             'description': self.description,
#             'url': self.url,
#             'compensation': self.compensation,
#             'address': self.address,
#             'employment': self.employment
#         }

