from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean , JSON,  func
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import update
from sqlalchemy import and_, or_

load_dotenv(".env")
Engine=create_engine(os.environ.get("POSTGRES_URI"))
Base= declarative_base()
Session = sessionmaker(bind=Engine)
session = Session()

class FAQS(Base):
    __tablename__ = 'faqs'

    id = Column(Integer(), primary_key=True)
    user_id = Column(Text, nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
