<script setup lang="ts">

import type {
  Asset,
  AssetMovePayload
} from '~/types/asset'

import type {
  Department
} from '~/types/department'

import type {
  HospitalLocation
} from '~/types/location'


const props = defineProps<{
  asset: Asset

  departments: Department[]

  locations: HospitalLocation[]

  canChangeDepartment: boolean
}>()


const emit = defineEmits<{
  close: []

  save: [
    payload: AssetMovePayload
  ]
}>()


const departmentId =
  ref(
    props.asset.departmentId
  )


const locationId =
  ref<number | null>(
    props.asset.locationId
  )


const responsibleTeam =
  ref(
    props.asset.responsibleTeam
  )


const errorMessage =
  ref('')


const availableDepartments =
  computed(() => {

    return props.departments.filter(
      department =>
        department.status ===
          'Active' ||

        department.id ===
          props.asset.departmentId
    )
  })


const availableLocations =
  computed(() => {
    return props.locations.filter(
      location =>
        location.departmentId ===
          departmentId.value &&
        (
          location.status ===
            'Active' ||
          location.id ===
            props.asset.locationId
        )
    )
  })


watch(
  departmentId,
  (newValue, oldValue) => {
    if (
      newValue === oldValue
    ) {
      return
    }

    if (
      !availableLocations.value.some(
        location =>
          location.id ===
          locationId.value
      )
    ) {
      locationId.value =
        null
    }
  }
)


const handleSubmit = () => {

  errorMessage.value = ''


  if (!departmentId.value) {

    errorMessage.value =
      'Department is required.'

    return
  }


  if (!locationId.value) {

    errorMessage.value =
      'Location is required.'

    return
  }


  emit('save', {

    departmentId:
      departmentId.value,

    locationId:
      locationId.value,

    responsibleTeam:
      responsibleTeam.value.trim()
  })
}

</script>


<template>

  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4 py-6"
    @click.self="emit('close')"
  >

    <div
      class="w-full max-w-xl overflow-hidden rounded-2xl bg-white shadow-xl"
    >

      <div
        class="flex items-start justify-between border-b border-gray-200 px-6 py-5"
      >

        <div>

          <h2
            class="text-lg font-semibold text-text-primary"
          >
            Move Asset
          </h2>

          <p
            class="mt-1 text-sm text-text-secondary"
          >
            {{ asset.assetId }} · {{ asset.name }}
          </p>

        </div>


        <button
          type="button"
          aria-label="Close"
          class="text-xl text-gray-400"
          @click="emit('close')"
        >
          ×
        </button>

      </div>


      <form
        class="space-y-5 p-6"
        @submit.prevent="handleSubmit"
      >

        <div
          v-if="errorMessage"
          class="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600"
        >
          {{ errorMessage }}
        </div>


        <div>

          <label
            for="moveDepartment"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Department
          </label>

          <select
            id="moveDepartment"
            v-model="departmentId"
            :disabled="!canChangeDepartment"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm disabled:cursor-not-allowed disabled:bg-gray-100"
          >

            <option
              v-for="department in availableDepartments"
              :key="department.id"
              :value="department.id"
            >
              {{ department.name }}
            </option>

          </select>


          <p
            v-if="!canChangeDepartment"
            class="mt-1.5 text-xs text-gray-500"
          >
            Your role can move equipment only within the current department.
          </p>

        </div>


        <div>

          <label
            for="moveLocation"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Current Location
          </label>

          <select
            id="moveLocation"
            v-model="locationId"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm"
          >

            <option :value="null">
              Select location
            </option>

            <option
              v-for="location in availableLocations"
              :key="location.id"
              :value="location.id"
            >
              {{ location.name }}
              ·
              {{ location.type }}
            </option>

          </select>

        </div>


        <div>

          <label
            for="moveResponsibleTeam"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Responsible Team / Assignment
          </label>

          <input
            id="moveResponsibleTeam"
            v-model="responsibleTeam"
            type="text"
            class="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm"
          />

        </div>


        <div
          class="flex justify-end gap-3 border-t border-gray-200 pt-5"
        >

          <button
            type="button"
            class="rounded-lg border border-gray-300 px-5 py-2.5 text-sm"
            @click="emit('close')"
          >
            Cancel
          </button>


          <button
            type="submit"
            class="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white"
          >
            Move Asset
          </button>

        </div>

      </form>

    </div>

  </div>

</template>