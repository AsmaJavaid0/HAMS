<script setup lang="ts">
definePageMeta({ layout: 'dashboard' })

import QrScanner from '~/components/faults/QrScanner.vue'
import type { AssetFaultEvidence } from '~/types/asset-fault'

const { user } = useAuth()
const { assets } = useAssets()
const { reportFault, getReportsByReporter } = useAssetFaults()
const { getLocationPath } = useLocations()

const selectedAssetId = ref<number | null>(null)
const description = ref('')
const evidence = ref<AssetFaultEvidence | undefined>()
const errorMessage = ref('')
const successMessage = ref('')
const showScanner = ref(false)
const cameraInput = ref<HTMLInputElement | null>(null)

const departmentAssets = computed(() => {
  if (!user.value?.hospital_id || !user.value.department_id) return []

  return assets.value.filter(asset =>
    asset.hospitalId === user.value?.hospital_id &&
    asset.departmentId === user.value?.department_id
  )
})

const myReports = computed(() =>
  user.value ? getReportsByReporter(user.value.id) : []
)

const selectedAsset = computed(() =>
  departmentAssets.value.find(asset => asset.id === selectedAssetId.value) ?? null
)

const selectedAssetLocation = computed(() =>
  selectedAsset.value ? getLocationPath(selectedAsset.value.locationId) : ''
)

const formatDate = (value: string) => new Date(value).toLocaleString()

const openCamera = () => cameraInput.value?.click()

const captureEvidence = (event: Event) => {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    errorMessage.value = 'Please capture an image of the equipment.'
    input.value = ''
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    errorMessage.value = 'The equipment photo must be 5 MB or smaller.'
    input.value = ''
    return
  }

  const reader = new FileReader()
  reader.onload = () => {
    evidence.value = {
      fileName: file.name || 'equipment-photo.jpg',
      mimeType: file.type,
      size: file.size,
      dataUrl: typeof reader.result === 'string' ? reader.result : undefined
    }
    errorMessage.value = ''
  }
  reader.readAsDataURL(file)
}

const removeEvidence = () => {
  evidence.value = undefined
  if (cameraInput.value) cameraInput.value.value = ''
}

const handleScan = (value: string) => {
  const normalized = value.trim().toLowerCase()
  const match = departmentAssets.value.find(asset =>
    asset.assetId.trim().toLowerCase() === normalized || String(asset.id) === value.trim()
  )

  if (!match) {
    errorMessage.value = 'This QR code does not match equipment available to you.'
    showScanner.value = false
    return
  }

  selectedAssetId.value = match.id
  errorMessage.value = ''
  showScanner.value = false
}

const submitFault = () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!user.value || user.value.role !== 'nurse') {
    errorMessage.value = 'Only nurses can submit frontline fault reports.'
    return
  }

  if (!selectedAsset.value) {
    errorMessage.value = 'Please select or scan the equipment.'
    return
  }

  const result = reportFault(
    selectedAsset.value,
    { description: description.value, evidence: evidence.value },
    { id: user.value.id, name: user.value.name },
    {
      role: user.value.role,
      hospitalId: user.value.hospital_id,
      departmentId: user.value.department_id ?? null
    }
  )

  if (!result.ok) {
    errorMessage.value = result.message
    return
  }

  successMessage.value = `${result.asset.assetId} has been marked Out of Service and the fault has been logged.`
  selectedAssetId.value = null
  description.value = ''
  evidence.value = undefined
  if (cameraInput.value) cameraInput.value.value = ''
}
</script>

<template>
  <div class="space-y-6">
    <div class="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
      <h1 class="text-2xl font-bold text-gray-800">Nurse</h1>
      <p class="mt-1 text-sm text-gray-500">
        Report equipment problems from your department. You do not manage maintenance or asset lifecycle statuses.
      </p>
    </div>

    <div class="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
      <div class="mb-5">
        <h2 class="text-lg font-semibold text-gray-800">Report an Equipment Issue</h2>
        <p class="mt-1 text-sm text-gray-500">
          A submitted fault is immediately logged and the affected asset is automatically marked Out of Service.
        </p>
      </div>

      <form class="max-w-2xl space-y-4" @submit.prevent="submitFault">
        <div class="rounded-lg border border-gray-200 bg-gray-50 p-4">
          <p class="text-xs font-medium uppercase tracking-wide text-gray-500">Reporter</p>
          <p class="mt-1 text-sm font-semibold text-gray-800">{{ user?.name }}</p>
          <p class="text-xs text-gray-500">Hospital: {{ user?.hospital_name || user?.hospital_id }}</p>
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Select Asset</label>
          <div class="flex gap-2">
            <select
              v-model="selectedAssetId"
              class="min-w-0 flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none"
            >
              <option :value="null">Select equipment</option>
              <option v-for="asset in departmentAssets" :key="asset.id" :value="asset.id">
                {{ asset.assetId }} — {{ asset.name }}
              </option>
            </select>
            <button
              type="button"
              class="shrink-0 rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
              @click="showScanner = true"
            >
              Scan QR
            </button>
          </div>
        </div>

        <div v-if="selectedAsset" class="rounded-lg border border-blue-100 bg-blue-50 p-4">
          <p class="text-xs font-medium uppercase tracking-wide text-blue-700">Equipment Location</p>
          <p class="mt-1 text-sm font-semibold text-gray-800">{{ selectedAssetLocation || 'Location not available' }}</p>
          <p class="mt-1 text-xs text-gray-500">
            This location comes from the asset record and is captured with the fault report. It is not manually entered by the nurse.
          </p>
        </div>

        <QrScanner v-if="showScanner" @scanned="handleScan" @close="showScanner = false" />

        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Equipment Photo</label>
          <input
            ref="cameraInput"
            type="file"
            accept="image/*"
            capture="environment"
            class="hidden"
            @change="captureEvidence"
          >
          <button
            type="button"
            class="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="openCamera"
          >
            Take Equipment Photo
          </button>
          <p class="mt-1 text-xs text-gray-500">Uses the device camera. Gallery selection is not offered in this workflow.</p>

          <div v-if="evidence" class="mt-3 flex items-center justify-between rounded-lg border border-gray-200 bg-gray-50 p-3">
            <div class="min-w-0">
              <p class="truncate text-sm font-medium text-gray-800">{{ evidence.fileName }}</p>
              <p class="text-xs text-gray-500">Photo attached to this fault report</p>
            </div>
            <button type="button" class="ml-3 text-sm text-red-600 hover:text-red-700" @click="removeEvidence">
              Remove
            </button>
          </div>
        </div>

        <div>
          <label class="mb-1 block text-sm font-medium text-gray-700">Describe Fault</label>
          <textarea
            v-model="description"
            rows="4"
            placeholder="Describe what is wrong with the equipment..."
            class="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primary focus:outline-none"
          />
        </div>

        <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
        <p v-if="successMessage" class="text-sm text-green-600">{{ successMessage }}</p>

        <button
          type="submit"
          class="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Report Issue
        </button>
      </form>
    </div>

    <div class="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
      <div class="mb-4 flex items-center justify-between">
        <div>
          <h2 class="text-lg font-semibold text-gray-800">My Reported Issues</h2>
          <p class="mt-1 text-sm text-gray-500">Your fault-reporting history and accountability record.</p>
        </div>
        <span class="rounded-full bg-gray-100 px-3 py-1 text-sm font-medium text-gray-700">
          {{ myReports.length }} reports
        </span>
      </div>

      <div v-if="myReports.length" class="overflow-x-auto">
        <table class="min-w-full text-left text-sm">
          <thead class="border-b border-gray-200 text-xs uppercase text-gray-500">
            <tr>
              <th class="px-3 py-3">Asset</th>
              <th class="px-3 py-3">Location</th>
              <th class="px-3 py-3">Issue</th>
              <th class="px-3 py-3">Status</th>
              <th class="px-3 py-3">Date</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100">
            <tr v-for="report in myReports" :key="report.id">
              <td class="px-3 py-3 font-medium text-gray-800">
                {{ assets.find(asset => asset.id === report.assetId)?.assetId ?? report.assetId }}
              </td>
              <td class="px-3 py-3 text-gray-600">{{ report.locationPath }}</td>
              <td class="max-w-md px-3 py-3 text-gray-600">{{ report.description }}</td>
              <td class="px-3 py-3">
                <span class="rounded-full bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700">
                  {{ report.status }}
                </span>
              </td>
              <td class="whitespace-nowrap px-3 py-3 text-gray-500">{{ formatDate(report.createdAt) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <p v-else class="text-sm text-gray-500">You have not reported any equipment issues yet.</p>
    </div>
  </div>
</template>
