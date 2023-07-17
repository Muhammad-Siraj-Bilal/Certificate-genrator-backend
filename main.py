from fastapi import FastAPI, Depends, Body, HTTPException, status
from utils.connect_to_db import Base, engine
import utils.crud as crud, tables.tables as tables
from fastapi.responses import FileResponse
from schema.schema import MemberSchema
from utils.cert_generator import *
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



TITLE = "Middlesex Computing Society Backend"
DESCRIPTION = "Backend system for MCS"
app = FastAPI(title= TITLE, description=DESCRIPTION)
app.mount("/resources", StaticFiles(directory="resources"))

origins = ["http://localhost","http://localhost:5500", "http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Base.metadata.create_all(bind=engine)

@app.post("/users", summary="Creates a new member account", description="Takes in a MemberSchema object which takes all the fields required to create a new user")
def createUser(member: MemberSchema, db=Depends(crud.get_db)):
    new_user = tables.Member(**member.model_dump())
    new_user = crud.createMember(new_user, db)
    if new_user:
        new_user.password = None
        return new_user
    return HTTPException(status_code=status.HTTP_409_CONFLICT)

@app.post("/certify/{email}", summary="This endpoint will certify that a user has completed the study group program")
def certifyUser(email:str, db= Depends(crud.get_db)):
    user = crud.get_user(email, db)
    user = crud.update(user, db, True)
    return user

@app.get("/users", summary="This endpoint gets all the Users, their is a query parameter track which could filter down the search")
def getUsers(track: str | None = None, db = Depends(crud.get_db)):
    result = crud.getMembers(db, track)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.delete("/delete/{email}", summary="This endpoint will delete the member with the specified email from the database")
def deleteUser(email: str, db = Depends(crud.get_db)):
    user = crud.get_user(email, db)
    crud.deleteMember(user, db)
    return {"status":"Member has been deleted"}

@app.post("/api/validate", tags=["Certificate"], summary="Validates if a user has been assigned a certificate")
def validate(email:str = Body(), track:str = Body(), db=Depends(crud.get_db)):
    user = crud.get_user(email, db)
    result = crud.certify(user)
    return result

@app.get("/api/get_certificate/{email}", tags=["Certificate"], summary="Downloads the certificate for a certified user")
def getCertificate(email:str, db=Depends(crud.get_db)):
    user = crud.get_user(email, db)

    # check if the user has a certificate 
    hasCertificate: bool = crud.certify(user)
    if hasCertificate:
        template = generate_cert(user.fullName, user.track)
        filePath = f'{user.fullName}.png'
        cv2.imwrite(filePath, template)
        response = FileResponse(filePath, filename=filePath, media_type="image/png")
        return response

    return {"status":"User has not been assigned a certificate"}
