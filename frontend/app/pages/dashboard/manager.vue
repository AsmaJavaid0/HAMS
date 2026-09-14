<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })
const { user } = useAuth()
const { assets } = useAssets()

const supervisedAssets = computed(() => {
  return assets.value.filter(asset => {
    const belongsToHospital = asset.hospitalId === user.value?.hospital_id
    const belongsToDepartment = !user.value?.department_id ||
      asset.departmentId === user.value.department_id

    return belongsToHospital && belongsToDepartment
  })
})

const totalAssetsUnderSupervision = computed(
  () => supervisedAssets.value.length
)

const assetsRequiringAttention = computed(() =>
  supervisedAssets.value.filter(asset =>
    [
      'Under Maintenance',
      'Out of Service',
      'Quarantined',
      'Pending Disposal'
    ].includes(asset.operationalStatus)
  ).length
)
</script>

<template>
  <div class="space-y-6">
    <div class="rounded-xl bg-white p-6 shadow-sm border border-gray-100">
      <h1 class="text-2xl font-bold text-gray-800">Manager Dashboard</h1>
      <p class="text-sm text-gray-500 mt-1">Welcome back, {{ user?.name }}. Hospital asset overview & department reports.</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Assets Requiring Attention</p>
        <h3 class="text-2xl font-bold text-orange-500 mt-2">{{ assetsRequiringAttention }}</h3>
      </div>
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Total Assets Under Supervision</p>
        <h3 class="text-2xl font-bold text-primary mt-2">{{ totalAssetsUnderSupervision }}</h3>
      </div>
      <div class="bg-white p-5 rounded-xl shadow-sm border border-gray-100">
        <p class="text-xs uppercase font-semibold text-gray-400">Pending Approvals</p>
        <h3 class="text-2xl font-bold text-orange-500 mt-2">—</h3>
      </div>
    </div>
  </div>
</template>