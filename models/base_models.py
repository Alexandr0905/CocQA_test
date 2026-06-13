from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from constants import Roles, City


class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20,
                                description="passwordRepeat должен полностью совпадать с полем password")
    roles: List[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    class Config:
        json_encoders = {
            Roles: lambda v: v.value
        }


class CreateUserData(TestUser):
    verified: bool
    banned: bool


class LoginData(BaseModel):
    email: str
    password: str


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                       description="Email пользователя")
    fullName: str = Field(min_length=1, max_length=100, description="Полное имя пользователя")
    verified: bool
    banned: bool
    roles: List[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени. Ожидается формат ISO 8601.")
        return value


class MovieResponseModel(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str] = None
    location: City
    published: bool
    rating: Optional[float] = None
    genreId: int
    createdAt: datetime

class MoviesListResponseModel(BaseModel):
    count: int = Field(..., ge=0)
    movies: List[MovieResponseModel]