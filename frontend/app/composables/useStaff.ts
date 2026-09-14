import type {
  AccessScope,
  UserRole
} from '~/types/auth'
import { mockStaff } from '~/config/data/staff'
import { useDepartments } from '~/composables/useDepartments'
import { useMockPersistence } from '~/composables/useMockPersistence'
import type {
  StaffFormPayload,
  StaffMember,
  StaffStatus
} from '~/types/staff'


type StaffOperationResult =
  | {
      ok: true
      staff: StaffMember
    }
  | {
      ok: false
      message: string
    }


export const useStaff = () => {
  const { getDepartmentById } = useDepartments()

  /*
  |--------------------------------------------------------------------------
  | SHARED STAFF STATE
  |--------------------------------------------------------------------------
  */

  const staffMembers = useMockPersistence<StaffMember[]>(
  'assetcare-staff',
  () => [...mockStaff],
  2
)


  /*
  |--------------------------------------------------------------------------
  | ROLE → ACCESS SCOPE
  |--------------------------------------------------------------------------
  |
  | Current frontend policy:
  |
  | Admin       = whole hospital
  | Biomedical  = hospital/equipment scope
  | Manager     = assigned department
  | Nurse       = assigned department
  |
  */

  const getScopeForRole = (
    role: UserRole
  ): AccessScope => {

    if (
      role === 'admin' ||
      role === 'biomedical'
    ) {
      return 'hospital'
    }

    return 'department'
  }


  /*
  |--------------------------------------------------------------------------
  | LOOKUPS
  |--------------------------------------------------------------------------
  */

  const getStaffById = (
    id: number
  ) => {

    return (
      staffMembers.value.find(
        staff =>
          staff.id === id
      ) ?? null
    )
  }


  const getStaffByEmail = (
    email: string
  ) => {

    const normalized =
      email
        .trim()
        .toLowerCase()

    return (
      staffMembers.value.find(
        staff =>
          staff.email
            .toLowerCase() ===
          normalized
      ) ?? null
    )
  }


  /*
  |--------------------------------------------------------------------------
  | VALIDATION
  |--------------------------------------------------------------------------
  */

  const validateStaffPayload = (
    payload: StaffFormPayload,
    actorRole: UserRole,
    hospitalId: string,
    editingId?: number
  ): string | null => {

    /*
     * Manager can never create/elevate
     * somebody to Admin.
     */

    if (
      actorRole !== 'admin' &&
      payload.role === 'admin'
    ) {
      return (
        'Only a Hospital Administrator can assign the Admin role.'
      )
    }


    /*
     * Non-admin staff require department.
     */

    if (
      payload.role !== 'admin' &&
      !payload.departmentId
    ) {
      return (
        'A department is required for this role.'
      )
    }

    if (payload.departmentId) {
      const department = getDepartmentById(payload.departmentId)

      if (!department) {
        return 'Selected department was not found.'
      }

      if (department.hospitalId !== hospitalId) {
        return 'Selected department does not belong to this hospital.'
      }

      if (department.status !== 'Active') {
        return 'Selected department must be Active.'
      }
    }

    if (!payload.name.trim()) {
      return 'Staff member name is required.'
    }

    if (!payload.email.trim()) {
      return 'Email is required.'
    }

    if (!payload.employeeId.trim()) {
      return 'Employee ID is required.'
    }


    /*
     * Email must be unique.
     */

    const emailOwner =
      staffMembers.value.find(
        staff =>
          staff.email
            .toLowerCase() ===
            payload.email
              .trim()
              .toLowerCase() &&

          staff.id !== editingId
      )

    if (emailOwner) {
      return (
        'A staff member with this email already exists.'
      )
    }


    /*
     * Employee ID must be unique.
     */

    const employeeIdOwner =
      staffMembers.value.find(
        staff =>
          staff.employeeId
            .toLowerCase() ===
            payload.employeeId
              .trim()
              .toLowerCase() &&

          staff.id !== editingId
      )

    if (employeeIdOwner) {
      return (
        'A staff member with this employee ID already exists.'
      )
    }


    return null
  }


  /*
  |--------------------------------------------------------------------------
  | CREATE
  |--------------------------------------------------------------------------
  */

const createStaff = (
  payload: StaffFormPayload,
  actorRole: UserRole,
  hospitalId: string
): StaffOperationResult => {

    const validationError =
      validateStaffPayload(
        payload,
        actorRole,
        hospitalId
      )

    if (validationError) {
      return {
        ok: false,
        message: validationError
      }
    }


    const newStaff:
      StaffMember = {

      id: Date.now(),
 hospitalId,
      name:
        payload.name.trim(),

      email:
        payload.email
          .trim()
          .toLowerCase(),

      employeeId:
        payload.employeeId
          .trim()
          .toUpperCase(),

      phone:
        payload.phone.trim(),

      role:
        payload.role,

      departmentId:
        payload.role === 'admin'
          ? null
          : payload.departmentId,

      accessScope:
        getScopeForRole(
          payload.role
        ),

      status:
        payload.status
    }


    staffMembers.value.push(
      newStaff
    )


    return {
      ok: true,
      staff: newStaff
    }
  }


  /*
  |--------------------------------------------------------------------------
  | UPDATE
  |--------------------------------------------------------------------------
  */

  const updateStaff = (
    id: number,
    payload: StaffFormPayload,
    actorRole: UserRole
  ): StaffOperationResult => {

    const index =
      staffMembers.value.findIndex(
        staff =>
          staff.id === id
      )


    if (index === -1) {
      return {
        ok: false,
        message:
          'Staff member was not found.'
      }
    }

    const existingStaff =
      staffMembers.value[index]

    if (!existingStaff) {
      return {
        ok: false,
        message:
          'Staff member was not found.'
      }
    }


    const validationError =
      validateStaffPayload(
        payload,
        actorRole,
        existingStaff.hospitalId,
        id
      )


    if (validationError) {
      return {
        ok: false,
        message: validationError
      }
    }


    const updatedStaff:
      StaffMember = {

      ...existingStaff,

      name:
        payload.name.trim(),

      email:
        payload.email
          .trim()
          .toLowerCase(),

      employeeId:
        payload.employeeId
          .trim()
          .toUpperCase(),

      phone:
        payload.phone.trim(),

      role:
        payload.role,

      departmentId:
        payload.role === 'admin'
          ? null
          : payload.departmentId,

      accessScope:
        getScopeForRole(
          payload.role
        ),

      status:
        payload.status
    }


    staffMembers.value[index] =
      updatedStaff


    return {
      ok: true,
      staff: updatedStaff
    }
  }


  /*
  |--------------------------------------------------------------------------
  | STATUS
  |--------------------------------------------------------------------------
  */

/*
|--------------------------------------------------------------------------
| ASSIGN DEPARTMENT
|--------------------------------------------------------------------------
*/

const setStaffDepartment = (
  id: number,
  departmentId: string | null
) => {

  const staff =
    getStaffById(id)


  if (!staff) {
    return false
  }


  if (staff.role === 'admin') {
    return false
  }

  if (departmentId) {
    const department = getDepartmentById(departmentId)

    if (
      !department ||
      department.hospitalId !== staff.hospitalId ||
      department.status !== 'Active'
    ) {
      return false
    }
  }


  staff.departmentId =
    departmentId


  return true
}

  const setStaffStatus = (
    id: number,
    status: StaffStatus
  ) => {

    const staff =
      getStaffById(id)

    if (!staff) {
      return false
    }

    staff.status = status

    if (status !== 'Active') {
      const { departments } = useDepartments()

      departments.value.forEach(department => {
        if (department.managerId === staff.id) {
          department.managerId = null
        }
      })
    }

    return true
  }


  return {
    staffMembers,

    getScopeForRole,

    getStaffById,
    getStaffByEmail,

    createStaff,
    updateStaff,

    setStaffStatus,
    setStaffDepartment
  }
}

