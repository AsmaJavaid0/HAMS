import type {
  Department,
  DepartmentFormPayload
} from '~/types/department'
import { mockDepartments } from '~/config/data/departments'
import { mockStaff } from '~/config/data/staff'
import { useMockPersistence } from '~/composables/useMockPersistence'

type DepartmentOperationResult =
  | {
      ok: true
      department: Department
    }
  | {
      ok: false
      message: string
    }


export const useDepartments = () => {

  /*
  |--------------------------------------------------------------------------
  | SHARED DEPARTMENT STATE
  |--------------------------------------------------------------------------
  */

const departments = useMockPersistence<Department[]>(
  'assetcare-departments',
  () => [...mockDepartments],
  2
)

const staffMembers = useMockPersistence(
  'assetcare-staff',
  () => [...mockStaff],
  2
)


  /*
  |--------------------------------------------------------------------------
  | ACTIVE DEPARTMENTS
  |--------------------------------------------------------------------------
  */

  const activeDepartments =
    computed(() => {

      return departments.value.filter(
        department =>
          department.status ===
          'Active'
      )
    })


  /*
  |--------------------------------------------------------------------------
  | LOOKUP
  |--------------------------------------------------------------------------
  */

  const getDepartmentById = (
    id: string | null | undefined
  ) => {

    if (!id) {
      return null
    }

    return (
      departments.value.find(
        department =>
          department.id === id
      ) ?? null
    )
  }


  /*
  |--------------------------------------------------------------------------
  | VALIDATION
  |--------------------------------------------------------------------------
  */

  const validateDepartment = (
    payload: DepartmentFormPayload,
    hospitalId: string,
    editingId?: string
  ): string | null => {

    if (!payload.name.trim()) {
      return 'Department name is required.'
    }

    if (!payload.code.trim()) {
      return 'Department code is required.'
    }

    const normalizedName =
      payload.name
        .trim()
        .toLowerCase()


    const normalizedCode =
      payload.code
        .trim()
        .toLowerCase()


    const duplicateName =
      departments.value.find(
        department =>
          department.name
            .trim()
            .toLowerCase() ===
            normalizedName &&

          department.id !==
            editingId
      )


    if (duplicateName) {
      return (
        'A department with this name already exists.'
      )
    }


    const duplicateCode =
      departments.value.find(
        department =>
          department.code
            .trim()
            .toLowerCase() ===
            normalizedCode &&

          department.id !==
            editingId
      )


    if (duplicateCode) {
      return (
        'A department with this code already exists.'
      )
    }


    /*
     * One manager cannot manage
     * multiple departments.
     */

    if (payload.managerId) {

      const manager = staffMembers.value.find(
        staff => staff.id === payload.managerId
      )

      if (!manager) {
        return 'Selected manager was not found.'
      }

      if (
        manager.hospitalId !== hospitalId ||
        manager.status !== 'Active' ||
        manager.role !== 'manager'
      ) {
        return 'Selected manager must be an active manager from this hospital.'
      }

      const managerDepartment =
        departments.value.find(
          department =>
            department.managerId ===
              payload.managerId &&

            department.id !==
              editingId
        )


      if (managerDepartment) {

        return (
          `This manager is already assigned to ${managerDepartment.name}.`
        )
      }
    }


    return null
  }


  /*
  |--------------------------------------------------------------------------
  | CREATE
  |--------------------------------------------------------------------------
  */
const createDepartment = (
  payload: DepartmentFormPayload,
  hospitalId: string
): DepartmentOperationResult => {

    const validationError =
      validateDepartment(
        payload,
        hospitalId
      )


    if (validationError) {

      return {
        ok: false,
        message:
          validationError
      }
    }


    const newDepartment: Department = {
      id: `dept-${Date.now()}`,

  hospitalId,

  name: payload.name.trim(),

  code: payload.code.trim().toUpperCase(),

  managerId: payload.managerId,

  status: 'Active',

  description: payload.description.trim()
}


    departments.value.push(
      newDepartment
    )


    return {
      ok: true,

      department:
        newDepartment
    }
  }


  /*
  |--------------------------------------------------------------------------
  | UPDATE
  |--------------------------------------------------------------------------
  */

  const updateDepartment = (
    id: string,
    payload: DepartmentFormPayload
  ): DepartmentOperationResult => {

    const index =
      departments.value.findIndex(
        department =>
          department.id === id
      )


    if (index === -1) {

      return {
        ok: false,

        message:
          'Department was not found.'
      }
    }

    const existingDepartment =
      departments.value[index]

    if (!existingDepartment) {
      return {
        ok: false,
        message:
          'Department was not found.'
      }
    }


    const validationError =
      validateDepartment(
        payload,
        existingDepartment.hospitalId,
        id
      )


    if (validationError) {

      return {
        ok: false,

        message:
          validationError
      }
    }


    const existing =
      departments.value[index]


    if (!existing) {

      return {
        ok: false,

        message:
          'Department was not found.'
      }
    }


    const updatedDepartment:
      Department = {

      ...existing,

      name:
        payload.name.trim(),

      code:
        payload.code
          .trim()
          .toUpperCase(),

      managerId:
        payload.managerId,

      description:
        payload.description.trim()
    }


    departments.value[index] =
      updatedDepartment


    return {
      ok: true,

      department:
        updatedDepartment
    }
  }


  /*
  |--------------------------------------------------------------------------
  | STATUS
  |--------------------------------------------------------------------------
  */

  const toggleDepartmentStatus = (
    id: string
  ) => {

    const department =
      getDepartmentById(id)


    if (!department) {
      return false
    }


    department.status =
      department.status ===
        'Active'
        ? 'Inactive'
        : 'Active'


    return true
  }


  return {
    departments,
    activeDepartments,

    getDepartmentById,

    createDepartment,
    updateDepartment,

    toggleDepartmentStatus
  }
}