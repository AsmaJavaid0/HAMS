<script setup lang="ts">
import type { Asset } from '~/types/asset'
import type { Department } from '~/types/department'
import type { HospitalLocation } from '~/types/location'

import { getDaysUntilMaintenance, getMaintenancePriority, getMaintenancePriorityClass } from '~/utils/assetMaintenance'

const props = defineProps<{ asset: Asset; department: Department | null; location: HospitalLocation | null; locationPath: string }>()

const { getEffectiveAssetStatus, getEffectiveLocationStatus } = useDependencyStatus()
const effectiveStatus = computed(() => getEffectiveAssetStatus(props.asset))
const locationEffectiveStatus = computed(() => getEffectiveLocationStatus(props.location?.id))
const isContextUnavailable = computed(() => effectiveStatus.value === 'Unavailable')
const maintenancePriority = computed(() => getMaintenancePriority(props.asset.nextMaintenanceDate))
const maintenanceDays = computed(() => getDaysUntilMaintenance(props.asset.nextMaintenanceDate))

const getStatusClass = (status: string) => {
  switch (status) {
    case 'Operational': return 'bg-green-50 text-green-700'
    case 'Under Maintenance': return 'bg-yellow-50 text-yellow-700'
    case 'Out of Service': return 'bg-red-50 text-red-700'
    case 'Quarantined': return 'bg-orange-50 text-orange-700'
    case 'Pending Disposal': return 'bg-purple-50 text-purple-700'
    case 'Retired': return 'bg-gray-100 text-gray-600'
    default: return 'bg-gray-100 text-gray-600'
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="rounded-xl border border-gray-200 bg-white p-6">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <p class="text-sm font-semibold text-primary">{{ asset.assetId }}</p>
          <h1 class="mt-1 text-2xl font-bold text-text-primary">{{ asset.name }}</h1>
          <p class="mt-1 text-sm text-gray-500">{{ asset.category }}</p>
        </div>
        <div class="text-right">
          <NuxtLink
            :to="`/assets/${asset.assetId}/verification`"
            class="inline-flex items-center rounded-lg border border-primary px-3 py-2 text-sm font-semibold text-primary hover:bg-blue-50"
          >
            Verify Asset
          </NuxtLink>
          <span class="mt-2 inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="getStatusClass(effectiveStatus)">
            {{ effectiveStatus }}
          </span>
          <p class="mt-2 text-xs text-gray-500">Recorded status: {{ asset.operationalStatus }}</p>
          <p class="mt-1 text-xs text-gray-500">Condition: {{ asset.condition }}</p>
          <div class="mt-2">
            <span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="getMaintenancePriorityClass(maintenancePriority)">
              Maintenance: {{ maintenancePriority }}
            </span>
          </div>
        </div>
      </div>
      <div v-if="isContextUnavailable" class="mt-4 rounded-lg border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
        This asset is currently unavailable because its department or location is inactive. Its recorded asset lifecycle status has not been changed.
      </div>
    </div>

    <div class="grid gap-6 xl:grid-cols-2">
      <section class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="font-semibold text-text-primary">Technical Information</h2>
        <dl class="mt-5 space-y-4">
          <div><dt class="text-xs text-gray-400">Manufacturer</dt><dd class="mt-1 text-sm font-medium">{{ asset.manufacturer || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Model</dt><dd class="mt-1 text-sm font-medium">{{ asset.model || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Serial Number</dt><dd class="mt-1 text-sm font-medium">{{ asset.serialNumber || '—' }}</dd></div>
        </dl>
      </section>

      <section class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="font-semibold text-text-primary">Current Assignment</h2>
        <dl class="mt-5 space-y-4">
          <div><dt class="text-xs text-gray-400">Department</dt><dd class="mt-1 text-sm font-medium">{{ department?.name || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Location</dt><dd class="mt-1 text-sm font-medium">{{ location?.name || '—' }}</dd><p v-if="locationPath" class="mt-1 text-xs text-gray-400">{{ locationPath }}</p><p class="mt-2 text-xs" :class="locationEffectiveStatus === 'Active' ? 'text-green-600' : 'text-amber-600'">Location status: {{ locationEffectiveStatus }}</p></div>
          <div><dt class="text-xs text-gray-400">Responsible Team</dt><dd class="mt-1 text-sm font-medium">{{ asset.responsibleTeam || '—' }}</dd></div>
        </dl>
      </section>

      <section class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="font-semibold text-text-primary">Warranty & Vendor</h2>
        <dl class="mt-5 space-y-4">
          <div><dt class="text-xs text-gray-400">Purchase Date</dt><dd class="mt-1 text-sm font-medium">{{ asset.purchaseDate || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Warranty Expiry</dt><dd class="mt-1 text-sm font-medium">{{ asset.warrantyExpiry || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Vendor</dt><dd class="mt-1 text-sm font-medium">{{ asset.vendorName || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Service Contact</dt><dd class="mt-1 text-sm font-medium">{{ asset.serviceContact || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Service Email</dt><dd class="mt-1 text-sm font-medium">{{ asset.serviceEmail || '—' }}</dd></div>
        </dl>
      </section>

      <section class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="font-semibold text-text-primary">Maintenance Schedule</h2>
        <dl class="mt-5 space-y-4">
          <div><dt class="text-xs text-gray-400">Last Maintenance</dt><dd class="mt-1 text-sm font-medium">{{ asset.lastMaintenanceDate || '—' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Next Maintenance</dt><dd class="mt-1 text-sm font-medium">{{ asset.nextMaintenanceDate || 'Not scheduled' }}</dd></div>
          <div><dt class="text-xs text-gray-400">Maintenance Priority</dt><dd class="mt-2"><span class="inline-flex rounded-full px-2.5 py-1 text-xs font-semibold" :class="getMaintenancePriorityClass(maintenancePriority)">{{ maintenancePriority }}</span></dd></div>
          <div v-if="maintenanceDays !== null"><dt class="text-xs text-gray-400">Schedule</dt><dd class="mt-1 text-sm font-medium"><template v-if="maintenanceDays < 0">{{ Math.abs(maintenanceDays) }} day(s) overdue</template><template v-else>Maintenance due in {{ maintenanceDays }} day(s)</template></dd></div>
        </dl>
      </section>

      <section class="rounded-xl border border-gray-200 bg-white p-6">
        <h2 class="font-semibold text-text-primary">Notes</h2>
        <div class="mt-5 space-y-5"><div><p class="text-xs text-gray-400">Warranty Notes</p><p class="mt-1 text-sm leading-6 text-gray-600">{{ asset.warrantyNotes || 'No warranty notes.' }}</p></div><div><p class="text-xs text-gray-400">Asset Description</p><p class="mt-1 text-sm leading-6 text-gray-600">{{ asset.description || 'No description.' }}</p></div></div>
      </section>
    </div>
  </div>
</template>
