from sqlalchemy.orm import Session
from utils.connect_to_db import localSession
import tables.tables as tables

def get_db()-> Session:
    session: Session = localSession()
    try:
        yield session
    finally:
        session.close()

def createMember(member: tables.Member, db: Session):
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def get_user(email: str, db: Session)->tables.Member|None:
    result = db.query(tables.Member).filter(tables.Member.email == email)
    try:
        user = result[0]
        return user
    except:
        return None


def validate(email: str, track: str, db: Session):
    user = get_user(email, db)
    if user:
        return True
    return False

def certify(user: tables.Member):
    if user:
        return user.completed
    return False



