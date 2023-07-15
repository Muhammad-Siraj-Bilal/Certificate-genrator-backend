from fastapi import FastAPI, Depends, Body
from utils.connect_to_db import Base, engine
import utils.crud as crud, tables.tables as tables
from fastapi.responses import FileResponse
from schema.schema import MemberSchema
from utils.cert_generator import *
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()
app.mount("/resources", StaticFiles(directory="resources"))

Base.metadata.create_all(bind=engine)

@app.post("/users")
def createUser(member: MemberSchema, db=Depends(crud.get_db)):

    # this function takes in the member info data and 
    # creates a tables Member object of a user 
    new_user = tables.Member(**member.model_dump())

    # commits this new user to the database
    new_user = crud.createMember(new_user, db)
    return new_user

@app.post("/api/validate")
def validate(email:str = Body(), track:str = Body(), db=Depends(crud.get_db)):

    # checks if the user exists in the database and
    # if the user is eligible to get a certificate 
    user = crud.get_user(email, db)
    result = crud.certify(user)
    return result

@app.get("/api/get_certificate/{email}")
def getCertificate(email:str, db=Depends(crud.get_db)):
    user = crud.get_user(email, db)

    # check if the user has a certificate 
    hasCertificate: bool = crud.certify(user)
    if hasCertificate:
        template = generate_cert(user.fullName, user.track)
        # if not template.any():
        print("working")
        filePath = f'{user.fullName}.png'
        cv2.imwrite(filePath, template)
        response = FileResponse(filePath)

        # delete file 
        # os.remove(filePath)
        return response

    return {"status":"User has not been assigned a certificate"}
