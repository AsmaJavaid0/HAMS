<script setup lang="ts">

type Department = {
  name: string
  assets: number
  percentage: number
}

defineProps<{
  departments: Department[]
}>()

const viewAllDepartments = () => {
  navigateTo('/admin/departments')
}

</script>

<template>

  <div class="rounded-xl border border-border bg-white p-5 shadow-sm">

    <!-- Header -->
    <div class="mb-5 flex items-center justify-between">

      <div>
        <h2 class="text-lg font-semibold text-text-primary">
          Top Departments
        </h2>

        <p class="mt-1 text-sm text-text-secondary">
          Departments with the highest number of assets
        </p>
      </div>

      <button
        type="button"
        class="text-sm font-medium text-primary hover:underline"
        @click="viewAllDepartments"
      >
        View All
      </button>

    </div>


    <!-- Departments -->
    <div class="space-y-5">

      <div
        v-for="department in departments"
        :key="department.name"
      >

        <div class="mb-2 flex items-center justify-between">

          <span class="text-sm font-medium text-text-primary">
            {{ department.name }}
          </span>

          <span class="text-sm text-text-secondary">
            {{ department.assets }} assets
          </span>

        </div>


        <!-- Progress Bar -->
        <div class="h-2 w-full overflow-hidden rounded-full bg-gray-100">

          <div
            class="h-full rounded-full bg-primary transition-all duration-500"
            :style="{ width: `${department.percentage}%` }"
          />

        </div>

      </div>

    </div>

  </div>

</template>
