<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })
const { user } = useAuth()
const { assets } = useAssets()

const hospitalAssets = computed(() =>
  assets.value.filter(
    asset => asset.hospitalId === user.value?.hospital_id
  )
)

const pendingRepairs = computed(() =>
  hospitalAssets.value.filter(
    asset =>
      asset.operationalStatus === 'Under Maintenance' ||
      asset.operationalStatus === 'Out of Service'
  ).length
)

const scheduledMaintenanceThisWeek = computed(() => {
  const today = new Date()
  const endOfWeek = new Date(today)
  endOfWeek.setDate(today.getDate() + 7)

  return hospitalAssets.value.filter(asset => {
    const maintenanceDate = new Date(asset.nextMaintenanceDate)

    return (
      maintenanceDate.getTime() >= today.getTime() &&
      maintenanceDate.getTime() <= endOfWeek.getTime()
    )
  }).length
})
</script>

<template>
  <div class="space-y-6">
    <div class="rounded-xl bg-white p-6 shadow-sm border border-gray-100">
      <h1 class="text-2xl font-bold text-gray-800">Biomedical Engineering Dashboard</h1>
      <p class="text-sm text-gray-500 mt-1">Equipment maintenance, calibration schedules & repairs.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Pending Repairs</p>
        <h3 class="text-2xl font-bold text-red-500 mt-2">{{ pendingRepairs }} Units</h3>
      </div>
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Scheduled PM This Week</p>
        <h3 class="text-2xl font-bold text-primary mt-2">{{ scheduledMaintenanceThisWeek }}</h3>
      </div>
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Calibration Overdue</p>
        <h3 class="text-2xl font-bold text-orange-500 mt-2">—</h3>
      </div>
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Completed This Month</p>
        <h3 class="text-2xl font-bold text-green-600 mt-2">—</h3>
      </div>
    </div>
  </div>
</template>