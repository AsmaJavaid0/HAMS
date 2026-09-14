<script setup lang="ts">
import { useOperationFeedback } from '~/composables/useOperationFeedback'
import LocationForm
  from '~/components/Forms/LocationForm.vue'

import type {
  HospitalLocation,
  LocationFormPayload,
  LocationType
} from '~/types/location'


definePageMeta({
  layout: 'dashboard'
})


const {
  locations,

  getLocationById,
  getLocationPath,

  createLocation,
  updateLocation,

  toggleLocationStatus
} = useLocations()


const {
  departments,
  getDepartmentById
} = useDepartments()

const {
  user
} = useAuth()

const {
  addAuditEvent
} = useAuditLog()

const {
  operationError,
  successMessage,
  clearFeedback,
  setError,
  setSuccess
} = useOperationFeedback()


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const searchQuery =
  ref('')

const typeFilter =
  ref<'All' | LocationType>(
    'All'
  )

const statusFilter =
  ref<
    'All' |
    'Active' |
    'Inactive'
  >('All')


const showLocationForm =
  ref(false)

const editingLocation =
  ref<HospitalLocation | null>(
    null
  )


/*
|--------------------------------------------------------------------------
| FILTERED LOCATIONS
|--------------------------------------------------------------------------
*/

const filteredLocations =
  computed(() => {

    const query =
      searchQuery.value
        .trim()
        .toLowerCase()

    return locations.value.filter(
      location => {

        const department =
          getDepartmentById(
            location.departmentId
          )

        const parent =
          getLocationById(
            location.parentId
          )


        const matchesSearch =
          !query ||

          location.name
            .toLowerCase()
            .includes(query) ||

          location.type
            .toLowerCase()
            .includes(query) ||

          (
            department?.name
              .toLowerCase()
              .includes(query)
            ?? false
          ) ||

          (
            parent?.name
              .toLowerCase()
              .includes(query)
            ?? false
          )


        const matchesType =
          typeFilter.value === 'All' ||
          location.type ===
            typeFilter.value


        const matchesStatus =
          statusFilter.value === 'All' ||
          location.status ===
            statusFilter.value


        return (
          matchesSearch &&
          matchesType &&
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
    locations.value.filter(
      item =>
        item.status === 'Active'
    ).length
  )

const buildingCount =
  computed(() =>
    locations.value.filter(
      item =>
        item.type === 'Building'
    ).length
  )

const roomCount =
  computed(() =>
    locations.value.filter(
      item =>
        item.type === 'Room'
    ).length
  )


/*
|--------------------------------------------------------------------------
| FORM
|--------------------------------------------------------------------------
*/

const openAddLocation = () => {

  clearFeedback()

  editingLocation.value =
    null

  showLocationForm.value =
    true
}


const openEditLocation = (
  location: HospitalLocation
) => {

  clearFeedback()

  editingLocation.value = {
    ...location
  }

  showLocationForm.value =
    true
}


const closeLocationForm = () => {

  showLocationForm.value =
    false

  editingLocation.value =
    null
}


/*
|--------------------------------------------------------------------------
| SAVE
|--------------------------------------------------------------------------
*/

const saveLocation = (
  payload: LocationFormPayload
) => {

  clearFeedback()


  const wasEditing =
    Boolean(
      editingLocation.value
    )


  if (!user.value?.hospital_id) {
    setError(
      'Unable to determine the hospital.'
    )

    return
  }


  let savedLocation:
    HospitalLocation | null =
    null


  /*
  |--------------------------------------------------------------------------
  | UPDATE
  |--------------------------------------------------------------------------
  */

  if (editingLocation.value) {

    const result =
      updateLocation(
        editingLocation.value.id,
        payload
      )


    if (!result.ok) {

      setError(
        result.message
      )

      return
    }


    savedLocation =
      result.location


    addAuditEvent({

      action:
        'Updated',

      entityType:
        'Location',

      entityId:
        savedLocation.id,

      entityName:
        savedLocation.name,

      hospitalId:
        user.value.hospital_id,

      actorId:
        user.value.id,

      actorName:
        user.value.name,

      description:
        `updated location ${savedLocation.name}.`
    })

  }


  /*
  |--------------------------------------------------------------------------
  | CREATE
  |--------------------------------------------------------------------------
  */

  else {

    const result =
      createLocation(
        payload,
        user.value.hospital_id
      )


    if (!result.ok) {

      setError(
        result.message
      )

      return
    }


    savedLocation =
      result.location


    addAuditEvent({

      action:
        'Created',

      entityType:
        'Location',

      entityId:
        savedLocation.id,

      entityName:
        savedLocation.name,

      hospitalId:
        user.value.hospital_id,

      actorId:
        user.value.id,

      actorName:
        user.value.name,

      description:
        `created location ${savedLocation.name}.`
    })
  }


  if (!savedLocation) {

    setError(
      'Unable to save this location.'
    )

    return
  }


  setSuccess(
    wasEditing
      ? `${savedLocation.name} was updated successfully.`
      : `${savedLocation.name} was created successfully.`
  )


  closeLocationForm()
}
/*
|--------------------------------------------------------------------------
| STATUS
|--------------------------------------------------------------------------
*/

const changeLocationStatus = (
  location: HospitalLocation
) => {

  clearFeedback()

  const action =
    location.status === 'Active'
      ? 'deactivate'
      : 'activate'

  const confirmed =
    window.confirm(
      `Are you sure you want to ${action} "${location.name}"?`
    )

  if (!confirmed) {
    return
  }

  const result = toggleLocationStatus(
    location.id
  )

  if (!result.ok) {
    setError(result.message)
    return
  }

  setSuccess(
    `${location.name} is now ${location.status.toLowerCase()}.`
  )

  if (user.value) {

    addAuditEvent({

      action:
        location.status === 'Active'
          ? 'Activated'
          : 'Deactivated',

      entityType:
        'Location',

      entityId:
        location.id,
hospitalId:
  user.value.hospital_id,
      entityName:
        location.name,

      actorId:
        user.value.id,

      actorName:
        user.value.name,

      description:
        `${location.status === 'Active'
          ? 'activated'
          : 'deactivated'} location ${location.name}.`
    })
  }
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
          Locations
        </h1>

        <p
          class="mt-1 text-sm text-text-secondary"
        >
          Manage hospital buildings, floors, wards, rooms and sub-locations.
        </p>

      </div>


      <button
        type="button"
        class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-blue-700"
        @click="openAddLocation"
      >
        + Add Location
      </button>

    </div>

        <!-- Feedback -->

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

        <p
          class="text-xs font-medium uppercase tracking-wide text-gray-400"
        >
          Total Locations
        </p>

        <p
          class="mt-2 text-2xl font-bold text-text-primary"
        >
          {{ locations.length }}
        </p>

      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >

        <p
          class="text-xs font-medium uppercase tracking-wide text-gray-400"
        >
          Active
        </p>

        <p
          class="mt-2 text-2xl font-bold text-green-600"
        >
          {{ activeCount }}
        </p>

      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >

        <p
          class="text-xs font-medium uppercase tracking-wide text-gray-400"
        >
          Buildings
        </p>

        <p
          class="mt-2 text-2xl font-bold text-primary"
        >
          {{ buildingCount }}
        </p>

      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >

        <p
          class="text-xs font-medium uppercase tracking-wide text-gray-400"
        >
          Rooms
        </p>

        <p
          class="mt-2 text-2xl font-bold text-primary"
        >
          {{ roomCount }}
        </p>

      </div>

    </div>


    <!-- Search Filters -->

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
          placeholder="Search locations..."
          class="w-full rounded-lg border border-gray-300 bg-white py-2.5 pl-9 pr-4 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
        />

      </div>


      <select
        v-model="typeFilter"
        class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm outline-none focus:border-primary"
      >

        <option value="All">
          All Types
        </option>

        <option value="Building">
          Building
        </option>

        <option value="Floor">
          Floor
        </option>

        <option value="Ward">
          Ward
        </option>

        <option value="Room">
          Room
        </option>

        <option value="Sub-location">
          Sub-location
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

        <option value="Inactive">
          Inactive
        </option>

      </select>

    </div>


    <!-- Table -->

    <div
      v-if="filteredLocations.length"
      class="overflow-hidden rounded-xl border border-gray-200 bg-white"
    >

      <div class="overflow-x-auto">

        <table
          class="min-w-[1050px] w-full"
        >

          <thead
            class="border-b border-gray-200 bg-gray-50"
          >

            <tr>

              <th
                class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Location
              </th>

              <th
                class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Type
              </th>

              <th
                class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Parent
              </th>

              <th
                class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Department
              </th>

              <th
                class="px-6 py-4 text-left text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Status
              </th>

              <th
                class="px-6 py-4 text-right text-xs font-semibold uppercase tracking-wide text-gray-500"
              >
                Actions
              </th>

            </tr>

          </thead>


          <tbody
            class="divide-y divide-gray-100"
          >

            <tr
              v-for="location in filteredLocations"
              :key="location.id"
              class="transition hover:bg-gray-50"
            >

              <!-- Location -->

              <td class="px-6 py-4">

                <div
                  class="font-medium text-text-primary"
                >
                  {{ location.name }}
                </div>

                <div
                  class="mt-1 max-w-md truncate text-xs text-gray-400"
                  :title="getLocationPath(location.id)"
                >
                  {{ getLocationPath(location.id) }}
                </div>

              </td>


              <!-- Type -->

              <td class="px-6 py-4">

                <span
                  class="rounded-md bg-blue-50 px-2.5 py-1 text-xs font-medium text-primary"
                >
                  {{ location.type }}
                </span>

              </td>


              <!-- Parent -->

              <td
                class="px-6 py-4 text-sm text-gray-600"
              >
                {{
                  getLocationById(
                    location.parentId
                  )?.name ||
                  'Root'
                }}
              </td>


              <!-- Department -->

              <td
                class="px-6 py-4 text-sm text-gray-600"
              >
                {{
                  getDepartmentById(
                    location.departmentId
                  )?.name ||
                  '—'
                }}
              </td>


              <!-- Status -->

              <td class="px-6 py-4">

                <CommonStatusBadge
                  :label="location.status"
                  :tone="
                    location.status === 'Active'
                      ? 'success'
                      : 'neutral'
                  "
                />

              </td>


              <!-- Actions -->

              <td class="px-6 py-4">

                <div
                  class="flex items-center justify-end gap-2"
                >

                  <button
                    type="button"
                    class="rounded-lg border border-gray-200 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
                    @click="openEditLocation(location)"
                  >
                    Edit
                  </button>


                  <button
                    type="button"
                    class="rounded-lg border px-3 py-1.5 text-xs font-medium"
                    :class="
                      location.status === 'Active'
                        ? 'border-red-200 text-red-600 hover:bg-red-50'
                        : 'border-green-200 text-green-600 hover:bg-green-50'
                    "
                    @click="changeLocationStatus(location)"
                  >
                    {{
                      location.status === 'Active'
                        ? 'Deactivate'
                        : 'Activate'
                    }}
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
        ⌖
      </div>

      <h2
        class="mt-4 text-lg font-semibold text-text-primary"
      >
        No locations found
      </h2>

      <p
        class="mt-2 max-w-md text-sm text-text-secondary"
      >
        Try changing your search or filter criteria, or add a new location.
      </p>

    </div>


    <!-- Form -->

    <LocationForm
      v-if="showLocationForm"
      :location="editingLocation"
      :locations="locations"
      :departments="departments"
      @close="closeLocationForm"
      @save="saveLocation"
    />

  </div>

</template>