from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.dependencies import get_current_user
from app.database import get_db
from app.models import Hospital, Role, User
from app.schemas import HospitalRegistration, LoginRequest
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.get("/staff")
def get_staff(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not authorized to view staff")

    hospital_id = current_user["user"].hospital_id
    users = db.execute(
        select(User).where(User.hospital_id == hospital_id)
    ).scalars().all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "status": user.status,
        }
        for user in users
    ]


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user),
):
    user = current_user["user"]
    role = current_user["role"]

    return {
        "id": user.id,
        "hospital_id": user.hospital_id,
        "hospital_name": user.hospital.name,
        "full_name": user.full_name,
        "email": user.email,
        "role": role,
        "department_id": user.department_id,
    }

@router.post("/register-hospital")
def register_hospital(
    data: HospitalRegistration,
    db: Session = Depends(get_db),
):
    hospital_email = str(data.hospital_email).lower().strip()
    admin_email = str(data.admin_email).lower().strip()
    registration_number = data.registration_number.strip()

    # --------------------------------
    # Check hospital registration number
    # --------------------------------

    existing_hospital = db.execute(
        select(Hospital).where(
            Hospital.registration_number == registration_number
        )
    ).scalar_one_or_none()

    if existing_hospital:
        raise HTTPException(
            status_code=409,
            detail="Hospital registration number already exists.",
        )

    # --------------------------------
    # Check admin email
    # --------------------------------

    existing_user = db.execute(
        select(User).where(
            User.email == admin_email
        )
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Administrator email already exists.",
        )

    # --------------------------------
    # Find ADMIN role
    # --------------------------------

    admin_role = db.execute(
        select(Role).where(func.lower(Role.code) == "admin")
    ).scalar_one_or_none()

    if not admin_role:
        raise HTTPException(
            status_code=500,
            detail="ADMIN role is not configured.",
        )

    try:
        # --------------------------------
        # Create hospital
        # --------------------------------

        hospital = Hospital(
            name=data.hospital_name.strip(),
            registration_number=registration_number,
            email=hospital_email,
            phone=data.hospital_phone,
            address=data.address.strip(),
            city=data.city.strip(),
            country=data.country.strip(),
            status="active",
        )

        db.add(hospital)

        # Flush gives us hospital.id
        # without committing yet.
        db.flush()

        # --------------------------------
        # Create first administrator
        # --------------------------------

        admin_user = User(
            hospital_id=hospital.id,
            role_id=admin_role.id,
            full_name=data.admin_full_name.strip(),
            email=admin_email,
            password_hash=hash_password(data.password),
            phone=data.admin_phone,
            photo_url=data.photo_url,
            status="active",
        )

        db.add(admin_user)

        # --------------------------------
        # Commit BOTH records together
        # --------------------------------

        db.commit()

        return {
            "message": "Hospital and administrator registered successfully.",
            "hospital_id": hospital.id,
            "user_id": admin_user.id,
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Registration failed. No changes were saved.",
        )
    # ============================================
# LOGIN
# ============================================

@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    email = str(data.email).lower().strip()

    # --------------------------------
    # Find active user
    # --------------------------------

    user = db.execute(
        select(User).where(
            User.email == email,
            User.status == "active",
        )
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    # --------------------------------
    # Verify password
    # --------------------------------

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password.",
        )

    # --------------------------------
    # Check hospital
    # --------------------------------

    hospital = db.execute(
        select(Hospital).where(
            Hospital.id == user.hospital_id,
            Hospital.status == "active",
        )
    ).scalar_one_or_none()

    if not hospital:
        raise HTTPException(
            status_code=403,
            detail="Hospital account is inactive or unavailable.",
        )

    # --------------------------------
    # Get role
    # --------------------------------

    role = db.execute(
        select(Role).where(
            Role.id == user.role_id
        )
    ).scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=500,
            detail="User role is not configured.",
        )

    role_code = str(role.code).strip().lower()

    if role_code == "manager":
        raise HTTPException(
            status_code=403,
            detail="Legacy Manager role is not supported in V1.",
        )

    if role_code not in {"admin", "nurse", "biomedical"}:
        raise HTTPException(
            status_code=403,
            detail="Unsupported role for this application.",
        )

    # --------------------------------
    # Create JWT
    # --------------------------------

    access_token = create_access_token(
        {
            "sub": str(user.id),
            "hospital_id": str(user.hospital_id),
            "role": role_code,
        }
    )

    return {
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "hospital_id": user.hospital_id,
            "hospital_name": hospital.name,
            "full_name": user.full_name,
            "email": user.email,
            "role": role_code,
            "department_id": user.department_id,
        },
    }
