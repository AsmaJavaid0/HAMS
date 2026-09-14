<script setup lang="ts">
import AssetForm from '~/components/Forms/AssetForm.vue'
import { ASSET_CATEGORIES, ASSET_CONDITIONS, ASSET_OPERATIONAL_STATUSES } from '~/types/asset'
import type { Asset, AssetCategory, AssetCondition, AssetFormPayload, AssetOperationalStatus } from '~/types/asset'
import { getMaintenancePriority, getMaintenancePriorityClass } from '~/utils/assetMaintenance'
import type { AssetMutationActor } from '~/types/asset-history'
import { canViewAssetInScope, hasAssetPermission, hasHospitalWideAssetView } from '~/config/assetPermissions'

definePageMeta({ layout: 'dashboard' })

const { user, userRole } = useAuth()
const { getStaffByEmail } = useStaff()
const { hospital } = useHospital()
const { departments, getDepartmentById } = useDepartments()
const { locations, getLocationById } = useLocations()
const { assets, createAsset, updateAsset } = useAssets()
const { recordAssetAudit } = useAssetAudit()
const { operationError, successMessage, clearFeedback, setError, setSuccess } = useOperationFeedback()

const actor = computed<AssetMutationActor | null>(() => {
  if (!user.value) return null
  return { id: user.value.id, name: user.value.name }
})

const currentStaff = computed(() => {
  if (!user.value) return null
  return getStaffByEmail(user.value.email)
})

const canCreate = computed(() => hasAssetPermission(userRole.value, 'create'))
const canEditMaster = computed(() => hasAssetPermission(userRole.value, 'editMaster'))

const scopedAssets = computed(() => assets.value.filter(asset =>
  canViewAssetInScope(
    userRole.value,
    user.value?.hospital_id,
    currentStaff.value?.departmentId,
    asset
  )
))

const searchQuery = ref('')
const departmentFilter = ref<number | 'All'>('All')
const locationFilter = ref<number | 'All'>('All')
const categoryFilter = ref<'All' | AssetCategory>('All')
const statusFilter = ref<'All' | AssetOperationalStatus>('All')
const conditionFilter = ref<'All' | AssetCondition>('All')

const hasActiveFilters = computed(() => Boolean(
  searchQuery.value ||
  departmentFilter.value !== 'All' ||
  locationFilter.value !== 'All' ||
  categoryFilter.value !== 'All' ||
  statusFilter.value !== 'All' ||
  conditionFilter.value !== 'All'
))

const resetFilters = () => {
  searchQuery.value = ''
  departmentFilter.value = 'All'
  locationFilter.value = 'All'
  categoryFilter.value = 'All'
  statusFilter.value = 'All'
  conditionFilter.value = 'All'
}

const filterDepartments = computed(() => {
  if (hasHospitalWideAssetView(userRole.value)) return departments.value
  const departmentId = currentStaff.value?.departmentId
  if (!departmentId) return []
  const department = getDepartmentById(departmentId)
  return department ? [department] : []
})

const filterLocations = computed(() => {
  let result = locations.value
  if (departmentFilter.value !== 'All') {
    result = result.filter(location => location.departmentId === departmentFilter.value)
  } else if (!hasHospitalWideAssetView(userRole.value)) {
    const departmentId = currentStaff.value?.departmentId
    result = result.filter(location => location.departmentId === departmentId)
  }
  return result.filter(location => location.status === 'Active')
})

watch(departmentFilter, () => {
  locationFilter.value = 'All'
})

const filteredAssets = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  return scopedAssets.value.filter(asset => {
    const matchesSearch = !query ||
      asset.assetId.toLowerCase().includes(query) ||
      asset.name.toLowerCase().includes(query) ||
      asset.serialNumber.toLowerCase().includes(query) ||
      asset.manufacturer.toLowerCase().includes(query) ||
      asset.model.toLowerCase().includes(query)
    const matchesDepartment = departmentFilter.value === 'All' || asset.departmentId === departmentFilter.value
    const matchesLocation = locationFilter.value === 'All' || asset.locationId === locationFilter.value
    const matchesCategory = categoryFilter.value === 'All' || asset.category === categoryFilter.value
    const matchesStatus = statusFilter.value === 'All' || asset.operationalStatus === statusFilter.value
    const matchesCondition = conditionFilter.value === 'All' || asset.condition === conditionFilter.value
    return matchesSearch && matchesDepartment && matchesLocation && matchesCategory && matchesStatus && matchesCondition
  })
})

const operationalCount = computed(() => scopedAssets.value.filter(asset => asset.operationalStatus === 'Operational').length)
const highMaintenanceCount = computed(() => scopedAssets.value.filter(asset => getMaintenancePriority(asset.nextMaintenanceDate) === 'High').length)
const overdueMaintenanceCount = computed(() => scopedAssets.value.filter(asset => getMaintenancePriority(asset.nextMaintenanceDate) === 'Overdue').length)

const showAssetForm = ref(false)
const editingAsset = ref<Asset | null>(null)

const openCreateAsset = () => {
  if (!canCreate.value) return
  clearFeedback()
  editingAsset.value = null
  showAssetForm.value = true
}

const openEditAsset = (asset: Asset) => {
  if (!canEditMaster.value) return
  clearFeedback()
  editingAsset.value = { ...asset }
  showAssetForm.value = true
}

const closeAssetForm = () => {
  showAssetForm.value = false
  editingAsset.value = null
}

const saveAsset = (payload: AssetFormPayload) => {
  clearFeedback()
  if (!user.value || !actor.value) {
    setError('Authenticated user could not be resolved.')
    return
  }
  const wasEditing = Boolean(editingAsset.value)
  if (wasEditing && !canEditMaster.value) {
    setError('You do not have permission to edit asset master information.')
    return
  }
  if (!wasEditing && !canCreate.value) {
    setError('You do not have permission to create assets.')
    return
  }
  const result = editingAsset.value
    ? updateAsset(editingAsset.value.id, payload, actor.value, {
        role: user.value.role,
        hospitalId: user.value.hospital_id,
        departmentId: currentStaff.value?.departmentId ?? user.value.department_id
      })
    : createAsset(payload, user.value.hospital_id, actor.value)
  if (!result.ok) {
    setError(result.message)
    return
  }
  recordAssetAudit(
    wasEditing ? 'Updated' : 'Created',
    result.asset,
    { id: user.value.id, name: user.value.name },
    wasEditing ? `updated asset ${result.asset.assetId}.` : `created asset ${result.asset.assetId}.`
  )
  setSuccess(wasEditing ? `${result.asset.assetId} updated successfully.` : `${result.asset.assetId} created successfully.`)
  closeAssetForm()
}

const getStatusClass = (status: AssetOperationalStatus) => {
  switch (status) {
    case 'Operational': return 'bg-green-50 text-green-700'
    case 'Under Maintenance': return 'bg-yellow-50 text-yellow-700'
    case 'Out of Service': return 'bg-red-50 text-red-700'
    case 'Quarantined': return 'bg-orange-50 text-orange-700'
    case 'Pending Disposal': return 'bg-purple-50 text-purple-700'
    case 'Retired': return 'bg-gray-100 text-gray-600'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-2xl font-bold text-text-primary">Asset Register</h1>
        <p class="mt-1 text-sm text-text-secondary">Search and manage equipment within your authorised hospital scope.</p>
      </div>
      <CommonBaseButton v-if="canCreate" @click="openCreateAsset">+ Create Asset</CommonBaseButton>
    </div>

    <div v-if="!canEditMaster" class="rounded-lg border border-blue-100 bg-blue-50 px-4 py-3 text-sm text-blue-700">
      You have asset visibility within your authorised scope. Asset master information can only be changed by authorised administrators.
    </div>

    <CommonFeedbackAlert :message="operationError" type="error" />
    <CommonFeedbackAlert :message="successMessage" type="success" />

    <div class="grid grid-cols-2 gap-3 lg:grid-cols-4">
      <div class="rounded-xl border border-gray-200 bg-white p-4">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">Visible Assets</p>
        <p class="mt-2 text-2xl font-bold text-text-primary">{{ scopedAssets.length }}</p>
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">Operational</p>
        <p class="mt-2 text-2xl font-bold text-green-600">{{ operationalCount }}</p>
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">High Maintenance</p>
        <p class="mt-2 text-2xl font-bold text-orange-600">{{ highMaintenanceCount }}</p>
      </div>
      <div class="rounded-xl border border-gray-200 bg-white p-4">
        <p class="text-xs font-semibold uppercase tracking-wide text-gray-400">Overdue</p>
        <p class="mt-2 text-2xl font-bold text-red-600">{{ overdueMaintenanceCount }}</p>
      </div>
    </div>

    <div class="space-y-3 rounded-xl border border-gray-200 bg-white p-4">
      <input v-model="searchQuery" type="text" placeholder="Search asset ID, name, serial, manufacturer or model..." class="w-full rounded-lg border border-gray-300 px-4 py-2.5 text-sm outline-none focus:border-primary" />
      <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-5">
        <select v-model="departmentFilter" class="rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm">
          <option value="All">All Departments</option>
          <option v-for="department in filterDepartments" :key="department.id" :value="department.id">{{ department.name }}</option>
        </select>
        <select v-model="locationFilter" class="rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm">
          <option value="All">All Locations</option>
          <option v-for="location in filterLocations" :key="location.id" :value="location.id">{{ location.name }}</option>
        </select>
        <select v-model="categoryFilter" class="rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm">
          <option value="All">All Categories</option>
          <option v-for="item in ASSET_CATEGORIES" :key="item" :value="item">{{ item }}</option>
        </select>
        <select v-model="statusFilter" class="rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm">
          <option value="All">All Statuses</option>
          <option v-for="item in ASSET_OPERATIONAL_STATUSES" :key="item" :value="item">{{ item }}</option>
        </select>
        <select v-model="conditionFilter" class="rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm">
          <option value="All">All Conditions</option>
          <option v-for="item in ASSET_CONDITIONS" :key="item" :value="item">{{ item }}</option>
        </select>
      </div>
      <div v-if="hasActiveFilters" class="flex justify-end">
        <button type="button" class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50" @click="resetFilters">Clear All</button>
      </div>
    </div>

    <div class="overflow-hidden rounded-xl border border-gray-200 bg-white">
      <div class="overflow-x-auto">
        <table class="w-full min-w-[1320px] text-left">
          <thead class="border-b border-gray-200 bg-gray-50">
            <tr>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Asset</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Category</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Department</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Location</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Condition</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Maintenance Priority</th>
              <th class="px-5 py-4 text-xs font-semibold uppercase text-gray-500">Status</th>
              <th class="px-5 py-4 text-right text-xs font-semibold uppercase text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="asset in filteredAssets" :key="asset.id" class="hover:bg-gray-50">
              <td class="px-5 py-4">
                <p class="font-semibold text-text-primary">{{ asset.name }}</p>
                <p class="mt-1 text-xs font-medium text-primary">{{ asset.assetId }}</p>
                <p v-if="asset.serialNumber" class="mt-1 text-xs text-gray-400">SN: {{ asset.serialNumber }}</p>
              </td>
              <td class="px-5 py-4 text-sm text-gray-600">{{ asset.category }}</td>
              <td class="px-5 py-4 text-sm text-gray-600">{{ getDepartmentById(asset.departmentId)?.name || '—' }}</td>
              <td class="px-5 py-4 text-sm text-gray-600">{{ getLocationById(asset.locationId)?.name || '—' }}</td>
              <td class="px-5 py-4 text-sm text-gray-600">{{ asset.condition }}</td>
              <td class="px-5 py-4">
                <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="getMaintenancePriorityClass(getMaintenancePriority(asset.nextMaintenanceDate))">{{ getMaintenancePriority(asset.nextMaintenanceDate) }}</span>
                <p v-if="asset.nextMaintenanceDate" class="mt-1 text-xs text-gray-400">Due: {{ asset.nextMaintenanceDate }}</p>
              </td>
              <td class="px-5 py-4">
                <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium" :class="getStatusClass(asset.operationalStatus)">{{ asset.operationalStatus }}</span>
              </td>
              <td class="px-5 py-4">
                <div class="flex items-center justify-end gap-3">
                  <NuxtLink :to="`/assets/${asset.assetId}`" class="text-sm font-medium text-primary hover:underline">View</NuxtLink>
                  <NuxtLink :to="`/assets/${asset.assetId}/verification`" class="text-sm font-medium text-primary hover:underline">Evidence</NuxtLink>
                  <button v-if="canEditMaster" type="button" class="text-sm font-medium text-gray-600 hover:text-text-primary" @click="openEditAsset(asset)">Edit</button>
                </div>
              </td>
            </tr>
            <tr v-if="filteredAssets.length === 0">
              <td colspan="8" class="px-6 py-16 text-center">
                <h2 class="text-lg font-semibold text-text-primary">No assets found</h2>
                <p class="mt-2 text-sm text-text-secondary">No assets match the current search, filters or authorised scope.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <AssetForm v-if="showAssetForm" :asset="editingAsset" :departments="departments" :locations="locations" @close="closeAssetForm" @save="saveAsset" />
  </div>
</template>
