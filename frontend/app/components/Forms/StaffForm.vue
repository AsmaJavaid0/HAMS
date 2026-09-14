<script setup lang="ts">

import type {
  UserRole
} from '~/types/auth'

import type {
  Department
} from '~/types/department'

import type {
  StaffFormPayload,
  StaffMember,
  StaffStatus
} from '~/types/staff'


const props = defineProps<{
  staff?: StaffMember | null

  departments: Department[]

  currentUserRole: UserRole
}>()


const emit = defineEmits<{
  close: []

  save: [
    payload: StaffFormPayload
  ]
}>()


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const staffName = ref('')

const email = ref('')

const employeeId = ref('')

const phone = ref('')

const role =
  ref<UserRole>('nurse')

const departmentId =
  ref<string | null>(null)

const status =
  ref<StaffStatus>('Active')


/*
|--------------------------------------------------------------------------
| ERRORS
|--------------------------------------------------------------------------
*/

const nameError = ref('')

const emailError = ref('')

const employeeIdError =
  ref('')

const departmentError =
  ref('')


/*
|--------------------------------------------------------------------------
| EDIT MODE
|--------------------------------------------------------------------------
*/

const isEditMode =
  computed(
    () =>
      Boolean(props.staff)
  )


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
        'Active' ||

        department.id ===
          props.staff?.departmentId
    )
  })


/*
|--------------------------------------------------------------------------
| SELECTED DEPARTMENT
|--------------------------------------------------------------------------
*/

const selectedDepartment =
  computed(() => {

    if (!departmentId.value) {
      return null
    }

    return (
      props.departments.find(
        department =>
          department.id ===
          departmentId.value
      ) ?? null
    )
  })


/*
|--------------------------------------------------------------------------
| EFFECTIVE ACCESS
|--------------------------------------------------------------------------
*/

const effectiveAccess =
  computed(() => {

    if (role.value === 'admin') {
      return 'Whole Hospital'
    }


    if (
      role.value ===
      'biomedical'
    ) {
      return (
        'Hospital-wide Biomedical / Equipment scope'
      )
    }


    if (
      selectedDepartment.value
    ) {
      return (
        `${selectedDepartment.value.name} only`
      )
    }


    return (
      'Select a department to determine access.'
    )
  })


/*
|--------------------------------------------------------------------------
| ROLE LABEL
|--------------------------------------------------------------------------
*/

const roleLabel =
  computed(() => {

    const labels:
      Record<UserRole, string> = {

      admin:
        'Hospital Administrator',

      manager:
        'Department Manager',

      biomedical:
        'Biomedical Engineer',

      nurse:
        'Nurse / Clinical Staff'
    }

    return labels[role.value]
  })


/*
|--------------------------------------------------------------------------
| LOAD STAFF
|--------------------------------------------------------------------------
*/

const loadStaff = () => {

  const staff =
    props.staff


  if (staff) {

    staffName.value =
      staff.name

    email.value =
      staff.email

    employeeId.value =
      staff.employeeId

    phone.value =
      staff.phone

    role.value =
      staff.role

    departmentId.value =
      staff.departmentId

    status.value =
      staff.status

  } else {

    staffName.value = ''

    email.value = ''

    employeeId.value = ''

    phone.value = ''

    role.value = 'nurse'

    departmentId.value =
      null

    status.value =
      'Active'
  }


  nameError.value = ''

  emailError.value = ''

  employeeIdError.value = ''

  departmentError.value = ''
}


watch(
  () => props.staff,

  loadStaff,

  {
    immediate: true
  }
)


/*
|--------------------------------------------------------------------------
| ROLE CHANGE
|--------------------------------------------------------------------------
*/

watch(
  role,

  () => {

    /*
     * Admin doesn't belong to
     * a department.
     */

    if (
      role.value === 'admin'
    ) {
      departmentId.value =
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

  emailError.value = ''

  employeeIdError.value = ''

  departmentError.value = ''


  let valid = true


  /*
  |--------------------------------------------------------------------------
  | NAME
  |--------------------------------------------------------------------------
  */

  if (
    !staffName.value.trim()
  ) {

    nameError.value =
      'Staff member name is required.'

    valid = false
  }


  /*
  |--------------------------------------------------------------------------
  | EMAIL
  |--------------------------------------------------------------------------
  */

  if (!email.value.trim()) {

    emailError.value =
      'Email is required.'

    valid = false

  } else if (
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
      email.value.trim()
    )
  ) {

    emailError.value =
      'Please enter a valid email address.'

    valid = false
  }


  /*
  |--------------------------------------------------------------------------
  | EMPLOYEE ID
  |--------------------------------------------------------------------------
  */

  if (
    !employeeId.value.trim()
  ) {

    employeeIdError.value =
      'Employee ID is required.'

    valid = false
  }


  /*
  |--------------------------------------------------------------------------
  | DEPARTMENT
  |--------------------------------------------------------------------------
  */

  if (
    role.value !== 'admin' &&
    !departmentId.value
  ) {

    departmentError.value =
      'Department is required for this role.'

    valid = false
  }


  if (!valid) {
    return
  }


  emit('save', {

    name:
      staffName.value.trim(),

    email:
      email.value
        .trim()
        .toLowerCase(),

    employeeId:
      employeeId.value
        .trim()
        .toUpperCase(),

    phone:
      phone.value.trim(),

    role:
      role.value,

    departmentId:
      role.value === 'admin'
        ? null
        : departmentId.value,

    status:
      status.value
  })
}

</script>


<template>

  <CommonBaseModal
    :title="isEditMode ? 'Edit Staff Member' : 'Add Staff Member'"
    :description="isEditMode
      ? 'Update profile, role, department and account status.'
      : 'Create a staff profile and assign hospital access.'"
    size="lg"
    height="92vh"
    @close="emit('close')"
  >


      <form
        class="space-y-6 p-6"
        @submit.prevent="handleSubmit"
      >

        <!-- Frontend notice -->

        <div
          v-if="!isEditMode"
          class="rounded-lg border border-blue-100 bg-blue-50 px-4 py-3 text-sm text-blue-700"
        >
          Account invitation/email delivery will be connected when the authentication backend is integrated.
        </div>


        <div
          class="grid gap-5 md:grid-cols-2"
        >

          <!-- Name -->

          <CommonBaseInput
            id="staffName"
            v-model="staffName"
            label="Full Name"
            placeholder="Full name"
            :error="nameError"
          />


          <!-- Employee ID -->

          <CommonBaseInput
            id="employeeId"
            v-model="employeeId"
            label="Employee ID"
            placeholder="e.g. AC-NUR-014"
            :error="employeeIdError"
          />


          <!-- Email -->

          <CommonBaseInput
            id="staffEmail"
            v-model="email"
            label="Email"
            type="email"
            placeholder="staff@hospital.com"
            :error="emailError"
          />


          <!-- Phone -->

          <CommonBaseInput
            id="staffPhone"
            v-model="phone"
            label="Phone"
            type="tel"
            placeholder="+61 4xx xxx xxx"
            hint="(optional)"
          />


          <!-- Role -->

          <div>

            <label
              for="staffRole"
              class="mb-2 block text-sm font-medium text-text-primary"
            >
              Role
            </label>

            <select
              id="staffRole"
              v-model="role"
              class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
            >

              <option
                v-if="props.currentUserRole === 'admin'"
                value="admin"
              >
                Admin
              </option>

              <option value="manager">
                Manager
              </option>

              <option value="biomedical">
                Biomedical
              </option>

              <option value="nurse">
                Nurse
              </option>

            </select>

          </div>


          <!-- Department -->

          <div>

            <label
              for="staffDepartment"
              class="mb-2 block text-sm font-medium text-text-primary"
            >
              Department
            </label>

            <select
              id="staffDepartment"
              v-model="departmentId"
              :disabled="role === 'admin'"
              class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10 disabled:cursor-not-allowed disabled:bg-gray-100"
            >

              <option :value="null">
                {{
                  role === 'admin'
                    ? 'Whole Hospital'
                    : 'Select Department'
                }}
              </option>

              <option
                v-for="department in activeDepartments"
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


          <!-- Status -->

          <div>

            <label
              for="staffStatus"
              class="mb-2 block text-sm font-medium text-text-primary"
            >
              Account Status
            </label>

            <select
              id="staffStatus"
              v-model="status"
              class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
            >

              <option value="Active">
                Active
              </option>

              <option value="Suspended">
                Suspended
              </option>

              <option value="Inactive">
                Inactive
              </option>

            </select>

          </div>

        </div>


        <!-- Effective Access -->

        <div
          class="rounded-xl border border-gray-200 bg-gray-50 p-4"
        >

          <p
            class="text-xs font-semibold uppercase tracking-wide text-gray-400"
          >
            Effective Access
          </p>

          <div
            class="mt-3 grid gap-3 sm:grid-cols-2"
          >

            <div>

              <p
                class="text-xs text-gray-500"
              >
                Role
              </p>

              <p
                class="mt-1 text-sm font-semibold text-text-primary"
              >
                {{ roleLabel }}
              </p>

            </div>


            <div>

              <p
                class="text-xs text-gray-500"
              >
                Access Scope
              </p>

              <p
                class="mt-1 text-sm font-semibold text-text-primary"
              >
                {{ effectiveAccess }}
              </p>

            </div>

          </div>

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
                : 'Add Staff'
            }}
          </CommonBaseButton>

        </div>

      </form>
  </CommonBaseModal>

</template>