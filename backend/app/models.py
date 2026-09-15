from sqlalchemy import BigInteger, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Hospital(Base):
    __tablename__ = "hospitals"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    registration_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
    )

    address: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    city: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
    )

    # Relationships
    users = relationship("User", back_populates="hospital")
    departments = relationship("Department", back_populates="hospital")
    locations = relationship("Location", back_populates="hospital")
    assets = relationship("Asset", back_populates="hospital")


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    # Relationships
    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    hospital_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("hospitals.id"),
        nullable=False,
    )

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("roles.id"),
        nullable=False,
    )

    department_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id"),
        nullable=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    phone: Mapped[str | None] = mapped_column(
        String(30),
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(500),
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
    )

    # Relationships
    hospital = relationship("Hospital", back_populates="users")
    role = relationship("Role", back_populates="users")
    department = relationship("Department", foreign_keys=[department_id])
    managed_departments = relationship("Department", foreign_keys="[Department.manager_id]", back_populates="manager")
    uploaded_documents = relationship("AssetDocument", back_populates="uploader")
    moved_assets = relationship("AssetMovement", foreign_keys="[AssetMovement.moved_by]", back_populates="mover")
    notifications = relationship("Notification", back_populates="recipient")
    audit_logs = relationship("AuditLog", back_populates="user")


class Department(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    hospital_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("hospitals.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    manager_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    hospital = relationship("Hospital", back_populates="departments")
    manager = relationship("User", foreign_keys=[manager_id])
    assets = relationship("Asset", back_populates="department")
    locations = relationship("Location", back_populates="department")


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    hospital_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("hospitals.id"),
        nullable=False,
    )

    department_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id"),
        nullable=True,
    )

    parent_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("locations.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    hospital = relationship("Hospital", back_populates="locations")
    department = relationship("Department", back_populates="locations")
    parent = relationship("Location", remote_side=[id], back_populates="children")
    children = relationship("Location", back_populates="parent")
    assets = relationship("Asset", back_populates="location")


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    asset_id: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    hospital_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("hospitals.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    department_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id"),
        nullable=True,
    )

    location_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("locations.id"),
        nullable=True,
    )

    responsible_team: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    condition: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="Good",
    )

    operational_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Operational",
    )

    last_maintenance_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    next_maintenance_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    purchase_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    warranty_expiry: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    vendor_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    service_contact: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    service_email: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    warranty_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    hospital = relationship("Hospital", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    location = relationship("Location", back_populates="assets")
    maintenance_records = relationship("Maintenance", back_populates="asset")
    compliance_records = relationship("Compliance", back_populates="asset")
    documents = relationship("AssetDocument", back_populates="asset")
    movement_history = relationship("AssetMovement", back_populates="asset")


class Maintenance(Base):
    __tablename__ = "maintenance"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    asset_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("assets.id"),
        nullable=False,
    )

    maintenance_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    technician_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    vendor_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    maintenance_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    next_maintenance_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    asset = relationship("Asset", back_populates="maintenance_records")


class Compliance(Base):
    __tablename__ = "compliance"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    asset_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("assets.id"),
        nullable=False,
    )

    certification_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    certification_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    issuing_authority: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    issue_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expiry_date: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships
    asset = relationship("Asset", back_populates="compliance_records")


class AssetDocument(Base):
    __tablename__ = "asset_documents"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    asset_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("assets.id"),
        nullable=False,
    )

    document_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    document_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    uploaded_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )

    uploaded_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    asset = relationship("Asset", back_populates="documents")
    uploader = relationship("User")


class AssetMovement(Base):
    __tablename__ = "asset_movements"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    asset_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("assets.id"),
        nullable=False,
    )

    from_department_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id"),
        nullable=True,
    )

    to_department_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("departments.id"),
        nullable=True,
    )

    from_location_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("locations.id"),
        nullable=True,
    )

    to_location_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("locations.id"),
        nullable=True,
    )

    moved_by: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )

    movement_date: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Relationships
    asset = relationship("Asset", back_populates="movement_history")
    from_department = relationship("Department", foreign_keys=[from_department_id])
    to_department = relationship("Department", foreign_keys=[to_department_id])
    from_location = relationship("Location", foreign_keys=[from_location_id])
    to_location = relationship("Location", foreign_keys=[to_location_id])
    mover = relationship("User")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    user_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    entity_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    entity_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    changes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True,
    )

    user_agent: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relationships
    user = relationship("User")


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    recipient_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    notification_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    related_entity_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    related_entity_id: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True,
    )

    is_read: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    read_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    recipient = relationship("User")
