export type DepartmentStatus =
  | 'Active'
  | 'Inactive'


export interface Department {
  id: string
  hospitalId: string
  name: string
  code: string

  managerId: number | null

  status: DepartmentStatus

  description?: string
}


export interface DepartmentFormPayload {
  name: string
  code: string

  managerId: number | null

  description: string
}