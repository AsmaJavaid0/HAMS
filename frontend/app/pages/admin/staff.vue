<script setup lang="ts">
import { useOperationFeedback } from '~/composables/useOperationFeedback'
import StaffForm
  from '~/components/Forms/StaffForm.vue'

import type {
  UserRole
} from '~/types/auth'

import {
  getShortRoleLabel
} from '~/config/permissions'

import type {
  StaffFormPayload,
  StaffMember,
  StaffStatus
} from '~/types/staff'


definePageMeta({
  layout: 'dashboard'
})


const {
  user,
  userRole
} = useAuth()

const {
  addAuditEvent
} = useAuditLog()


const {
  departments,
  getDepartmentById
} = useDepartments()


const {
  staffMembers,

  createStaff,
  updateStaff,

  setStaffStatus
} = useStaff()


/*
|--------------------------------------------------------------------------
| CURRENT USER
|--------------------------------------------------------------------------
*/

const currentUserRole =
  computed<UserRole>(
    () =>
      userRole.value ??
      'nurse'
  )


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const searchQuery =
  ref('')

const roleFilter =
  ref<'All' | UserRole>(
    'All'
  )

const statusFilter =
  ref<
    'All' |
    StaffStatus
  >('All')


const showStaffForm =
  ref(false)

const editingStaff =
  ref<StaffMember | null>(
    null
  )

const {
  operationError,
  successMessage,
  clearFeedback,
  setError,
  setSuccess
} = useOperationFeedback()


/*
|--------------------------------------------------------------------------
| ROLE LABEL
|--------------------------------------------------------------------------
*/


/*
|--------------------------------------------------------------------------
| EFFECTIVE ACCESS
|--------------------------------------------------------------------------
*/

const getEffectiveAccess = (
  staff: StaffMember
) => {

  if (
    staff.role === 'admin'
  ) {
    return 'Whole Hospital'
  }


  if (
    staff.role ===
    'biomedical'
  ) {
    return (
      'Hospital-wide Biomedical'
    )
  }


  const department =
    getDepartmentById(
      staff.departmentId
    )


  if (!department) {
    return (
      'Department not assigned'
    )
  }


  return (
    `${department.name} only`
  )
}


/*
|--------------------------------------------------------------------------
| FILTER
|--------------------------------------------------------------------------
*/

const filteredStaff =
  computed(() => {

    const query =
      searchQuery.value
        .trim()
        .toLowerCase()


    return staffMembers.value.filter(
      staff => {

        const department =
          getDepartmentById(
            staff.departmentId
          )


        const matchesSearch =
          !query ||

          staff.name
            .toLowerCase()
            .includes(query) ||

          staff.email
            .toLowerCase()
            .includes(query) ||

          staff.employeeId
            .toLowerCase()
            .includes(query) ||

          getShortRoleLabel(
            staff.role
          )
            .toLowerCase()
            .includes(query) ||

          (
            department?.name
              .toLowerCase()
              .includes(query)
            ?? false
          )


        const matchesRole =
          roleFilter.value ===
            'All' ||

          staff.role ===
            roleFilter.value


        const matchesStatus =
          statusFilter.value ===
            'All' ||

          staff.status ===
            statusFilter.value


        return (
          matchesSearch &&
          matchesRole &&
          matchesStatus
        )
      }
    )
  })


/*
|--------------------------------------------------------------------------
| SUMMARY
|--------------------------------------------------------------------------
*/

const activeCount =
  computed(() =>
    staffMembers.value.filter(
      staff =>
        staff.status ===
        'Active'
    ).length
  )


const suspendedCount =
  computed(() =>
    staffMembers.value.filter(
      staff =>
        staff.status ===
        'Suspended'
    ).length
  )


const managerCount =
  computed(() =>
    staffMembers.value.filter(
      staff =>
        staff.role ===
        'manager'
    ).length
  )


/*
|--------------------------------------------------------------------------
| FORM
|--------------------------------------------------------------------------
*/

const openAddStaff = () => {

  clearFeedback()

  editingStaff.value =
    null

  showStaffForm.value =
    true
}


const openEditStaff = (
  staff: StaffMember
) => {

  clearFeedback()

  editingStaff.value = {
    ...staff
  }

  showStaffForm.value =
    true
}


const closeStaffForm = () => {

  showStaffForm.value =
    false

  editingStaff.value =
    null
}


/*
|--------------------------------------------------------------------------
| SAVE
|--------------------------------------------------------------------------
*/

const saveStaff = (
  payload: StaffFormPayload
) => {

  clearFeedback()


  const result =
    editingStaff.value

      ? updateStaff(
          editingStaff.value.id,
          payload,
          currentUserRole.value
        )

      : createStaff(
  payload,
  currentUserRole.value,
  user.value!.hospital_id
)


  if (!result.ok) {

    setError(
      result.message
    )

    return
  }


  const wasEditing =
    Boolean(
      editingStaff.value
    )


  if (user.value) {

    addAuditEvent({

      action:
        wasEditing
          ? 'Updated'
          : 'Created',

      entityType:
        'Staff',
hospitalId:
  user.value.hospital_id,
      entityId:
        result.staff.id,

      entityName:
        result.staff.name,

      actorId:
        user.value.id,

      actorName:
        user.value.name,

      description:
        wasEditing
          ? `updated staff member ${result.staff.name}.`
          : `added staff member ${result.staff.name}.`
    })
  }


  setSuccess(
    editingStaff.value

      ? `${result.staff.name} was updated successfully.`

      : `${result.staff.name} was added successfully.`
  )


  closeStaffForm()
}


/*
|--------------------------------------------------------------------------
| STATUS
|--------------------------------------------------------------------------
*/

const updateStatus = (
  staff: StaffMember,
  status: StaffStatus
) => {

  clearFeedback()


  /*
   * Avoid modifying own demo account.
   */

  if (
    staff.email ===
    user.value?.email
  ) {

    setError(
      'You cannot suspend or deactivate your own account from this screen.'
    )

    return
  }


  const action =
    status === 'Active'
      ? 'activate'
      : status === 'Suspended'
        ? 'suspend'
        : 'deactivate'


  const confirmed =
    window.confirm(
      `Are you sure you want to ${action} "${staff.name}"?`
    )


  if (!confirmed) {
    return
  }


  setStaffStatus(
    staff.id,
    status
  )


  if (user.value) {

    addAuditEvent({

      action:
        status === 'Suspended'
          ? 'Suspended'
          : status === 'Inactive'
            ? 'Deactivated'
            : 'Activated',

      entityType:
        'Staff',

      entityId:
        staff.id,

      entityName:
        staff.name,
hospitalId:
  user.value.hospital_id,
      actorId:
        user.value.id,

      actorName:
        user.value.name,

      description:
        `${status === 'Suspended'
          ? 'suspended'
          : status === 'Inactive'
            ? 'deactivated'
            : 'activated'} staff member ${staff.name}.`
    })
  }


  setSuccess(
    `${staff.name} is now ${status.toLowerCase()}.`
  )
}

</script>


<template>

  <div class="space-y-6">

    <!-- Header -->

    <div
      class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >

      <div>

        <h1
          class="text-2xl font-bold text-text-primary"
        >
          Staff
        </h1>

        <p
          class="mt-1 text-sm text-text-secondary"
        >
          Manage hospital staff, roles, department assignments and account access.
        </p>

      </div>


      <button
        type="button"
        class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
        @click="openAddStaff"
      >
        + Add Staff
      </button>

    </div>


    <!-- Messages -->

    <CommonFeedbackAlert
      :message="operationError"
      type="error"
    />

    <CommonFeedbackAlert
      :message="successMessage"
      type="success"
    />


    <!-- Summary -->

    <div
      class="grid grid-cols-2 gap-3 lg:grid-cols-4"
    >

      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >
        <p class="text-xs font-medium uppercase tracking-wide text-gray-400">
          Total Staff
        </p>

        <p class="mt-2 text-2xl font-bold text-text-primary">
          {{ staffMembers.length }}
        </p>
      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >
        <p class="text-xs font-medium uppercase tracking-wide text-gray-400">
          Active
        </p>

        <p class="mt-2 text-2xl font-bold text-green-600">
          {{ activeCount }}
        </p>
      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >
        <p class="text-xs font-medium uppercase tracking-wide text-gray-400">
          Suspended
        </p>

        <p class="mt-2 text-2xl font-bold text-yellow-600">
          {{ suspendedCount }}
        </p>
      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >
        <p class="text-xs font-medium uppercase tracking-wide text-gray-400">
          Managers
        </p>

        <p class="mt-2 text-2xl font-bold text-primary">
          {{ managerCount }}
        </p>
      </div>

    </div>


    <!-- Search -->

    <div
      class="flex flex-col gap-3 rounded-xl border border-gray-200 bg-white p-4 lg:flex-row"
    >

      <div class="relative flex-1">

        <span
          class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
        >
          ⌕
        </span>

        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search staff..."
          class="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-9 pr-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
        />

      </div>


      <select
        v-model="roleFilter"
        class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-primary"
      >

        <option value="All">
          All Roles
        </option>

        <option value="admin">
          Admin
        </option>

        <option value="manager">
          Manager
        </option>

        <option value="biomedical">
          Biomedical
        </option>

        <option value="nurse">
          Nurse
        </option>

      </select>


      <select
        v-model="statusFilter"
        class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-primary"
      >

        <option value="All">
          All Status
        </option>

        <option value="Active">
          Active
        </option>

        <option value="Suspended">
          Suspended
        </option>

        <option value="Inactive">
          Inactive
        </option>

      </select>

    </div>


    <!-- Table -->

    <div
      v-if="filteredStaff.length"
      class="overflow-hidden rounded-xl border border-gray-200 bg-white"
    >

      <div class="overflow-x-auto">

        <table
          class="min-w-[1150px] w-full"
        >

          <thead
            class="border-b border-gray-200 bg-gray-50"
          >

            <tr>

              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                Staff Member
              </th>

              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                Employee ID
              </th>

              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                Role
              </th>

              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                Department
              </th>

              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                Effective Access
              </th>

              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
                Status
              </th>

              <th class="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">
                Actions
              </th>

            </tr>

          </thead>


          <tbody
            class="divide-y divide-gray-100"
          >

            <tr
              v-for="staff in filteredStaff"
              :key="staff.id"
              class="hover:bg-gray-50"
            >

              <td class="px-6 py-4">

                <p
                  class="font-medium text-text-primary"
                >
                  {{ staff.name }}
                </p>

                <p
                  class="mt-1 text-xs text-gray-500"
                >
                  {{ staff.email }}
                </p>

              </td>


              <td
                class="px-6 py-4 text-sm text-gray-600"
              >
                {{ staff.employeeId }}
              </td>


              <td class="px-6 py-4">

                <span
                  class="rounded-md bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700"
                >
                  {{ getShortRoleLabel(staff.role) }}
                </span>

              </td>


              <td
                class="px-6 py-4 text-sm text-gray-600"
              >
                {{
                  getDepartmentById(
                    staff.departmentId
                  )?.name ||
                  'Whole Hospital'
                }}
              </td>


              <td
                class="px-6 py-4 text-sm text-gray-600"
              >
                {{ getEffectiveAccess(staff) }}
              </td>


              <td class="px-6 py-4">

                <CommonStatusBadge
                  v-if="staff.status === 'Active'"
                  label="Active"
                  tone="success"
                />

                <CommonStatusBadge
                  v-else-if="staff.status === 'Suspended'"
                  label="Suspended"
                  tone="warning"
                />

                <CommonStatusBadge
                  v-else
                  label="Inactive"
                  tone="neutral"
                />

              </td>


              <td class="px-6 py-4">

                <div
                  class="flex items-center justify-end gap-2"
                >

                  <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                    @click="openEditStaff(staff)"
                  >
                    Edit
                  </button>


                  <button
                    v-if="staff.status === 'Active'"
                    type="button"
                    class="rounded-lg border border-yellow-200 px-3 py-1.5 text-xs font-medium text-yellow-700 hover:bg-yellow-50"
                    @click="updateStatus(staff, 'Suspended')"
                  >
                    Suspend
                  </button>


                  <button
                    v-if="staff.status !== 'Active'"
                    type="button"
                    class="rounded-lg border border-green-200 px-3 py-1.5 text-xs font-medium text-green-700 hover:bg-green-50"
                    @click="updateStatus(staff, 'Active')"
                  >
                    Activate
                  </button>


                  <button
                    v-if="staff.status !== 'Inactive'"
                    type="button"
                    class="rounded-lg border border-red-200 px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-50"
                    @click="updateStatus(staff, 'Inactive')"
                  >
                    Deactivate
                  </button>

                </div>

              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </div>


    <!-- Empty -->

    <div
      v-else
      class="flex min-h-[320px] flex-col items-center justify-center rounded-xl border border-gray-200 bg-white px-6 text-center"
    >

      <div
        class="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-2xl text-primary"
      >
        ♙
      </div>

      <h2
        class="mt-4 text-lg font-semibold text-text-primary"
      >
        No staff found
      </h2>

      <p
        class="mt-2 text-sm text-text-secondary"
      >
        Try changing your search or filter criteria.
      </p>

    </div>


    <StaffForm
      v-if="showStaffForm"
      :staff="editingStaff"
      :departments="departments"
      :current-user-role="currentUserRole"
      @close="closeStaffForm"
      @save="saveStaff"
    />

  </div>

</template>