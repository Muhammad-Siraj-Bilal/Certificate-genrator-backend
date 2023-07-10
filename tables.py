from connect_to_db import Base
from sqlalchemy import Column, String, Integer, Boolean


class Member(Base):
    __tablename__ = "Member"

    fullName = Column(String)
    email = Column(String, primary_key=True, nullable=False)
    track = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    is_mentor = Column(Boolean, default=False)
    password = Column(String, nullable=True)
