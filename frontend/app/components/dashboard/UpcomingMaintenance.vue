<script setup lang="ts">

type Maintenance = {
  asset: string
  assetCode: string
  department: string
  date: string
  priority: string
}

defineProps<{
  maintenance: Maintenance[]
}>()

const viewAllMaintenance = () => {
  navigateTo('/assets')
}

</script>

<template>

  <div class="rounded-xl border border-border bg-white p-5 shadow-sm">

    <!-- Header -->
    <div class="mb-5 flex items-center justify-between">

      <div>
        <h2 class="text-lg font-semibold text-text-primary">
          Upcoming Maintenance
        </h2>

        <p class="mt-1 text-sm text-text-secondary">
          Equipment scheduled for maintenance
        </p>
      </div>

      <button
        type="button"
        class="text-sm font-medium text-primary hover:underline"
        @click="viewAllMaintenance"
      >
        View All
      </button>

    </div>


    <!-- Table -->
    <div class="overflow-x-auto">

      <table class="w-full min-w-[650px]">

        <thead>

          <tr class="border-b border-border">

            <th
              class="pb-3 text-left text-xs font-semibold uppercase tracking-wide text-text-secondary"
            >
              Asset
            </th>

            <th
              class="pb-3 text-left text-xs font-semibold uppercase tracking-wide text-text-secondary"
            >
              Department
            </th>

            <th
              class="pb-3 text-left text-xs font-semibold uppercase tracking-wide text-text-secondary"
            >
              Date
            </th>

            <th
              class="pb-3 text-left text-xs font-semibold uppercase tracking-wide text-text-secondary"
            >
              Priority
            </th>

          </tr>

        </thead>


        <tbody>

          <tr
            v-for="item in maintenance"
            :key="item.assetCode"
            class="border-b border-border last:border-0"
          >

            <!-- Asset -->
            <td class="py-4">

              <div class="font-medium text-text-primary">
                {{ item.asset }}
              </div>

              <div class="mt-1 text-xs text-text-secondary">
                {{ item.assetCode }}
              </div>

            </td>


            <!-- Department -->
            <td class="py-4 text-sm text-text-secondary">
              {{ item.department }}
            </td>


            <!-- Date -->
            <td class="py-4 text-sm text-text-secondary">
              {{ item.date }}
            </td>


            <!-- Priority -->
            <td class="py-4">

              <span
                class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
                :class="{
                  'bg-red-100 text-red-700': item.priority === 'Critical',
                  'bg-orange-100 text-orange-700': item.priority === 'High',
                  'bg-yellow-100 text-yellow-700': item.priority === 'Medium',
                  'bg-green-100 text-green-700': item.priority === 'Low'
                }"
              >
                {{ item.priority }}
              </span>

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>

</template>