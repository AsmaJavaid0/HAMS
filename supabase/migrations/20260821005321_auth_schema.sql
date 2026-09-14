-- ============================================
-- ASSETCARE - AUTHENTICATION SCHEMA
-- ============================================

-- 1. HOSPITALS
CREATE TABLE hospitals (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(150) NOT NULL,
    registration_number VARCHAR(100) NOT NULL UNIQUE,

    email VARCHAR(150) NOT NULL,
    phone VARCHAR(30),

    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,

    status VARCHAR(30) NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT hospitals_status_check
        CHECK (status IN ('active', 'inactive', 'suspended'))
);


-- 2. ROLES
CREATE TABLE roles (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) NOT NULL UNIQUE,

    description VARCHAR(255),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- 3. USERS
CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    hospital_id BIGINT NOT NULL,
    role_id BIGINT NOT NULL,

    full_name VARCHAR(150) NOT NULL,

    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,

    phone VARCHAR(30),
    photo_url VARCHAR(500),

    status VARCHAR(30) NOT NULL DEFAULT 'active',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT users_hospital_fk
        FOREIGN KEY (hospital_id)
        REFERENCES hospitals(id)
        ON DELETE CASCADE,

    CONSTRAINT users_role_fk
        FOREIGN KEY (role_id)
        REFERENCES roles(id),

    CONSTRAINT users_status_check
        CHECK (status IN ('active', 'inactive', 'suspended'))
);


-- 4. PERMISSIONS
CREATE TABLE permissions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    code VARCHAR(100) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,

    description VARCHAR(255),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- 5. ROLE-PERMISSION
CREATE TABLE role_permissions (
    role_id BIGINT NOT NULL,
    permission_id BIGINT NOT NULL,

    PRIMARY KEY (role_id, permission_id),

    CONSTRAINT role_permissions_role_fk
        FOREIGN KEY (role_id)
        REFERENCES roles(id)
        ON DELETE CASCADE,

    CONSTRAINT role_permissions_permission_fk
        FOREIGN KEY (permission_id)
        REFERENCES permissions(id)
        ON DELETE CASCADE
);


-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_users_hospital_id
    ON users(hospital_id);

CREATE INDEX idx_users_role_id
    ON users(role_id);

CREATE INDEX idx_users_email
    ON users(email);

CREATE INDEX idx_role_permissions_permission_id
    ON role_permissions(permission_id);


-- ============================================
-- DEFAULT ROLES
-- ============================================

INSERT INTO roles (name, code, description)
VALUES
    ('Administrator', 'ADMIN', 'Full access to the hospital AssetCare system'),
    ('Manager', 'MANAGER', 'Management and operational access'),
    ('Biomedical Engineer', 'BIOMEDICAL', 'Biomedical equipment and maintenance access'),
    ('Nurse', 'NURSE', 'Nursing and assigned asset access');


-- ============================================
-- DEFAULT PERMISSIONS
-- ============================================

INSERT INTO permissions (code, name, description)
VALUES
    ('HOSPITAL_VIEW', 'View Hospital', 'View hospital information'),
    ('HOSPITAL_MANAGE', 'Manage Hospital', 'Manage hospital information'),

    ('USER_VIEW', 'View Users', 'View hospital users'),
    ('USER_CREATE', 'Create Users', 'Create hospital users'),
    ('USER_UPDATE', 'Update Users', 'Update hospital users'),
    ('USER_DELETE', 'Delete Users', 'Delete hospital users'),

    ('ASSET_VIEW', 'View Assets', 'View assets'),
    ('ASSET_CREATE', 'Create Assets', 'Create assets'),
    ('ASSET_UPDATE', 'Update Assets', 'Update assets'),
    ('ASSET_DELETE', 'Delete Assets', 'Delete assets'),

    ('MAINTENANCE_VIEW', 'View Maintenance', 'View maintenance records'),
    ('MAINTENANCE_CREATE', 'Create Maintenance', 'Create maintenance records'),
    ('MAINTENANCE_UPDATE', 'Update Maintenance', 'Update maintenance records'),

    ('FAULT_CREATE', 'Report Fault', 'Report asset faults'),
    ('FAULT_VIEW', 'View Faults', 'View reported faults'),

    ('REPORT_VIEW', 'View Reports', 'View system reports');