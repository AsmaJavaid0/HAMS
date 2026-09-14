<script setup lang="ts">

type Alert = {
  title: string
  message: string
  type: string
  time: string
}

defineProps<{
  alerts: Alert[]
}>()

const viewAllAlerts = () => {
  navigateTo('/admin/audit')
}

</script>

<template>

  <div class="rounded-xl border border-border bg-white p-5 shadow-sm">

    <!-- Header -->
    <div class="mb-5">

      <h2 class="text-lg font-semibold text-text-primary">
        System Alerts
      </h2>

      <p class="mt-1 text-sm text-text-secondary">
        Important notifications and alerts
      </p>

    </div>


    <!-- Alerts -->
    <div class="space-y-4">

      <div
        v-for="alert in alerts"
        :key="`${alert.title}-${alert.time}`"
        class="rounded-lg border p-4"
        :class="{
          'border-red-200 bg-red-50': alert.type === 'error',
          'border-orange-200 bg-orange-50': alert.type === 'warning',
          'border-green-200 bg-green-50': alert.type === 'success'
        }"
      >

        <div class="flex gap-3">

          <!-- Alert Icon -->
          <div
            class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-sm font-bold"
            :class="{
              'bg-red-100 text-red-600': alert.type === 'error',
              'bg-orange-100 text-orange-600': alert.type === 'warning',
              'bg-green-100 text-green-600': alert.type === 'success'
            }"
          >
            <span v-if="alert.type === 'error'">!</span>
            <span v-else-if="alert.type === 'warning'">!</span>
            <span v-else>✓</span>
          </div>


          <!-- Alert Content -->
          <div class="min-w-0 flex-1">

            <h3 class="text-sm font-semibold text-text-primary">
              {{ alert.title }}
            </h3>

            <p class="mt-1 text-xs leading-5 text-text-secondary">
              {{ alert.message }}
            </p>

            <p class="mt-2 text-xs text-text-secondary">
              {{ alert.time }}
            </p>

          </div>

        </div>

      </div>

    </div>


    <!-- View All -->
    <button
      type="button"
      class="mt-5 w-full rounded-lg border border-border py-2.5 text-sm font-medium text-primary transition hover:bg-gray-50"
      @click="viewAllAlerts"
    >
      View All Alerts
    </button>

  </div>

</template>