from sqlalchemy import Integer, Column, String, DateTime
from datetime import datetime

from src.core.database import Base


class Job(Base):
    __tablename__ = 'jobs'
    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    description = Column( 'description', String)
    location = Column('location', String )
    company_name = Column('company_name', String)
    created_at = Column('created_at', DateTime, default=datetime.now)