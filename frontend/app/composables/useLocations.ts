import type {
  HospitalLocation,
  LocationFormPayload,
  LocationType
} from '~/types/location'

import { mockLocations } from '~/config/data/locations'
import { useDepartments } from '~/composables/useDepartments'
import { useMockPersistence } from '~/composables/useMockPersistence'
import { LOCATION_PARENT_TYPES } from '~/config/locationHierarchy'

type LocationOperationResult =
  | { ok: true; location: HospitalLocation }
  | { ok: false; message: string }

type LocationStatusResult =
  | { ok: true }
  | { ok: false; message: string }

export const useLocations = () => {
  const { getDepartmentById } = useDepartments()

  const locations = useMockPersistence<HospitalLocation[]>(
    'assetcare-locations',
    () => [...mockLocations],
    2
  )

  const getLocationById = (id: number | null | undefined) => {
    if (!id) return null

    return locations.value.find(location => location.id === id) ?? null
  }

  const getLocationPath = (locationId: number) => {
    const path: string[] = []
    let current = getLocationById(locationId)
    const visited = new Set<number>()

    while (current && !visited.has(current.id)) {
      visited.add(current.id)
      path.unshift(current.name)
      current = getLocationById(current.parentId)
    }

    return path.join(' → ')
  }

  const getDescendantIds = (locationId: number) => {
    const ids = new Set<number>()

    const collect = (parentId: number) => {
      const children = locations.value.filter(location => location.parentId === parentId)

      children.forEach(child => {
        if (ids.has(child.id)) return
        ids.add(child.id)
        collect(child.id)
      })
    }

    collect(locationId)
    return ids
  }

  const validateLocationHierarchy = (
    type: LocationType,
    parentId: number | null,
    hospitalId?: string,
    editingId?: number
  ): string | null => {
    if (type === 'Building') {
      if (parentId !== null) return 'A Building cannot have a parent location.'
      return null
    }

    if (parentId === null) return `${type} must have a parent location.`

    if (editingId !== undefined && parentId === editingId) {
      return 'A location cannot be its own parent.'
    }

    if (editingId !== undefined && getDescendantIds(editingId).has(parentId)) {
      return 'A location cannot be moved under one of its descendants.'
    }

    const parent = getLocationById(parentId)

    if (!parent) return 'The selected parent location does not exist.'

    if (hospitalId && parent.hospitalId !== hospitalId) {
      return 'The selected parent location does not belong to this hospital.'
    }

    if (parent.status !== 'Active') {
      return 'The selected parent location must be Active.'
    }

    const requiredParentType =
      LOCATION_PARENT_TYPES[type as Exclude<LocationType, 'Building'>]

    if (parent.type !== requiredParentType) {
      return `${type} must have a ${requiredParentType} as its parent.`
    }

    return null
  }

  const validateLocationDepartment = (
    departmentId: string | null,
    hospitalId: string
  ): string | null => {
    if (!departmentId) return null

    const department = getDepartmentById(departmentId)

    if (!department) return 'Selected department was not found.'
    if (department.hospitalId !== hospitalId) {
      return 'Selected department does not belong to this hospital.'
    }
    if (department.status !== 'Active') {
      return 'Selected department must be Active.'
    }

    return null
  }

  const createLocation = (
    payload: LocationFormPayload,
    hospitalId: string
  ): LocationOperationResult => {
    if (!payload.name.trim()) {
      return { ok: false, message: 'Location name is required.' }
    }

    const departmentError = validateLocationDepartment(payload.departmentId, hospitalId)
    if (departmentError) return { ok: false, message: departmentError }

    const validationError = validateLocationHierarchy(
      payload.type,
      payload.parentId,
      hospitalId
    )
    if (validationError) return { ok: false, message: validationError }

    const newLocation: HospitalLocation = {
      id: Date.now(),
      hospitalId,
      name: payload.name.trim(),
      type: payload.type,
      parentId: payload.parentId,
      departmentId: payload.departmentId,
      description: payload.description.trim(),
      status: 'Active'
    }

    locations.value.push(newLocation)
    return { ok: true, location: newLocation }
  }

  const updateLocation = (
    id: number,
    payload: LocationFormPayload
  ): LocationOperationResult => {
    const index = locations.value.findIndex(location => location.id === id)

    if (index === -1) return { ok: false, message: 'Location not found.' }

    const existing = locations.value[index]
    if (!existing) return { ok: false, message: 'Location not found.' }

    if (!payload.name.trim()) {
      return { ok: false, message: 'Location name is required.' }
    }

    const departmentError = validateLocationDepartment(
      payload.departmentId,
      existing.hospitalId
    )
    if (departmentError) return { ok: false, message: departmentError }

    const validationError = validateLocationHierarchy(
      payload.type,
      payload.parentId,
      existing.hospitalId,
      id
    )
    if (validationError) return { ok: false, message: validationError }

    const updatedLocation: HospitalLocation = {
      ...existing,
      name: payload.name.trim(),
      type: payload.type,
      parentId: payload.parentId,
      departmentId: payload.departmentId,
      description: payload.description.trim()
    }

    locations.value[index] = updatedLocation
    return { ok: true, location: updatedLocation }
  }

  const toggleLocationStatus = (id: number): LocationStatusResult => {
    const location = getLocationById(id)

    if (!location) return { ok: false, message: 'Location not found.' }

    if (location.status === 'Inactive') {
      const departmentError = validateLocationDepartment(
        location.departmentId,
        location.hospitalId
      )
      if (departmentError) return { ok: false, message: departmentError }

      const parent = getLocationById(location.parentId)
      if (parent && parent.status !== 'Active') {
        return {
          ok: false,
          message: 'A location cannot be activated while its parent is Inactive.'
        }
      }

      location.status = 'Active'
      return { ok: true }
    }

    const hasActiveDescendant = Array.from(getDescendantIds(location.id)).some(
      descendantId => getLocationById(descendantId)?.status === 'Active'
    )

    if (hasActiveDescendant) {
      return {
        ok: false,
        message: 'A location with active descendants cannot be deactivated.'
      }
    }

    location.status = 'Inactive'
    return { ok: true }
  }

  return {
    locations,
    getLocationById,
    getLocationPath,
    getDescendantIds,
    validateLocationHierarchy,
    createLocation,
    updateLocation,
    toggleLocationStatus
  }
}
