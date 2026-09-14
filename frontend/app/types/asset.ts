export const ASSET_CATEGORIES = [
  'Medical Equipment',
  'Diagnostic Equipment',
  'Emergency Equipment',
  'Surgical Equipment',
  'Laboratory Equipment',
  'Furniture',
  'IT Equipment',
  'Other'
] as const

export type AssetCategory = typeof ASSET_CATEGORIES[number]

export const ASSET_CONDITIONS = [
  'Excellent',
  'Good',
  'Fair',
  'Poor',
  'Critical'
] as const

export type AssetCondition = typeof ASSET_CONDITIONS[number]

export type MaintenancePriority =
  | 'Not Scheduled'
  | 'Low'
  | 'Medium'
  | 'High'
  | 'Overdue'

export const ASSET_OPERATIONAL_STATUSES = [
  'Operational',
  'Under Maintenance',
  'Out of Service',
  'Quarantined',
  'Pending Disposal',
  'Retired'
] as const

export type AssetOperationalStatus = typeof ASSET_OPERATIONAL_STATUSES[number]

export type MaintenanceStatus =
  | 'Scheduled'
  | 'In Progress'
  | 'Completed'
  | 'Cancelled'

export interface MaintenanceRecordPayload {
  maintenanceDate: string
  status: MaintenanceStatus
  technicianName: string
  vendorName: string
  maintenanceType: string
  notes: string
  nextMaintenanceDate: string
}

export interface MaintenanceRecord extends MaintenanceRecordPayload {
  id: number
  assetId: number
  hospitalId: string
  createdAt: string
  updatedAt: string
}

export interface Asset {
  id: number
  assetId: string
  hospitalId: string
  name: string
  category: AssetCategory
  serialNumber: string
  manufacturer: string
  model: string
  departmentId: string
  locationId: number
  responsibleTeam: string
  condition: AssetCondition
  operationalStatus: AssetOperationalStatus
  lastMaintenanceDate: string
  nextMaintenanceDate: string
  purchaseDate: string
  warrantyExpiry: string
  vendorName: string
  serviceContact: string
  serviceEmail: string
  warrantyNotes: string
  description: string
  createdAt: string
  updatedAt: string
}

export interface AssetFormPayload {
  name: string
  category: AssetCategory
  serialNumber: string
  manufacturer: string
  model: string
  departmentId: string
  locationId: number
  responsibleTeam: string
  condition: AssetCondition
  operationalStatus: AssetOperationalStatus
  lastMaintenanceDate: string
  nextMaintenanceDate: string
  purchaseDate: string
  warrantyExpiry: string
  vendorName: string
  serviceContact: string
  serviceEmail: string
  warrantyNotes: string
  description: string
}

export interface AssetOperationalUpdatePayload {
  condition: AssetCondition
  operationalStatus: AssetOperationalStatus
}

export interface AssetMovePayload {
  departmentId: string
  locationId: number
  responsibleTeam: string
}
