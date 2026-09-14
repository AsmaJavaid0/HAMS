<script setup lang="ts">

import type { Department } from '~/types/department'
import type { HospitalLocation } from '~/types/location'
import type { StaffMember } from '~/types/staff'

const props = defineProps<{
  department: Department
  manager: StaffMember | null
  staff: StaffMember[]
  locations: HospitalLocation[]
}>()

const emit = defineEmits<{
  close: []
}>()

const {
  getDepartmentOperationalState,
  getDepartmentAssetSummary
} = useDependencyStatus()

const activeStaffCount = computed(() =>
  props.staff.filter(staff => staff.status === 'Active').length
)

const unavailableStaffCount = computed(() =>
  props.staff.filter(staff => staff.status !== 'Active').length
)

const operationalState = computed(() =>
  getDepartmentOperationalState(props.department.id)
)

const assetSummary = computed(() =>
  getDepartmentAssetSummary(props.department.id)
)

</script>

<template>

  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 py-6"
    @click.self="emit('close')"
  >

    <div class="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white shadow-xl">

      <div class="flex items-start justify-between border-b border-gray-200 px-6 py-5">
        <div>
          <div class="flex flex-wrap items-center gap-2">
            <h2 class="text-xl font-bold text-text-primary">
              {{ department.name }}
            </h2>

            <span class="rounded-md bg-gray-100 px-2 py-1 text-xs font-semibold text-gray-600">
              {{ department.code }}
            </span>

            <CommonStatusBadge
              :label="department.status"
              :tone="department.status === 'Active' ? 'success' : 'neutral'"
            />

            <CommonStatusBadge
              :label="operationalState"
              :tone="operationalState === 'Operational' ? 'success' : 'neutral'"
            />
          </div>

          <p class="mt-2 text-sm text-text-secondary">
            Department access and dependency-aware operational summary.
          </p>
        </div>

        <button
          type="button"
          aria-label="Close"
          class="flex h-8 w-8 items-center justify-center rounded-lg text-xl text-gray-400 hover:bg-gray-100"
          @click="emit('close')"
        >
          ×
        </button>
      </div>

      <div class="space-y-6 p-6">

        <div class="grid grid-cols-2 gap-3 sm:grid-cols-5">
          <div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
            <p class="text-xs uppercase tracking-wide text-gray-400">Staff</p>
            <p class="mt-2 text-xl font-bold text-text-primary">{{ staff.length }}</p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
            <p class="text-xs uppercase tracking-wide text-gray-400">Active Staff</p>
            <p class="mt-2 text-xl font-bold text-green-600">{{ activeStaffCount }}</p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
            <p class="text-xs uppercase tracking-wide text-gray-400">Unavailable</p>
            <p class="mt-2 text-xl font-bold text-orange-600">{{ unavailableStaffCount }}</p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
            <p class="text-xs uppercase tracking-wide text-gray-400">Assets</p>
            <p class="mt-2 text-xl font-bold text-text-primary">{{ assetSummary.total }}</p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
            <p class="text-xs uppercase tracking-wide text-gray-400">Unavailable Assets</p>
            <p class="mt-2 text-xl font-bold text-red-600">{{ assetSummary.unavailable }}</p>
          </div>
        </div>

        <div
          v-if="unavailableStaffCount > 0"
          class="rounded-xl border border-amber-200 bg-amber-50 p-4"
        >
          <p class="text-sm font-semibold text-amber-900">Staffing dependency</p>
          <p class="mt-1 text-sm text-amber-800">
            {{ unavailableStaffCount }} assigned staff member(s) are currently unavailable. Department status remains {{ department.status }}; operational state is derived separately.
          </p>
        </div>

        <div
          v-if="assetSummary.unavailable > 0 || assetSummary.outOfService > 0"
          class="rounded-xl border border-red-200 bg-red-50 p-4"
        >
          <p class="text-sm font-semibold text-red-900">Asset dependency</p>
          <p class="mt-1 text-sm text-red-800">
            {{ assetSummary.unavailable }} asset(s) are unavailable in the current department context, including {{ assetSummary.outOfService }} explicitly out-of-service asset(s).
          </p>
        </div>

        <div>
          <h3 class="text-sm font-semibold text-text-primary">Department Manager</h3>
          <div class="mt-3 rounded-xl border border-gray-200 p-4">
            <template v-if="manager">
              <div class="flex items-center justify-between gap-4">
                <div>
                  <p class="font-semibold text-text-primary">{{ manager.name }}</p>
                  <p class="mt-1 text-sm text-gray-500">{{ manager.email }}</p>
                  <p class="mt-1 text-xs text-gray-400">{{ manager.employeeId }}</p>
                </div>
                <span
                  class="rounded-full px-2.5 py-1 text-xs font-semibold"
                  :class="manager.status === 'Active' ? 'bg-green-50 text-green-700' : 'bg-amber-50 text-amber-700'"
                >
                  {{ manager.status }}
                </span>
              </div>
            </template>
            <p v-else class="text-sm text-gray-500">No manager has been assigned to this department.</p>
          </div>
        </div>

        <div>
          <h3 class="text-sm font-semibold text-text-primary">Asset Availability</h3>
          <div class="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
            <div class="rounded-xl border border-gray-200 p-3">
              <p class="text-xs text-gray-400">Operational</p>
              <p class="mt-1 text-lg font-semibold text-green-600">{{ assetSummary.operational }}</p>
            </div>
            <div class="rounded-xl border border-gray-200 p-3">
              <p class="text-xs text-gray-400">Out of Service</p>
              <p class="mt-1 text-lg font-semibold text-red-600">{{ assetSummary.outOfService }}</p>
            </div>
            <div class="rounded-xl border border-gray-200 p-3">
              <p class="text-xs text-gray-400">Maintenance</p>
              <p class="mt-1 text-lg font-semibold text-yellow-600">{{ assetSummary.underMaintenance || 0 }}</p>
            </div>
            <div class="rounded-xl border border-gray-200 p-3">
              <p class="text-xs text-gray-400">Retired</p>
              <p class="mt-1 text-lg font-semibold text-gray-600">{{ assetSummary.retired }}</p>
            </div>
          </div>
        </div>

        <div>
          <h3 class="text-sm font-semibold text-text-primary">Description</h3>
          <p class="mt-2 rounded-xl border border-gray-200 bg-gray-50 p-4 text-sm leading-6 text-gray-600">
            {{ department.description || 'No description has been provided.' }}
          </p>
        </div>

        <div>
          <h3 class="text-sm font-semibold text-text-primary">Assigned Staff</h3>
          <div
            v-if="staff.length"
            class="mt-3 divide-y divide-gray-100 overflow-hidden rounded-xl border border-gray-200"
          >
            <div
              v-for="member in staff"
              :key="member.id"
              class="flex items-center justify-between gap-4 px-4 py-3"
            >
              <div>
                <p class="text-sm font-medium text-text-primary">{{ member.name }}</p>
                <p class="mt-0.5 text-xs capitalize text-gray-500">{{ member.role }}</p>
              </div>
              <span
                class="text-xs"
                :class="member.status === 'Active' ? 'text-green-600' : 'text-gray-500'"
              >
                {{ member.status }}
              </span>
            </div>
          </div>
          <p v-else class="mt-3 rounded-xl border border-dashed border-gray-200 p-5 text-center text-sm text-gray-500">
            No staff assigned.
          </p>
        </div>

        <div>
          <h3 class="text-sm font-semibold text-text-primary">Associated Locations</h3>
          <div
            v-if="locations.length"
            class="mt-3 divide-y divide-gray-100 overflow-hidden rounded-xl border border-gray-200"
          >
            <div
              v-for="location in locations"
              :key="location.id"
              class="flex items-center justify-between gap-4 px-4 py-3"
            >
              <div>
                <p class="text-sm font-medium text-text-primary">{{ location.name }}</p>
                <p class="mt-0.5 text-xs text-gray-400">{{ location.type }}</p>
              </div>
              <span
                class="rounded-full px-2 py-1 text-xs font-medium"
                :class="location.status === 'Active' ? 'bg-green-50 text-green-700' : 'bg-gray-100 text-gray-600'"
              >
                {{ location.status }}
              </span>
            </div>
          </div>
          <p v-else class="mt-3 rounded-xl border border-dashed border-gray-200 p-5 text-center text-sm text-gray-500">
            No locations associated with this department.
          </p>
        </div>

        <div class="flex justify-end border-t border-gray-200 pt-5">
          <button
            type="button"
            class="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
            @click="emit('close')"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  </div>

</template>
