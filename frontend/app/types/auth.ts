export type UserRole =
  | 'admin'
  | 'manager'
  | 'biomedical'
  | 'nurse'

export type AccessScope =
  | 'hospital'
  | 'department'

export interface User {
  id: string
  name: string
  email: string
  role: UserRole

  hospital_id: string
  hospital_name?: string

  department_id?: string | null
  department_name?: string | null

  scope: AccessScope
}

export interface LoginResponse {
  token: string
  user: User
}

export type RegisterPayload = {
  name: string
  email: string
  password: string
  role: UserRole
}