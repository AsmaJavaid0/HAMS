from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# Authentication Schemas
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

# Department Schemas
class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    code: str = Field(min_length=1, max_length=50)
    manager_id: Optional[int] = None
    description: Optional[str] = None
    status: str = Field(default="active")

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    manager_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: int
    hospital_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Location Schemas
class LocationBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    type: str = Field(min_length=1, max_length=50)
    parent_id: Optional[int] = None
    department_id: Optional[int] = None
    description: Optional[str] = None
    status: str = Field(default="active")

class LocationCreate(LocationBase):
    pass

class LocationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    type: Optional[str] = Field(None, min_length=1, max_length=50)
    parent_id: Optional[int] = None
    department_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None

class LocationResponse(LocationBase):
    id: int
    hospital_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Asset Schemas
class AssetBase(BaseModel):
    asset_id: str = Field(min_length=1, max_length=100)
    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=50)
    serial_number: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=200)
    model: Optional[str] = Field(None, max_length=200)
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    responsible_team: Optional[str] = Field(None, max_length=200)
    condition: str = Field(default="Good")
    operational_status: str = Field(default="Operational")
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None
    vendor_name: Optional[str] = Field(None, max_length=200)
    service_contact: Optional[str] = Field(None, max_length=100)
    service_email: Optional[EmailStr] = None
    warranty_notes: Optional[str] = None
    description: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    serial_number: Optional[str] = Field(None, max_length=100)
    manufacturer: Optional[str] = Field(None, max_length=200)
    model: Optional[str] = Field(None, max_length=200)
    department_id: Optional[int] = None
    location_id: Optional[int] = None
    responsible_team: Optional[str] = Field(None, max_length=200)
    condition: Optional[str] = None
    operational_status: Optional[str] = None
    last_maintenance_date: Optional[datetime] = None
    next_maintenance_date: Optional[datetime] = None
    purchase_date: Optional[datetime] = None
    warranty_expiry: Optional[datetime] = None
    vendor_name: Optional[str] = Field(None, max_length=200)
    service_contact: Optional[str] = Field(None, max_length=100)
    service_email: Optional[EmailStr] = None
    warranty_notes: Optional[str] = None
    description: Optional[str] = None

class AssetResponse(AssetBase):
    id: int
    hospital_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Maintenance Schemas
class MaintenanceBase(BaseModel):
    maintenance_date: datetime
    status: str
    technician_name: Optional[str] = Field(None, min_length=1, max_length=200)
    vendor_name: Optional[str] = Field(None, max_length=200)
    maintenance_type: Optional[str] = Field(None, min_length=1, max_length=100)
    notes: Optional[str] = None
    next_maintenance_date: Optional[datetime] = None

class MaintenanceCreate(MaintenanceBase):
    asset_id: int

class MaintenanceUpdate(BaseModel):
    maintenance_date: Optional[datetime] = None
    status: Optional[str] = None
    technician_name: Optional[str] = Field(None, min_length=1, max_length=200)
    vendor_name: Optional[str] = Field(None, max_length=200)
    maintenance_type: Optional[str] = Field(None, min_length=1, max_length=100)
    notes: Optional[str] = None
    next_maintenance_date: Optional[datetime] = None

class MaintenanceResponse(MaintenanceBase):
    id: int
    asset_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Compliance Schemas
class ComplianceBase(BaseModel):
    certification_name: str = Field(min_length=1, max_length=200)
    certification_number: Optional[str] = Field(None, max_length=100)
    issuing_authority: Optional[str] = Field(None, max_length=200)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: str = Field(default="active")
    notes: Optional[str] = None

class ComplianceCreate(ComplianceBase):
    asset_id: int

class ComplianceUpdate(BaseModel):
    certification_name: Optional[str] = Field(None, min_length=1, max_length=200)
    certification_number: Optional[str] = Field(None, max_length=100)
    issuing_authority: Optional[str] = Field(None, max_length=200)
    issue_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class ComplianceResponse(ComplianceBase):
    id: int
    asset_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Asset Document Schemas
class AssetDocumentBase(BaseModel):
    asset_id: int
    document_name: str = Field(min_length=1, max_length=255)
    document_type: str = Field(min_length=1, max_length=100)
    file_url: str = Field(min_length=1, max_length=500)
    uploaded_by: int

class AssetDocumentCreate(AssetDocumentBase):
    pass

class AssetDocumentUpdate(BaseModel):
    asset_id: Optional[int] = None
    document_name: Optional[str] = Field(None, min_length=1, max_length=255)
    document_type: Optional[str] = Field(None, min_length=1, max_length=100)
    file_url: Optional[str] = Field(None, min_length=1, max_length=500)
    uploaded_by: Optional[int] = None

class AssetDocumentResponse(AssetDocumentBase):
    id: int
    uploaded_at: datetime

    class Config:
        from_attributes = True

# Asset Movement Schemas
class AssetMovementBase(BaseModel):
    asset_id: int
    from_department_id: Optional[int] = None
    to_department_id: Optional[int] = None
    from_location_id: Optional[int] = None
    to_location_id: Optional[int] = None
    movement_date: datetime
    notes: Optional[str] = None

class AssetMovementCreate(AssetMovementBase):
    pass

class AssetMovementUpdate(BaseModel):
    asset_id: Optional[int] = None
    from_department_id: Optional[int] = None
    to_department_id: Optional[int] = None
    from_location_id: Optional[int] = None
    to_location_id: Optional[int] = None
    movement_date: Optional[datetime] = None
    notes: Optional[str] = None

class AssetMovementResponse(AssetMovementBase):
    id: int
    moved_by: int
    created_at: datetime

    class Config:
        from_attributes = True

# Audit Log Schemas
class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    action: str = Field(min_length=1, max_length=100)
    entity_type: str = Field(min_length=1, max_length=50)
    entity_id: int
    entity_name: Optional[str] = Field(None, max_length=255)
    changes: Optional[str] = None
    ip_address: Optional[str] = Field(None, max_length=45)
    user_agent: Optional[str] = Field(None, max_length=500)

class AuditLogCreate(AuditLogBase):
    pass

class AuditLogResponse(AuditLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Notification Schemas
class NotificationBase(BaseModel):
    recipient_id: int
    title: str = Field(min_length=1, max_length=200)
    message: str = Field(min_length=1)
    notification_type: str = Field(min_length=1, max_length=50)
    related_entity_type: Optional[str] = Field(None, max_length=50)
    related_entity_id: Optional[int] = None
    is_read: bool = Field(default=False)

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    is_read: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: int
    created_at: datetime
    read_at: Optional[datetime] = None

    class Config:
        from_attributes = True