from fastapi import FastAPI, Depends, Body
from connect_to_db import Base, engine
import crud, tables
from fastapi.responses import FileResponse
from schema import MemberSchema

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/users")
def create_user(member: MemberSchema, db=Depends(crud.get_db)):
    new_user = tables.Member(**member.model_dump())
    new_user = crud.createMember(new_user, db)
    return new_user

@app.post("/api/validate")
def validate(email:str = Body(), track:str = Body(), db=Depends(crud.get_db)):
    result = crud.certificate(email, track, db)
    return result

@app.get("/api/get_certificate/{email}")
def certificate(email:str, db=Depends(crud.get_db)):
    user = crud.get_user(email, db)
    with open(f"{user.fullName}.txt", 'w') as file:
        file.write(user.fullName)
    return FileResponse(path = f"{user.fullName}.txt", media_type="text/plain", filename=f"{user.fullName}.txt")

