from pydantic import BaseModel


class LoginBody(BaseModel):
    email: str
    password: str


class RegisterBody(BaseModel):
    email: str
    password: str
    firstName: str
    lastName: str
    role: str
