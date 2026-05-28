from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    display_name: str
    role: str = "reviewer"
    department: str = ""


class UserResponse(BaseModel):
    id: int
    username: str
    display_name: str
    role: str
    department: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    access_token: str
    user: UserResponse
