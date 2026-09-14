export type LocationType =
  | 'Building'
  | 'Floor'
  | 'Ward'
  | 'Room'
  | 'Sub-location'

export type LocationStatus =
  | 'Active'
  | 'Inactive'

export interface HospitalLocation {
  id: number

  name: string
 hospitalId: string
  type: LocationType

  parentId: number | null

  departmentId: string | null

  status: LocationStatus

  description?: string
}

export interface LocationFormPayload {
  name: string

  type: LocationType

  parentId: number | null

  departmentId: string | null

  description: string
}