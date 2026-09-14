from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HospitalRegistration(BaseModel):
    hospital_name: str = Field(min_length=2, max_length=150)
    registration_number: str = Field(min_length=1, max_length=100)
    hospital_email: EmailStr
    hospital_phone: str | None = None
    address: str = Field(min_length=1, max_length=255)
    city: str = Field(min_length=1, max_length=100)
    country: str = Field(min_length=1, max_length=100)

    admin_full_name: str = Field(min_length=2, max_length=150)
    admin_email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    admin_phone: str | None = None
    photo_url: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str