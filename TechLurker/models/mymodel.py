"""Model for our database."""
from sqlalchemy import (
    Column,
    Integer,
    Unicode,
)

from .meta import Base


class TechModel(Base):
    """Create a TechModel class."""

    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    description = Column(Unicode)
    url = Column(Unicode)
    compensation = Column(Unicode)
    address = Column(Unicode)
    employment = Column(Unicode)

    def __init__(self, *args, **kwargs):
        """Modify the method to do new things."""
        super(TechModel, self).__init__(*args, **kwargs)

    def to_dict(self):
        """Take all model attributes and renders them as a dict."""
        return {
            'id': self.id,
            'description': self.description,
            'url': self.url,
            'compensation': self.compensation,
            'address': self.address,
            'employment': self.employment
        }
