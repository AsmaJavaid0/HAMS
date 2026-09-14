<script setup lang="ts">

import type {
  HospitalFormPayload,
  HospitalStatus
} from '~/types/hospital'
import { useOperationFeedback } from '~/composables/useOperationFeedback'

definePageMeta({
  layout: 'dashboard'
})


const {
  hospital,

  australianStates,
  australianTimezones,

  updateHospital
} = useHospital()

const {
  user
} = useAuth()


const {
  addAuditEvent
} = useAuditLog()

/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const isEditing =
  ref(false)

const {
  operationError,
  successMessage,
  clearFeedback,
  setError,
  setSuccess
} = useOperationFeedback()


const name =
  ref('')

const code =
  ref('')

const registrationNumber =
  ref('')

const email =
  ref('')

const phone =
  ref('')

const address =
  ref('')

const suburb =
  ref('')

const state =
  ref('')

const postcode =
  ref('')

const timezone =
  ref('')

const status =
  ref<HospitalStatus>(
    'Active'
  )


/*
|--------------------------------------------------------------------------
| LOAD PROFILE
|--------------------------------------------------------------------------
*/

const loadHospital = () => {

  name.value =
    hospital.value.name

  code.value =
    hospital.value.code

  registrationNumber.value =
    hospital.value.registrationNumber

  email.value =
    hospital.value.email

  phone.value =
    hospital.value.phone

  address.value =
    hospital.value.address

  suburb.value =
    hospital.value.suburb

  state.value =
    hospital.value.state

  postcode.value =
    hospital.value.postcode

  timezone.value =
    hospital.value.timezone

  status.value =
    hospital.value.status
}


loadHospital()


/*
|--------------------------------------------------------------------------
| EDIT
|--------------------------------------------------------------------------
*/

const startEditing = () => {

  clearFeedback()

  loadHospital()

  isEditing.value =
    true
}


const cancelEditing = () => {

  loadHospital()

  clearFeedback()

  isEditing.value =
    false
}


/*
|--------------------------------------------------------------------------
| SAVE
|--------------------------------------------------------------------------
*/

const saveHospital = () => {

  clearFeedback()


  const payload:
    HospitalFormPayload = {

    name:
      name.value,

    code:
      code.value,

    registrationNumber:
      registrationNumber.value,

    email:
      email.value,

    phone:
      phone.value,

    address:
      address.value,

    suburb:
      suburb.value,

    state:
      state.value,

    postcode:
      postcode.value,

    timezone:
      timezone.value,

    status:
      status.value
  }


  const result =
    updateHospital(payload)


  if (!result.ok) {

    setError(
      result.message
    )

    return
  }


  setSuccess(
    'Hospital profile updated successfully.'
  )

  if (user.value) {

    addAuditEvent({
      action: 'Updated',

      entityType:
        'Hospital',

      entityId:
        result.hospital.id,

      entityName:
        result.hospital.name,
hospitalId:
  user.value.hospital_id,
      actorId:
        user.value.id,

      actorName:
        user.value.name,

      description:
        'updated the hospital profile.'
    })
  }

  isEditing.value =
    false
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
          Hospital Profile
        </h1>

        <p
          class="mt-1 text-sm text-text-secondary"
        >
          Manage hospital identity, contact information and organisation settings.
        </p>

      </div>


      <div
        class="flex items-center gap-3"
      >

        <template v-if="isEditing">

          <button
            type="button"
            class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
            @click="cancelEditing"
          >
            Cancel
          </button>


          <button
            type="button"
            class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
            @click="saveHospital"
          >
            Save Changes
          </button>

        </template>


        <button
          v-else
          type="button"
          class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
          @click="startEditing"
        >
          Edit Profile
        </button>

      </div>

    </div>


    <!-- Messages -->

    <CommonFeedbackAlert
      :message="operationError"
      type="error"
    />

    <CommonFeedbackAlert
      :message="successMessage"
      type="success"
    />


    <!-- Organisation Summary -->

    <div
      class="grid grid-cols-1 gap-3 sm:grid-cols-3"
    >

      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >

        <p
          class="text-xs font-semibold uppercase tracking-wide text-gray-400"
        >
          Hospital Code
        </p>

        <p
          class="mt-2 font-semibold text-text-primary"
        >
          {{ hospital.code }}
        </p>

      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >

        <p
          class="text-xs font-semibold uppercase tracking-wide text-gray-400"
        >
          Current State
        </p>

        <p
          class="mt-2 font-semibold text-text-primary"
        >
          {{ hospital.state }}
        </p>

      </div>


      <div
        class="rounded-xl border border-gray-200 bg-white p-4"
      >

        <p
          class="text-xs font-semibold uppercase tracking-wide text-gray-400"
        >
          Status
        </p>

        <span
          class="mt-2 inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
          :class="
            hospital.status === 'Active'
              ? 'bg-green-50 text-green-700'
              : 'bg-gray-100 text-gray-600'
          "
        >
          {{ hospital.status }}
        </span>

      </div>

    </div>


    <!-- Main Card -->

    <div
      class="rounded-xl border border-gray-200 bg-white shadow-sm"
    >

      <div
        class="border-b border-gray-200 px-6 py-5"
      >

        <h2
          class="text-lg font-semibold text-text-primary"
        >
          Organisation Information
        </h2>

        <p
          class="mt-1 text-sm text-text-secondary"
        >
          Hospital details used throughout AssetCare.
        </p>

      </div>


      <div
        class="grid gap-6 p-6 md:grid-cols-2"
      >

        <!-- Name -->

        <CommonBaseInput
          id="hospitalName"
          v-model="name"
          label="Hospital Name"
          :disabled="!isEditing"
        />


        <!-- Code -->

        <CommonBaseInput
          id="hospitalCode"
          v-model="code"
          label="Hospital Code"
          :disabled="!isEditing"
        />


        <!-- Registration -->

        <CommonBaseInput
          id="hospitalRegistrationNumber"
          v-model="registrationNumber"
          label="Registration Number"
          :disabled="!isEditing"
        />


        <!-- Email -->

        <CommonBaseInput
          id="hospitalEmail"
          v-model="email"
          label="Contact Email"
          type="email"
          :disabled="!isEditing"
        />


        <!-- Phone -->

        <CommonBaseInput
          id="hospitalPhone"
          v-model="phone"
          label="Phone"
          type="tel"
          :disabled="!isEditing"
        />


        <!-- Timezone -->

        <div>

          <label
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Timezone
          </label>

          <select
            v-model="timezone"
            :disabled="!isEditing"
            class="h-11 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm outline-none focus:border-primary disabled:bg-gray-50"
          >

            <option
              v-for="item in australianTimezones"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>

          </select>

        </div>


        <!-- Address -->

        <div
          class="md:col-span-2"
        >

          <label
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Street Address
          </label>

          <textarea
            v-model="address"
            rows="3"
            :disabled="!isEditing"
            class="w-full resize-none rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 disabled:bg-gray-50 disabled:text-gray-500"
          />

        </div>


        <!-- Suburb -->

        <CommonBaseInput
          id="hospitalSuburb"
          v-model="suburb"
          label="Suburb / City"
          :disabled="!isEditing"
        />


        <!-- State -->

        <div>

          <label
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            State / Territory
          </label>

          <select
            v-model="state"
            :disabled="!isEditing"
            class="h-11 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm outline-none focus:border-primary disabled:bg-gray-50"
          >

            <option
              v-for="item in australianStates"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>

          </select>

        </div>


        <!-- Postcode -->

        <CommonBaseInput
          id="hospitalPostcode"
          v-model="postcode"
          label="Postcode"
          :disabled="!isEditing"
        />


        <!-- Country -->

        <div>

          <label
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Country
          </label>

          <input
            :value="hospital.country"
            type="text"
            disabled
            class="h-11 w-full rounded-lg border border-gray-300 bg-gray-50 px-4 text-sm text-gray-500"
          />

        </div>


        <!-- Status -->

        <div>

          <label
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Organisation Status
          </label>

          <select
            v-model="status"
            :disabled="!isEditing"
            class="h-11 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm outline-none focus:border-primary disabled:bg-gray-50"
          >

            <option value="Active">
              Active
            </option>

            <option value="Inactive">
              Inactive
            </option>

          </select>

        </div>

      </div>

    </div>

  </div>

</template>