from sqlalchemy.orm import Session
from utils.connect_to_db import localSession
import tables.tables as tables
from sqlalchemy import text



def get_db()-> Session:
    session: Session = localSession()
    try:
        yield session
    finally:
        session.close()

def getMembers(db: Session, track: str | None = None):
    if track == None: 
        return db.query(tables.Member).all()
    
    try:
        results = db.query(tables.Member).filter(tables.Member.track == track).all()
        return results
    except:
        return None




def createMember(member: tables.Member, db: Session):
    user = get_user(member.email, db)
    if user: 
        return None
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def deleteMember(member: tables.Member, db: Session):
    db.delete(member)
    db.commit()

def get_user(email: str, db: Session)->tables.Member|None:
    result = db.query(tables.Member).filter(tables.Member.email == email)
    try:
        user = result[0]
        return user
    except:
        return None

def update(user:tables.Member, db: Session, value:bool):
    if not user.completed:
        user.completed = value
    db.commit()
    db.refresh(user)
    return user


def validate(email: str, track: str, db: Session):
    user = get_user(email, db)
    if user:
        return True
    return False

def certify(user: tables.Member):
    if user:
        return user.completed
    return False



