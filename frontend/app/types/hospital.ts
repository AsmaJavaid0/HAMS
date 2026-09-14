export type HospitalStatus =
  | 'Active'
  | 'Inactive'

export interface HospitalProfile {
  id: string

  name: string
  code: string

  registrationNumber: string

  email: string
  phone: string

  address: string
  suburb: string
  state: string
  postcode: string
  country: string

  timezone: string

  status: HospitalStatus
}

export interface HospitalFormPayload {
  name: string
  code: string

  registrationNumber: string

  email: string
  phone: string

  address: string
  suburb: string
  state: string
  postcode: string

  timezone: string

  status: HospitalStatus
}