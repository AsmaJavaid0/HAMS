<script setup lang="ts">

import type {
  Department
} from '~/types/department'

import type {
  HospitalLocation,
  LocationFormPayload,
  LocationType
} from '~/types/location'
import { LOCATION_PARENT_TYPES } from '~/config/locationHierarchy'


const props = defineProps<{
  location?: HospitalLocation | null

  locations: HospitalLocation[]

  departments: Department[]
}>()


const emit = defineEmits<{
  close: []

  save: [
    payload: LocationFormPayload
  ]
}>()


/*
|--------------------------------------------------------------------------
| FORM STATE
|--------------------------------------------------------------------------
*/

const name = ref('')

const type =
  ref<LocationType>(
    'Building'
  )

const parentId =
  ref<number | null>(
    null
  )

const departmentId =
  ref<string | null>(
    null
  )

const description =
  ref('')


/*
|--------------------------------------------------------------------------
| ERRORS
|--------------------------------------------------------------------------
*/

const nameError = ref('')

const parentError = ref('')


/*
|--------------------------------------------------------------------------
| EDIT MODE
|--------------------------------------------------------------------------
*/

const isEditMode =
  computed(
    () => Boolean(
      props.location
    )
  )


/*
|--------------------------------------------------------------------------
| DESCENDANTS
|--------------------------------------------------------------------------
|
| Prevent:
|
| ICU Ward
|    ↓
| ICU Room
|
| and then assigning ICU Room
| as parent of ICU Ward.
|
*/

const descendantIds =
  computed(() => {

    const current =
      props.location

    if (!current) {
      return new Set<number>()
    }

    const ids =
      new Set<number>()

    const collect = (
      locationId: number
    ) => {

      props.locations
        .filter(
          item =>
            item.parentId ===
            locationId
        )
        .forEach(item => {

          if (
            ids.has(item.id)
          ) {
            return
          }

          ids.add(item.id)

          collect(item.id)
        })
    }

    collect(current.id)

    return ids
  })


/*
|--------------------------------------------------------------------------
| POSSIBLE PARENTS
|--------------------------------------------------------------------------
*/

const parentLocations =
  computed(() => {

    return props.locations.filter(
      location => {

        /*
         * Cannot parent itself
         */

        if (
          props.location &&
          location.id ===
          props.location.id
        ) {
          return false
        }

        /*
         * Cannot choose descendant
         */

        if (
          descendantIds.value.has(
            location.id
          )
        ) {
          return false
        }

        /*
         * Inactive location
         * cannot receive new children.
         */

        if (
          location.status !==
          'Active'
        ) {
          return false
        }

        /*
        |--------------------------------------------------------------------------
        | Hierarchy Rules
        |--------------------------------------------------------------------------
        */

        if (
          type.value ===
          'Building'
        ) {
          return false
        }

        return location.type ===
          LOCATION_PARENT_TYPES[
            type.value as Exclude<LocationType, 'Building'>
          ]
      }
    )
  })


/*
|--------------------------------------------------------------------------
| ACTIVE DEPARTMENTS
|--------------------------------------------------------------------------
*/

const activeDepartments =
  computed(() => {

    return props.departments.filter(
      department =>
        department.status ===
        'Active'
    )
  })


/*
|--------------------------------------------------------------------------
| LOAD DATA
|--------------------------------------------------------------------------
*/

const loadLocation = () => {

  const location =
    props.location

  if (location) {

    name.value =
      location.name

    type.value =
      location.type

    parentId.value =
      location.parentId

    departmentId.value =
      location.departmentId

    description.value =
      location.description ?? ''

  } else {

    name.value = ''

    type.value =
      'Building'

    parentId.value =
      null

    departmentId.value =
      null

    description.value = ''
  }

  nameError.value = ''

  parentError.value = ''
}


watch(
  () => props.location,

  loadLocation,

  {
    immediate: true
  }
)


/*
|--------------------------------------------------------------------------
| TYPE CHANGE
|--------------------------------------------------------------------------
*/

watch(
  type,

  () => {

    /*
     * Buildings are root locations.
     */

    if (
      type.value ===
      'Building'
    ) {
      parentId.value =
        null
    }

    /*
     * If selected parent is no longer valid,
     * clear it.
     */

    if (
      parentId.value &&
      !parentLocations.value.some(
        location =>
          location.id ===
          parentId.value
      )
    ) {
      parentId.value =
        null
    }
  }
)


/*
|--------------------------------------------------------------------------
| SUBMIT
|--------------------------------------------------------------------------
*/

const handleSubmit = () => {

  nameError.value = ''

  parentError.value = ''

  let valid = true


  if (!name.value.trim()) {

    nameError.value =
      'Location name is required.'

    valid = false
  }


  /*
   * Every location except Building
   * needs a parent.
   */

  if (
    type.value !==
      'Building' &&
    !parentId.value
  ) {

    parentError.value =
      'Please select a parent location.'

    valid = false
  }


  if (!valid) {
    return
  }


  emit('save', {

    name:
      name.value.trim(),

    type:
      type.value,

    parentId:
      type.value ===
      'Building'
        ? null
        : parentId.value,

    departmentId:
      departmentId.value,

    description:
      description.value.trim()
  })
}

</script>


<template>

  <CommonBaseModal
    :title="isEditMode ? 'Edit Location' : 'Add Location'"
    :description="isEditMode
      ? 'Update the hospital location.'
      : 'Add a new location to the hospital hierarchy.'"
    size="xl"
    height="92vh"
    @close="emit('close')"
  >


      <!-- Form -->

      <form
        class="space-y-5 p-6"
        @submit.prevent="handleSubmit"
      >

        <!-- Name -->

        <CommonBaseInput
          id="locationName"
          v-model="name"
          label="Location Name"
          placeholder="e.g. ICU Room 101"
          :error="nameError"
        />


        <!-- Type -->

        <div>

          <label
            for="locationType"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Location Type
          </label>

          <select
            id="locationType"
            v-model="type"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
          >

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

        </div>


        <!-- Parent -->

        <div>

          <label
            for="parentLocation"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Parent Location
          </label>

          <select
            id="parentLocation"
            v-model="parentId"
            :disabled="type === 'Building'"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 disabled:cursor-not-allowed disabled:bg-gray-100"
          >

            <option :value="null">
              {{
                type === 'Building'
                  ? 'Root location'
                  : 'Select parent location'
              }}
            </option>

            <option
              v-for="locationItem in parentLocations"
              :key="locationItem.id"
              :value="locationItem.id"
            >
              {{ locationItem.name }}
              ·
              {{ locationItem.type }}
            </option>

          </select>

          <p
            v-if="parentError"
            class="mt-1.5 text-xs text-red-500"
          >
            {{ parentError }}
          </p>

          <p
            v-else
            class="mt-1.5 text-xs text-text-secondary"
          >
            Buildings are root locations. Other location types belong inside the hospital hierarchy.
          </p>

        </div>


        <!-- Department -->

        <div>

          <label
            for="locationDepartment"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Associated Department
          </label>

          <select
            id="locationDepartment"
            v-model="departmentId"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
          >

            <option :value="null">
              No department
            </option>

            <option
              v-for="department in activeDepartments"
              :key="department.id"
              :value="department.id"
            >
              {{ department.name }}
            </option>

          </select>

        </div>


        <!-- Description -->

        <div>

          <label
            for="locationDescription"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Description
          </label>

          <textarea
            id="locationDescription"
            v-model="description"
            rows="3"
            placeholder="Optional location description"
            class="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
          />

        </div>


        <!-- Actions -->

        <div
          class="flex justify-end gap-3 border-t border-gray-200 pt-5"
        >

          <CommonBaseButton
            type="button"
            variant="secondary"
            @click="emit('close')"
          >
            Cancel
          </CommonBaseButton>


          <CommonBaseButton
            type="submit"
            variant="primary"
            class="font-semibold"
          >
            {{
              isEditMode
                ? 'Save Changes'
                : 'Add Location'
            }}
          </CommonBaseButton>

        </div>

      </form>
  </CommonBaseModal>

</template>