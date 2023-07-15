from pydantic import BaseModel

class MemberSchema(BaseModel):
    email: str 
    fullName: str 
    track: str 
    completed: bool = True
    password: str | None = None
    is_mentor: bool = True

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "email": "john@example.com",
                "fullName": "John Doe",
                "track": "Python",
                "completed": True,
                "password": "password123",}
        }
