-- ============================================
-- HOSPITAL ASSET MANAGEMENT SCHEMA
-- ============================================

-- 1. DEPARTMENTS
CREATE TABLE departments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hospital_id BIGINT NOT NULL,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,
    manager_id BIGINT,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT departments_hospital_fk
        FOREIGN KEY (hospital_id)
        REFERENCES hospitals(id)
        ON DELETE CASCADE,
    CONSTRAINT departments_manager_fk
        FOREIGN KEY (manager_id)
        REFERENCES users(id),
    CONSTRAINT departments_status_check
        CHECK (status IN ('active', 'inactive'))
);

-- 2. LOCATIONS
CREATE TABLE locations (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    hospital_id BIGINT NOT NULL,
    department_id BIGINT,
    parent_id BIGINT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    description TEXT,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT locations_hospital_fk
        FOREIGN KEY (hospital_id)
        REFERENCES hospitals(id)
        ON DELETE CASCADE,
    CONSTRAINT locations_department_fk
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL,
    CONSTRAINT locations_parent_fk
        FOREIGN KEY (parent_id)
        REFERENCES locations(id)
        ON DELETE CASCADE,
    CONSTRAINT locations_status_check
        CHECK (status IN ('active', 'inactive'))
);

-- 3. ASSETS
CREATE TABLE assets (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asset_id VARCHAR(100) NOT NULL UNIQUE,
    hospital_id BIGINT NOT NULL,
    name VARCHAR(200) NOT NULL,
    category VARCHAR(50) NOT NULL,
    serial_number VARCHAR(100),
    manufacturer VARCHAR(200),
    model VARCHAR(200),
    department_id BIGINT,
    location_id BIGINT,
    responsible_team VARCHAR(200),
    condition VARCHAR(20) NOT NULL DEFAULT 'Good',
    operational_status VARCHAR(30) NOT NULL DEFAULT 'Operational',
    last_maintenance_date TIMESTAMPTZ,
    next_maintenance_date TIMESTAMPTZ,
    purchase_date TIMESTAMPTZ,
    warranty_expiry TIMESTAMPTZ,
    vendor_name VARCHAR(200),
    service_contact VARCHAR(100),
    service_email VARCHAR(200),
    warranty_notes TEXT,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT assets_hospital_fk
        FOREIGN KEY (hospital_id)
        REFERENCES hospitals(id)
        ON DELETE CASCADE,
    CONSTRAINT assets_department_fk
        FOREIGN KEY (department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL,
    CONSTRAINT assets_location_fk
        FOREIGN KEY (location_id)
        REFERENCES locations(id)
        ON DELETE SET NULL,
    CONSTRAINT assets_condition_check
        CHECK (condition IN ('Excellent', 'Good', 'Fair', 'Poor', 'Critical')),
    CONSTRAINT assets_operational_status_check
        CHECK (operational_status IN ('Operational', 'Under Maintenance', 'Out of Service', 'Quarantined', 'Pending Disposal', 'Retired'))
);

-- 4. MAINTENANCE
CREATE TABLE maintenance (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    maintenance_date TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL,
    technician_name VARCHAR(200) NOT NULL,
    vendor_name VARCHAR(200),
    maintenance_type VARCHAR(100) NOT NULL,
    notes TEXT,
    next_maintenance_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT maintenance_asset_fk
        FOREIGN KEY (asset_id)
        REFERENCES assets(id)
        ON DELETE CASCADE,
    CONSTRAINT maintenance_status_check
        CHECK (status IN ('Scheduled', 'In Progress', 'Completed', 'Cancelled'))
);

-- 5. COMPLIANCE
CREATE TABLE compliance (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    certification_name VARCHAR(200) NOT NULL,
    certification_number VARCHAR(100),
    issuing_authority VARCHAR(200),
    issue_date TIMESTAMPTZ,
    expiry_date TIMESTAMPTZ,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT compliance_asset_fk
        FOREIGN KEY (asset_id)
        REFERENCES assets(id)
        ON DELETE CASCADE,
    CONSTRAINT compliance_status_check
        CHECK (status IN ('active', 'expired', 'suspended'))
);

-- 6. ASSET DOCUMENTS
CREATE TABLE asset_documents (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    document_type VARCHAR(100) NOT NULL,
    file_url VARCHAR(500) NOT NULL,
    uploaded_by BIGINT NOT NULL,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT asset_documents_asset_fk
        FOREIGN KEY (asset_id)
        REFERENCES assets(id)
        ON DELETE CASCADE,
    CONSTRAINT asset_documents_uploader_fk
        FOREIGN KEY (uploaded_by)
        REFERENCES users(id)
);

-- 7. ASSET MOVEMENTS
CREATE TABLE asset_movements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    asset_id BIGINT NOT NULL,
    from_department_id BIGINT,
    to_department_id BIGINT,
    from_location_id BIGINT,
    to_location_id BIGINT,
    moved_by BIGINT NOT NULL,
    movement_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    notes TEXT,
    CONSTRAINT asset_movements_asset_fk
        FOREIGN KEY (asset_id)
        REFERENCES assets(id)
        ON DELETE CASCADE,
    CONSTRAINT asset_movements_from_dept_fk
        FOREIGN KEY (from_department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL,
    CONSTRAINT asset_movements_to_dept_fk
        FOREIGN KEY (to_department_id)
        REFERENCES departments(id)
        ON DELETE SET NULL,
    CONSTRAINT asset_movements_from_loc_fk
        FOREIGN KEY (from_location_id)
        REFERENCES locations(id)
        ON DELETE SET NULL,
    CONSTRAINT asset_movements_to_loc_fk
        FOREIGN KEY (to_location_id)
        REFERENCES locations(id)
        ON DELETE SET NULL,
    CONSTRAINT asset_movements_mover_fk
        FOREIGN KEY (moved_by)
        REFERENCES users(id)
);

-- 8. AUDIT LOGS
CREATE TABLE audit_logs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NOT NULL,
    entity_name VARCHAR(255),
    changes TEXT,
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 9. NOTIFICATIONS
CREATE TABLE notifications (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    recipient_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    related_entity_type VARCHAR(50),
    related_entity_id BIGINT,
    is_read BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    read_at TIMESTAMPTZ,
    CONSTRAINT notifications_recipient_fk
        FOREIGN KEY (recipient_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Indexes for better performance
CREATE INDEX idx_departments_hospital_id ON departments(hospital_id);
CREATE INDEX idx_locations_hospital_id ON locations(hospital_id);
CREATE INDEX idx_locations_department_id ON locations(department_id);
CREATE INDEX idx_locations_parent_id ON locations(parent_id);
CREATE INDEX idx_assets_hospital_id ON assets(hospital_id);
CREATE INDEX idx_assets_department_id ON assets(department_id);
CREATE INDEX idx_assets_location_id ON assets(location_id);
CREATE INDEX idx_maintenance_asset_id ON maintenance(asset_id);
CREATE INDEX idx_compliance_asset_id ON compliance(asset_id);
CREATE INDEX idx_asset_documents_asset_id ON asset_documents(asset_id);
CREATE INDEX idx_asset_documents_uploaded_by ON asset_documents(uploaded_by);
CREATE INDEX idx_asset_movements_asset_id ON asset_movements(asset_id);
CREATE INDEX idx_asset_movements_from_dept ON asset_movements(from_department_id);
CREATE INDEX idx_asset_movements_to_dept ON asset_movements(to_department_id);
CREATE INDEX idx_asset_movements_from_loc ON asset_movements(from_location_id);
CREATE INDEX idx_asset_movements_to_loc ON asset_movements(to_location_id);
CREATE INDEX idx_asset_movements_moved_by ON asset_movements(moved_by);
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_entity_type ON audit_logs(entity_type);
CREATE INDEX idx_audit_logs_entity_id ON audit_logs(entity_id);
CREATE INDEX idx_notifications_recipient_id ON notifications(recipient_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);