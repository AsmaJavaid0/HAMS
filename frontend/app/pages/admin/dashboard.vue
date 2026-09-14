<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

const { user } = useAuth()
const { hospital } = useHospital()
const { assets } = useAssets()
const { departments } = useDepartments()
const { locations } = useLocations()
const { staffMembers } = useStaff()
const { auditEvents } = useAuditLog()

const hospitalId = computed(() => user.value?.hospital_id ?? '')

const hospitalAssets = computed(() =>
  assets.value.filter(asset => asset.hospitalId === hospitalId.value)
)

const hospitalDepartments = computed(() =>
  departments.value.filter(department => department.hospitalId === hospitalId.value)
)

const hospitalLocations = computed(() =>
  locations.value.filter(location => location.hospitalId === hospitalId.value)
)

const hospitalBuildings = computed(() =>
  hospitalLocations.value.filter(location => location.type === 'Building')
)

const hospitalStaff = computed(() =>
  staffMembers.value.filter(staff => staff.hospitalId === hospitalId.value)
)

const recentActivity = computed(() =>
  auditEvents.value
    .filter(event => event.hospitalId === hospitalId.value)
    .slice(0, 5)
)
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-text-primary">Hospital Overview</h1>
      <p class="mt-1 text-sm text-text-secondary">
        High-level view of your hospital and its managed resources.
      </p>
    </div>

    <section class="rounded-xl border border-gray-200 bg-white p-5">
      <div class="flex flex-col gap-1 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h2 class="text-lg font-semibold text-text-primary">Hospital Snapshot</h2>
          <p class="mt-1 text-sm text-text-secondary">
            Core information about {{ hospital.name }}.
          </p>
        </div>
        <NuxtLink
          to="/admin/hospital"
          class="text-sm font-medium text-primary hover:underline"
        >
          Hospital settings
        </NuxtLink>
      </div>

      <div class="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
        <NuxtLink to="/assets" class="rounded-lg border border-gray-200 p-4 transition hover:bg-gray-50">
          <p class="text-xs font-medium uppercase tracking-wide text-text-secondary">Assets</p>
          <p class="mt-2 text-2xl font-bold text-text-primary">{{ hospitalAssets.length }}</p>
          <p class="mt-1 text-xs text-text-secondary">Registered equipment</p>
        </NuxtLink>

        <NuxtLink to="/admin/departments" class="rounded-lg border border-gray-200 p-4 transition hover:bg-gray-50">
          <p class="text-xs font-medium uppercase tracking-wide text-text-secondary">Departments</p>
          <p class="mt-2 text-2xl font-bold text-text-primary">{{ hospitalDepartments.length }}</p>
          <p class="mt-1 text-xs text-text-secondary">Hospital departments</p>
        </NuxtLink>

        <NuxtLink to="/admin/locations" class="rounded-lg border border-gray-200 p-4 transition hover:bg-gray-50">
          <p class="text-xs font-medium uppercase tracking-wide text-text-secondary">Locations</p>
          <p class="mt-2 text-2xl font-bold text-text-primary">{{ hospitalLocations.length }}</p>
          <p class="mt-1 text-xs text-text-secondary">Across {{ hospitalBuildings.length }} buildings</p>
        </NuxtLink>

        <NuxtLink to="/admin/staff" class="rounded-lg border border-gray-200 p-4 transition hover:bg-gray-50">
          <p class="text-xs font-medium uppercase tracking-wide text-text-secondary">Staff</p>
          <p class="mt-2 text-2xl font-bold text-text-primary">{{ hospitalStaff.length }}</p>
          <p class="mt-1 text-xs text-text-secondary">Active hospital users</p>
        </NuxtLink>
      </div>
    </section>

    <section class="rounded-xl border border-gray-200 bg-white p-5">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-text-primary">Recent Activity</h2>
          <p class="mt-1 text-sm text-text-secondary">A brief view of recent governance activity.</p>
        </div>
        <NuxtLink to="/admin/audit" class="text-sm font-medium text-primary hover:underline">
          View audit log
        </NuxtLink>
      </div>

      <div v-if="recentActivity.length" class="mt-4 divide-y divide-gray-100">
        <div v-for="event in recentActivity" :key="event.id" class="flex flex-col gap-1 py-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-sm font-medium text-text-primary">{{ event.action }} — {{ event.entityName }}</p>
            <p class="text-xs text-text-secondary">{{ event.description }}</p>
          </div>
          <p class="text-xs text-text-secondary">{{ new Date(event.timestamp).toLocaleString() }}</p>
        </div>
      </div>
      <p v-else class="mt-4 text-sm text-text-secondary">No recorded activity yet.</p>
    </section>
  </div>
</template>
