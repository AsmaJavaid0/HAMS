<script setup lang="ts">

import type {
  Department,
  DepartmentFormPayload
} from '~/types/department'

import type {
  StaffMember
} from '~/types/staff'


const props = defineProps<{
  department?: Department | null

  managers: StaffMember[]
}>()


const emit = defineEmits<{
  close: []

  save: [
    payload: DepartmentFormPayload
  ]
}>()


/*
|--------------------------------------------------------------------------
| STATE
|--------------------------------------------------------------------------
*/

const departmentName =
  ref('')

const departmentCode =
  ref('')

const managerId =
  ref<number | null>(
    null
  )

const description =
  ref('')


/*
|--------------------------------------------------------------------------
| ERRORS
|--------------------------------------------------------------------------
*/

const nameError =
  ref('')

const codeError =
  ref('')


/*
|--------------------------------------------------------------------------
| EDIT MODE
|--------------------------------------------------------------------------
*/

const isEditMode =
  computed(
    () =>
      Boolean(
        props.department
      )
  )


/*
|--------------------------------------------------------------------------
| LOAD DEPARTMENT
|--------------------------------------------------------------------------
*/

const loadDepartment = () => {

  const department =
    props.department


  if (department) {

    departmentName.value =
      department.name

    departmentCode.value =
      department.code

    managerId.value =
      department.managerId

    description.value =
      department.description ?? ''

  } else {

    departmentName.value =
      ''

    departmentCode.value =
      ''

    managerId.value =
      null

    description.value =
      ''
  }


  nameError.value = ''

  codeError.value = ''
}


watch(
  () => props.department,

  loadDepartment,

  {
    immediate: true
  }
)


/*
|--------------------------------------------------------------------------
| AVAILABLE MANAGERS
|--------------------------------------------------------------------------
*/

const activeManagers =
  computed(() => {

    return props.managers.filter(
      manager =>
        manager.role ===
          'manager' &&

        manager.status ===
          'Active'
    )
  })


/*
|--------------------------------------------------------------------------
| SUBMIT
|--------------------------------------------------------------------------
*/

const handleSubmit = () => {

  nameError.value = ''

  codeError.value = ''


  let valid = true


  if (
    !departmentName.value.trim()
  ) {

    nameError.value =
      'Department name is required.'

    valid = false
  }


  if (
    !departmentCode.value.trim()
  ) {

    codeError.value =
      'Department code is required.'

    valid = false
  }


  if (!valid) {
    return
  }


  emit('save', {

    name:
      departmentName.value
        .trim(),

    code:
      departmentCode.value
        .trim()
        .toUpperCase(),

    managerId:
      managerId.value,

    description:
      description.value
        .trim()
  })
}

</script>


<template>

  <CommonBaseModal
    :title="isEditMode ? 'Edit Department' : 'Add Department'"
    :description="isEditMode
      ? 'Update department information and manager assignment.'
      : 'Create a hospital department.'"
    size="md"
    @close="emit('close')"
  >


      <form
        class="space-y-5 p-6"
        @submit.prevent="handleSubmit"
      >

        <!-- Name -->

        <CommonBaseInput
          id="departmentName"
          v-model="departmentName"
          label="Department Name"
          placeholder="e.g. Intensive Care Unit"
          :error="nameError"
        />


        <!-- Code -->

        <CommonBaseInput
          id="departmentCode"
          v-model="departmentCode"
          label="Department Code"
          placeholder="e.g. ICU"
          :error="codeError"
        />


        <!-- Manager -->

        <div>

          <label
            for="departmentManager"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Department Manager
          </label>

          <select
            id="departmentManager"
            v-model="managerId"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
          >

            <option :value="null">
              No manager assigned
            </option>

            <option
              v-for="manager in activeManagers"
              :key="manager.id"
              :value="manager.id"
            >
              {{ manager.name }}
              ·
              {{ manager.employeeId }}
            </option>

          </select>

          <p
            class="mt-1.5 text-xs text-text-secondary"
          >
            Only active staff with the Manager role can be assigned.
          </p>

        </div>


        <!-- Description -->

        <div>

          <label
            for="departmentDescription"
            class="mb-2 block text-sm font-medium text-text-primary"
          >
            Description
          </label>

          <textarea
            id="departmentDescription"
            v-model="description"
            rows="4"
            placeholder="Optional department description"
            class="w-full resize-none rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm outline-none focus:border-primary focus:ring-2 focus:ring-primary/10"
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
                : 'Add Department'
            }}
          </CommonBaseButton>

        </div>

      </form>
  </CommonBaseModal>

</template>