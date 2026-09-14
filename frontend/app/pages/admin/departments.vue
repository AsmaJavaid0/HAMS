<script setup lang="ts">
import { useOperationFeedback } from '~/composables/useOperationFeedback'
import DepartmentForm from '~/components/Forms/DepartmentForm.vue'
import DepartmentDetail from '~/components/departments/DepartmentDetail.vue'
import type { Department, DepartmentFormPayload } from '~/types/department'

definePageMeta({ layout: 'dashboard' })

const { departments, createDepartment, updateDepartment, toggleDepartmentStatus } = useDepartments()
const { staffMembers, getStaffById, setStaffDepartment } = useStaff()
const { locations } = useLocations()
const { user } = useAuth()
const { addAuditEvent } = useAuditLog()

const searchQuery = ref('')
const statusFilter = ref<'All' | 'Active' | 'Inactive'>('All')
const showDepartmentForm = ref(false)
const editingDepartment = ref<Department | null>(null)
const selectedDepartment = ref<Department | null>(null)

const { operationError, successMessage, clearFeedback, setError, setSuccess } = useOperationFeedback()

const managers = computed(() => staffMembers.value.filter(staff => staff.role === 'manager'))

const filteredDepartments = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return departments.value.filter(department => {
    const manager = getStaffById(department.managerId ?? -1)
    const matchesSearch =
      !query ||
      department.name.toLowerCase().includes(query) ||
      department.code.toLowerCase().includes(query) ||
      (manager?.name.toLowerCase().includes(query) ?? false)

    const matchesStatus =
      statusFilter.value === 'All' || department.status === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

const getDepartmentStaffCount = (departmentId: string) =>
  staffMembers.value.filter(staff => staff.departmentId === departmentId).length

const getDepartmentLocations = (departmentId: string) =>
  locations.value.filter(location => location.departmentId === departmentId)

const getLocationDepth = (locationId: number) => {
  let depth = 0
  let current = locations.value.find(location => location.id === locationId)

  while (current?.parentId !== null && current?.parentId !== undefined) {
    depth += 1
    current = locations.value.find(location => location.id === current?.parentId)
  }

  return depth
}

const getDepartmentLocationSummary = (departmentId: string) => {
  const departmentLocations = getDepartmentLocations(departmentId)

  return departmentLocations
    .slice()
    .sort((a, b) => {
      const depthDifference = getLocationDepth(a.id) - getLocationDepth(b.id)
      if (depthDifference !== 0) return depthDifference
      return a.id - b.id
    })
}

const openAddDepartment = () => {
  clearFeedback()
  editingDepartment.value = null
  showDepartmentForm.value = true
}

const openEditDepartment = (department: Department) => {
  clearFeedback()
  editingDepartment.value = { ...department }
  showDepartmentForm.value = true
}

const closeDepartmentForm = () => {
  showDepartmentForm.value = false
  editingDepartment.value = null
}

const openDepartmentDetail = (department: Department) => {
  selectedDepartment.value = department
}

const closeDepartmentDetail = () => {
  selectedDepartment.value = null
}

const saveDepartment = (payload: DepartmentFormPayload) => {
  clearFeedback()

  if (!user.value?.hospital_id) {
    setError('Unable to determine the hospital.')
    return
  }

  const result = editingDepartment.value
    ? updateDepartment(editingDepartment.value.id, payload)
    : createDepartment(payload, user.value.hospital_id)

  if (!result.ok) {
    setError(result.message)
    return
  }

  const department = result.department

  if (department.managerId) {
    setStaffDepartment(department.managerId, department.id)
  }

  setSuccess(
    editingDepartment.value
      ? `${department.name} was updated successfully.`
      : `${department.name} was created successfully.`
  )

  if (user.value) {
    addAuditEvent({
      action: editingDepartment.value ? 'Updated' : 'Created',
      entityType: 'Department',
      hospitalId: user.value.hospital_id,
      entityId: department.id,
      entityName: department.name,
      actorId: user.value.id,
      actorName: user.value.name,
      description: editingDepartment.value
        ? `updated department ${department.name}.`
        : `created department ${department.name}.`
    })
  }

  closeDepartmentForm()
}

const changeDepartmentStatus = (department: Department) => {
  clearFeedback()

  const isDeactivating = department.status === 'Active'
  const action = isDeactivating ? 'deactivate' : 'activate'

  if (!window.confirm(`Are you sure you want to ${action} "${department.name}"?`)) return

  toggleDepartmentStatus(department.id)

  if (isDeactivating) {
    locations.value.forEach(location => {
      if (location.departmentId !== department.id) return

      location.status = 'Inactive'

      if (user.value) {
        addAuditEvent({
          action: 'Deactivated',
          entityType: 'Location',
          hospitalId: user.value.hospital_id,
          entityId: location.id,
          entityName: location.name,
          actorId: user.value.id,
          actorName: user.value.name,
          description: `automatically deactivated location ${location.name} because department ${department.name} was deactivated.`
        })
      }
    })
  }

  setSuccess(
    isDeactivating
      ? `${department.name} is now inactive. All associated locations have also been deactivated.`
      : `${department.name} is now active.`
  )

  if (user.value) {
    addAuditEvent({
      action: department.status === 'Active' ? 'Activated' : 'Deactivated',
      entityType: 'Department',
      entityId: department.id,
      entityName: department.name,
      hospitalId: user.value.hospital_id,
      actorId: user.value.id,
      actorName: user.value.name,
      description: `${department.status === 'Active' ? 'activated' : 'deactivated'} department ${department.name}.`
    })
  }
}

const selectedManager = computed(() => {
  if (!selectedDepartment.value?.managerId) return null
  return getStaffById(selectedDepartment.value.managerId)
})

const selectedDepartmentStaff = computed(() => {
  if (!selectedDepartment.value) return []
  return staffMembers.value.filter(staff => staff.departmentId === selectedDepartment.value?.id)
})

const selectedDepartmentLocations = computed(() => {
  if (!selectedDepartment.value) return []
  return locations.value.filter(location => location.departmentId === selectedDepartment.value?.id)
})
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-text-primary">Departments</h1>
        <p class="mt-1 text-sm text-text-secondary">
          Manage hospital departments, managers, staff and associated locations.
        </p>
      </div>

      <CommonBaseButton @click="openAddDepartment">
        + Add Department
      </CommonBaseButton>
    </div>

    <CommonFeedbackAlert :message="operationError" type="error" />
    <CommonFeedbackAlert :message="successMessage" type="success" />

    <div class="flex flex-col gap-3 rounded-xl border border-gray-200 bg-white p-4 sm:flex-row">
      <div class="relative flex-1">
        <span class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">⌕</span>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search departments..."
          class="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-9 pr-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
        />
      </div>

      <select
        v-model="statusFilter"
        class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-primary"
      >
        <option value="All">All Status</option>
        <option value="Active">Active</option>
        <option value="Inactive">Inactive</option>
      </select>
    </div>

    <div v-if="filteredDepartments.length" class="overflow-hidden rounded-xl border border-gray-200 bg-white">
      <div class="overflow-x-auto">
        <table class="min-w-[1120px] w-full">
          <thead class="border-b border-gray-200 bg-gray-50">
            <tr>
              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Department</th>
              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Manager</th>
              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Staff</th>
              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Locations</th>
              <th class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">Status</th>
              <th class="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">Actions</th>
            </tr>
          </thead>

          <tbody class="divide-y divide-gray-100">
            <tr
              v-for="department in filteredDepartments"
              :key="department.id"
              class="align-top hover:bg-gray-50"
            >
              <td class="px-6 py-4">
                <p class="font-medium text-text-primary">{{ department.name }}</p>
                <span class="mt-1 inline-block rounded-md bg-gray-100 px-2 py-0.5 text-xs font-medium text-gray-600">
                  {{ department.code }}
                </span>
              </td>

              <td class="px-6 py-4 text-sm text-gray-600">
                {{ getStaffById(department.managerId ?? -1)?.name || 'Unassigned' }}
              </td>

              <td class="px-6 py-4 text-sm text-gray-600">
                {{ getDepartmentStaffCount(department.id) }}
              </td>

              <td class="px-6 py-4">
                <div class="space-y-1.5">
                  <p class="text-sm font-semibold text-text-primary">
                    {{ getDepartmentLocations(department.id).length }} locations
                  </p>

                  <div v-if="getDepartmentLocations(department.id).length" class="space-y-1 text-xs text-gray-500">
                    <div
                      v-for="location in getDepartmentLocationSummary(department.id)"
                      :key="location.id"
                      class="flex items-start gap-1.5"
                    >
                      <span class="mt-0.5 shrink-0 text-gray-300">•</span>
                      <span :class="getLocationDepth(location.id) > 0 ? 'pl-1' : 'font-medium text-gray-600'">
                        {{ location.name }}
                      </span>
                    </div>
                  </div>
                </div>
              </td>

              <td class="px-6 py-4">
                <CommonStatusBadge
                  :label="department.status"
                  :tone="department.status === 'Active' ? 'success' : 'neutral'"
                />
              </td>

              <td class="px-6 py-4">
                <div class="flex items-center justify-end gap-2">
                  <button
                    type="button"
                    class="rounded-lg border border-blue-200 px-3 py-1.5 text-xs font-medium text-primary hover:bg-blue-50"
                    @click="openDepartmentDetail(department)"
                  >
                    View
                  </button>

                  <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                    @click="openEditDepartment(department)"
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    class="rounded-lg border px-3 py-1.5 text-xs font-medium"
                    :class="department.status === 'Active'
                      ? 'border-red-200 text-red-600 hover:bg-red-50'
                      : 'border-green-200 text-green-600 hover:bg-green-50'"
                    @click="changeDepartmentStatus(department)"
                  >
                    {{ department.status === 'Active' ? 'Deactivate' : 'Activate' }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else class="flex min-h-[320px] flex-col items-center justify-center rounded-xl border border-gray-200 bg-white px-6 text-center">
      <div class="flex h-14 w-14 items-center justify-center rounded-full bg-primary/10 text-2xl text-primary">▤</div>
      <h2 class="mt-4 text-lg font-semibold text-text-primary">No departments found</h2>
      <p class="mt-2 text-sm text-text-secondary">Try changing your search or filter criteria.</p>
    </div>

    <DepartmentForm
      v-if="showDepartmentForm"
      :department="editingDepartment"
      :managers="managers"
      @close="closeDepartmentForm"
      @save="saveDepartment"
    />

    <DepartmentDetail
      v-if="selectedDepartment"
      :department="selectedDepartment"
      :manager="selectedManager"
      :staff="selectedDepartmentStaff"
      :locations="selectedDepartmentLocations"
      @close="closeDepartmentDetail"
    />
  </div>
</template>
