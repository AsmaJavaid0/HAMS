import type {
  AccessScope,
  UserRole
} from '~/types/auth'

export type StaffStatus =
  | 'Active'
  | 'Suspended'
  | 'Inactive'

export interface StaffMember {
  id: number
  hospitalId: string
  name: string
  email: string

  employeeId: string
  phone: string

  role: UserRole

  departmentId: string | null

  accessScope: AccessScope

  status: StaffStatus
}

export interface StaffFormPayload {
  name: string
  email: string

  employeeId: string
  phone: string

  role: UserRole

  departmentId: string | null

  status: StaffStatus
}