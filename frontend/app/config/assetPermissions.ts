import type { UserRole } from '~/types/auth'
import type { Asset, AssetOperationalStatus } from '~/types/asset'

export type AssetPermission =
  | 'view'
  | 'create'
  | 'editMaster'
  | 'editOperational'
  | 'move'
  | 'manageDocuments'
  | 'manageMaintenance'

const ROLE_ASSET_PERMISSIONS: Record<UserRole, AssetPermission[]> = {
  admin: [
    'view',
    'create',
    'editMaster',
    'editOperational',
    'move',
    'manageDocuments',
    'manageMaintenance'
  ],
  biomedical: [
    'view',
    'editOperational',
    'move',
    'manageDocuments',
    'manageMaintenance'
  ],
  manager: [
    'view',
    'editOperational',
    'move',
    'manageMaintenance'
  ],
  nurse: ['view']
}

export const hasAssetPermission = (
  role: UserRole | null,
  permission: AssetPermission
) => {
  if (!role) return false
  return ROLE_ASSET_PERMISSIONS[role].includes(permission)
}

export const hasHospitalWideAssetView = (role: UserRole | null) =>
  role === 'admin' || role === 'biomedical'

export const canViewAssetInScope = (
  role: UserRole | null,
  userHospitalId: string | null | undefined,
  userDepartmentId: string | null | undefined,
  asset: Asset
) => {
  if (!role || !userHospitalId) return false
  if (asset.hospitalId !== userHospitalId) return false
  if (hasHospitalWideAssetView(role)) return true
  if (!userDepartmentId) return false
  return asset.departmentId === userDepartmentId
}

export type AssetAccessContext = {
  role: UserRole
  hospitalId: string
  departmentId: string | null
}

export const canMoveAssetInContext = (
  context: AssetAccessContext,
  asset: Asset,
  targetDepartmentId: string
) => {
  if (
    context.role !== 'admin' &&
    context.role !== 'biomedical' &&
    context.role !== 'manager'
  ) return false

  if (!canViewAssetInScope(
    context.role,
    context.hospitalId,
    context.departmentId,
    asset
  )) return false

  if (
    context.role === 'manager' &&
    targetDepartmentId !== asset.departmentId
  ) return false

  return true
}

export const getAllowedOperationalStatuses = (
  role: UserRole | null
): AssetOperationalStatus[] => {
  if (role === 'admin') {
    return [
      'Operational',
      'Under Maintenance',
      'Out of Service',
      'Quarantined',
      'Pending Disposal',
      'Retired'
    ]
  }

  if (role === 'biomedical') {
    return [
      'Operational',
      'Under Maintenance',
      'Out of Service',
      'Quarantined',
      'Pending Disposal'
    ]
  }

  if (role === 'manager') {
    return ['Operational', 'Under Maintenance', 'Out of Service']
  }

  return []
}

export const canChangeAssetDepartment = (role: UserRole | null) =>
  role === 'admin' || role === 'biomedical'
