<script setup lang="ts">

import {
  ASSET_CATEGORIES,
  ASSET_CONDITIONS,
  ASSET_OPERATIONAL_STATUSES
} from '~/types/asset'

import type {
  Asset,
  AssetCategory,
  AssetCondition,
  AssetFormPayload,
  AssetOperationalStatus
} from '~/types/asset'

import type {
  Department
} from '~/types/department'

import type {
  HospitalLocation
} from '~/types/location'


const props = defineProps<{
  asset?: Asset | null

  departments: Department[]

  locations: HospitalLocation[]
}>()


const emit = defineEmits<{
  close: []

  save: [
    payload: AssetFormPayload
  ]
}>()


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const name =
  ref('')

const category =
  ref<AssetCategory>(
    'Medical Equipment'
  )

const serialNumber =
  ref('')

const manufacturer =
  ref('')

const model =
  ref('')


const departmentId =
  ref<string | null>(
    null
  )

const locationId =
  ref<number | null>(
    null
  )

const responsibleTeam =
  ref('')


const condition =
  ref<AssetCondition>(
    'Good'
  )

const operationalStatus =
  ref<AssetOperationalStatus>(
    'Operational'
  )


const lastMaintenanceDate =
  ref('')

const nextMaintenanceDate =
  ref('')


const purchaseDate =
  ref('')

const warrantyExpiry =
  ref('')

const vendorName =
  ref('')

const serviceContact =
  ref('')

const serviceEmail =
  ref('')

const warrantyNotes =
  ref('')

const description =
  ref('')


/*
|--------------------------------------------------------------------------
| ERRORS
|--------------------------------------------------------------------------
*/

const nameError =
  ref('')

const departmentError =
  ref('')

const locationError =
  ref('')

const dateError =
  ref('')

const maintenanceDateError =
  ref('')

const serviceEmailError =
  ref('')


const clearErrors = () => {

  nameError.value = ''

  departmentError.value = ''

  locationError.value = ''

  dateError.value = ''

  maintenanceDateError.value = ''

  serviceEmailError.value = ''
}


/*
|--------------------------------------------------------------------------
| EDIT MODE
|--------------------------------------------------------------------------
*/

const isEditMode =
  computed(() =>
    Boolean(
      props.asset
    )
  )


/*
|--------------------------------------------------------------------------
| DEPARTMENTS
|--------------------------------------------------------------------------
*/

const availableDepartments =
  computed(() => {

    return props.departments.filter(
      department =>
        department.status ===
          'Active' ||

        department.id ===
          props.asset?.departmentId
    )
  })


/*
|--------------------------------------------------------------------------
| LOCATIONS
|--------------------------------------------------------------------------
|
| Only locations belonging to selected department.
|
| Current inactive location stays visible during edit.
|
*/

const availableLocations =
  computed(() => {
    // For V1, show all active locations regardless of department selection
    // Room No. is the primary asset location
    return props.locations.filter(
      location => {
        return (
          location.status ===
            'Active' ||

          location.id ===
            props.asset?.locationId
        )
      }
    )
  })


/*
|--------------------------------------------------------------------------
| DEPARTMENT CHANGE
|--------------------------------------------------------------------------
*/

watch(
  departmentId,

  (
    newDepartmentId,
    oldDepartmentId
  ) => {

    if (
      newDepartmentId ===
      oldDepartmentId
    ) {
      return
    }


    /*
     * If selected location no longer
     * belongs to the department,
     * clear it.
     */

    if (
      locationId.value &&
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


/*
|--------------------------------------------------------------------------
| LOAD ASSET
|--------------------------------------------------------------------------
*/

const loadAsset = () => {

  clearErrors()


  if (props.asset) {

    const asset =
      props.asset


    name.value =
      asset.name

    category.value =
      asset.category

    serialNumber.value =
      asset.serialNumber

    manufacturer.value =
      asset.manufacturer

    model.value =
      asset.model


    departmentId.value =
      asset.departmentId

    locationId.value =
      asset.locationId

    responsibleTeam.value =
      asset.responsibleTeam


    condition.value =
      asset.condition

    operationalStatus.value =
      asset.operationalStatus

    lastMaintenanceDate.value =
      asset.lastMaintenanceDate

    nextMaintenanceDate.value =
      asset.nextMaintenanceDate


    purchaseDate.value =
      asset.purchaseDate

    warrantyExpiry.value =
      asset.warrantyExpiry

    vendorName.value =
      asset.vendorName

    serviceContact.value =
      asset.serviceContact

    serviceEmail.value =
      asset.serviceEmail

    warrantyNotes.value =
      asset.warrantyNotes

    description.value =
      asset.description

    return
  }


  name.value = ''

  category.value =
    'Medical Equipment'

  serialNumber.value = ''

  manufacturer.value = ''

  model.value = ''

  departmentId.value =
    null

  locationId.value =
    null

  responsibleTeam.value =
    ''

  condition.value =
    'Good'

  operationalStatus.value =
    'Operational'

  lastMaintenanceDate.value = ''

  nextMaintenanceDate.value = ''

  purchaseDate.value = ''

  warrantyExpiry.value = ''

  vendorName.value = ''

  serviceContact.value = ''

  serviceEmail.value = ''

  warrantyNotes.value = ''

  description.value = ''
}


watch(
  () => props.asset,

  loadAsset,

  {
    immediate: true
  }
)


/*
|--------------------------------------------------------------------------
| SUBMIT
|--------------------------------------------------------------------------
*/

const handleSubmit = () => {

  clearErrors()


  let valid = true


  if (!name.value.trim()) {

    nameError.value =
      'Asset name is required.'

    valid = false
  }


  // Department is now optional for V1 - no validation error


  // Location is now optional for V1 - no validation error


  if (
    purchaseDate.value &&
    warrantyExpiry.value &&
    warrantyExpiry.value <
      purchaseDate.value
  ) {

    dateError.value =
      'Warranty expiry cannot be earlier than the purchase date.'

    valid = false
  }


  if (
    lastMaintenanceDate.value &&
    nextMaintenanceDate.value &&
    nextMaintenanceDate.value <
      lastMaintenanceDate.value
  ) {

    maintenanceDateError.value =
      'Next maintenance date cannot be earlier than the last maintenance date.'

    valid = false
  }


  if (
    serviceEmail.value.trim() &&
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
      serviceEmail.value.trim()
    )
  ) {

    serviceEmailError.value =
      'Please enter a valid service email.'

    valid = false
  }


  if (!valid) {
    return
  }


  emit('save', {

    name:
      name.value.trim(),

    category:
      category.value,

    serialNumber:
      serialNumber.value.trim(),

    manufacturer:
      manufacturer.value.trim(),

    model:
      model.value.trim(),

    departmentId:
      departmentId.value,

    locationId:
      locationId.value,

    responsibleTeam:
      responsibleTeam.value.trim(),

    condition:
      condition.value,

    operationalStatus:
      operationalStatus.value,

    lastMaintenanceDate:
      lastMaintenanceDate.value,

    nextMaintenanceDate:
      nextMaintenanceDate.value,

    purchaseDate:
      purchaseDate.value,

    warrantyExpiry:
      warrantyExpiry.value,

    vendorName:
      vendorName.value.trim(),

    serviceContact:
      serviceContact.value.trim(),

    serviceEmail:
      serviceEmail.value
        .trim()
        .toLowerCase(),

    warrantyNotes:
      warrantyNotes.value.trim(),

    description:
      description.value.trim()
  })
}

</script>


<template>

  <CommonBaseModal
    :title="isEditMode ? 'Edit Asset' : 'Create Asset'"
    :description="isEditMode
      ? 'Update asset master, assignment and warranty information.'
      : 'Register new hospital equipment in AssetCare.'"
    size="xl"
    height="92vh"
    @close="emit('close')"
  >


      <form
        class="flex-1 space-y-7 overflow-y-auto p-6"
        @submit.prevent="handleSubmit"
      >

        <!-- Asset ID -->

        <div
          class="rounded-xl border border-blue-100 bg-blue-50 p-4"
        >

          <p
            class="text-xs font-semibold uppercase tracking-wide text-blue-500"
          >
            Asset ID
          </p>

          <p
            class="mt-1 font-semibold text-blue-900"
          >
            {{
              props.asset?.assetId ||
              'Generated automatically when the asset is saved'
            }}
          </p>

          <p
            class="mt-1 text-xs text-blue-600"
          >
            Asset ID is system controlled and cannot be edited.
          </p>

        </div>


        <!-- Basic Information -->

        <section>

          <h3
            class="mb-4 text-sm font-semibold text-text-primary"
          >
            Basic Information
          </h3>


          <div
            class="grid gap-5 md:grid-cols-2"
          >

            <CommonBaseInput
              id="assetName"
              v-model="name"
              label="Asset Name"
              placeholder="e.g. ICU Ventilator"
              required
              :error="nameError"
            />


            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Category *
              </label>

              <select
                v-model="category"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary"
              >

                <option
                  v-for="item in ASSET_CATEGORIES"
                  :key="item"
                  :value="item"
                >
                  {{ item }}
                </option>

              </select>

            </div>


            <CommonBaseInput
              id="assetManufacturer"
              v-model="manufacturer"
              label="Manufacturer"
              placeholder="e.g. Dräger"
            />


            <CommonBaseInput
              id="assetModel"
              v-model="model"
              label="Model"
              placeholder="e.g. Evita V600"
            />


            <div class="md:col-span-2">
              <CommonBaseInput
                id="assetSerialNumber"
                v-model="serialNumber"
                label="Serial Number"
                placeholder="Manufacturer serial number"
                hint="If provided, the serial number must be unique within the frontend demo register."
              />
            </div>

          </div>

        </section>


        <!-- Hospital Context -->

        <section>

          <h3
            class="mb-4 text-sm font-semibold text-text-primary"
          >
            Hospital Assignment
          </h3>

          <p
            v-if="isEditMode"
            class="mb-4 rounded-lg bg-blue-50 px-3 py-2 text-xs text-blue-700"
          >
            Department, location and responsible assignment are changed through the Move Asset action so that movement history is preserved.
          </p>


          <div
            class="grid gap-5 md:grid-cols-2"
          >

            <!-- Department -->

            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Department
              </label>

              <select
                v-model="departmentId"
                :disabled="isEditMode"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary"
              >

                <option :value="null">
                  Select department
                </option>

                <option
                  v-for="department in availableDepartments"
                  :key="department.id"
                  :value="department.id"
                >
                  {{ department.name }}
                </option>

              </select>


              <p
                v-if="departmentError"
                class="mt-1.5 text-xs text-red-500"
              >
                {{ departmentError }}
              </p>

            </div>


            <!-- Location -->

            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Room No.
              </label>

              <select
                v-model="locationId"
                :disabled="!departmentId || isEditMode"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary disabled:cursor-not-allowed disabled:bg-gray-100"
              >

                <option :value="null">
                  Select room
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


              <p
                v-if="locationError"
                class="mt-1.5 text-xs text-red-500"
              >
                {{ locationError }}
              </p>

            </div>


            <div class="md:col-span-2">
              <CommonBaseInput
                id="responsibleTeam"
                v-model="responsibleTeam"
                label="Responsible Team / Assignment"
                placeholder="e.g. ICU Clinical Team"
                :disabled="isEditMode"
              />
            </div>

          </div>

        </section>


        <!-- Condition -->

        <section>

          <h3
            class="mb-4 text-sm font-semibold text-text-primary"
          >
            Condition & Lifecycle
          </h3>

          <p
            v-if="isEditMode"
            class="mb-4 rounded-lg bg-blue-50 px-3 py-2 text-xs text-blue-700"
          >
            Condition and operational status are changed through Update Status so that lifecycle history is preserved.
          </p>


          <div
            class="grid gap-5 md:grid-cols-2"
          >

            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Condition
              </label>

              <select
                v-model="condition"
                :disabled="isEditMode"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm disabled:cursor-not-allowed disabled:bg-gray-100"
              >

                <option
                  v-for="item in ASSET_CONDITIONS"
                  :key="item"
                  :value="item"
                >
                  {{ item }}
                </option>

              </select>

            </div>


            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Operational Status
              </label>

              <select
                v-model="operationalStatus"
                :disabled="isEditMode"
                class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm disabled:cursor-not-allowed disabled:bg-gray-100"
              >

                <option
                  v-for="item in ASSET_OPERATIONAL_STATUSES"
                  :key="item"
                  :value="item"
                >
                  {{ item }}
                </option>

              </select>

            </div>

          </div>

        </section>


        <!-- Maintenance -->

        <section>

          <div
            class="mb-4"
          >

            <h3
              class="text-sm font-semibold text-text-primary"
            >
              Maintenance Schedule
            </h3>

            <p
              class="mt-1 text-xs text-text-secondary"
            >
              Maintenance priority is calculated automatically from the next maintenance date.
            </p>

          </div>

          <div
            class="grid gap-5 md:grid-cols-2"
          >

            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Last Maintenance Date
              </label>

              <input
                v-model="lastMaintenanceDate"
                type="date"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none focus:border-primary"
              />

            </div>

            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Next Maintenance Date
              </label>

              <input
                v-model="nextMaintenanceDate"
                type="date"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm outline-none focus:border-primary"
              />

            </div>

          </div>

          <p
            v-if="maintenanceDateError"
            class="mt-2 text-xs text-red-500"
          >
            {{ maintenanceDateError }}
          </p>

        </section>


        <!-- Warranty -->

        <section>

          <h3
            class="mb-4 text-sm font-semibold text-text-primary"
          >
            Purchase, Warranty & Vendor
          </h3>


          <div
            class="grid gap-5 md:grid-cols-2"
          >

            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Purchase Date
              </label>

              <input
                v-model="purchaseDate"
                type="date"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm"
              />

            </div>


            <div>

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Warranty Expiry
              </label>

              <input
                v-model="warrantyExpiry"
                type="date"
                class="w-full rounded-lg border border-gray-300 px-4 py-3 text-sm"
              />

              <p
                v-if="dateError"
                class="mt-1.5 text-xs text-red-500"
              >
                {{ dateError }}
              </p>

            </div>


            <CommonBaseInput
              id="vendorName"
              v-model="vendorName"
              label="Vendor Name"
              placeholder="Vendor / supplier"
            />


            <CommonBaseInput
              id="serviceContact"
              v-model="serviceContact"
              label="Service Contact"
              placeholder="+61 ..."
            />


            <div class="md:col-span-2">
              <CommonBaseInput
                id="serviceEmail"
                v-model="serviceEmail"
                label="Service Email"
                type="email"
                placeholder="service@vendor.com"
                :error="serviceEmailError"
              />
            </div>


            <div class="md:col-span-2">

              <label
                class="mb-2 block text-sm font-medium text-text-primary"
              >
                Warranty Notes
              </label>

              <textarea
                v-model="warrantyNotes"
                rows="3"
                placeholder="Warranty conditions, service agreements or notes..."
                class="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 text-sm"
              />

            </div>

          </div>

        </section>


        <!-- Description -->

        <section>

          <label
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Description
          </label>

          <textarea
            v-model="description"
            rows="3"
            placeholder="Additional asset information..."
            class="w-full resize-none rounded-lg border border-gray-300 px-4 py-3 text-sm"
          />

        </section>


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
                : 'Create Asset'
            }}
          </CommonBaseButton>

        </div>

      </form>
  </CommonBaseModal>

</template>