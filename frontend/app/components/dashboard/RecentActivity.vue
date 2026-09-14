<script setup lang="ts">

type Activity = {
  user: string
  action: string
  asset: string
  assetCode: string
  time: string
}

defineProps<{
  activities: Activity[]
}>()

const viewAllActivity = () => {
  navigateTo('/admin/audit')
}

</script>

<template>

  <div class="rounded-xl border border-border bg-white p-5 shadow-sm">

    <!-- Header -->
    <div class="mb-5 flex items-center justify-between">

      <div>

        <h2 class="text-lg font-semibold text-text-primary">
          Recent Activity
        </h2>

        <p class="mt-1 text-sm text-text-secondary">
          Latest activity across hospital assets
        </p>

      </div>

      <button
        type="button"
        class="text-sm font-medium text-primary hover:underline"
        @click="viewAllActivity"
      >
        View All
      </button>

    </div>


    <!-- Activity List -->
    <div class="divide-y divide-border">

      <div
        v-for="(activity, index) in activities"
        :key="`${activity.assetCode}-${index}`"
        class="flex items-center gap-4 py-4 first:pt-0 last:pb-0"
      >

        <!-- Avatar -->
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary"
        >
          {{ activity.user.charAt(0) }}
        </div>


        <!-- Activity Details -->
        <div class="min-w-0 flex-1">

          <p class="text-sm text-text-primary">

            <span class="font-semibold">
              {{ activity.user }}
            </span>

            <span class="text-text-secondary">
              {{ ' ' + activity.action + ' ' }}
            </span>

            <span class="font-medium">
              {{ activity.asset }}
            </span>

          </p>

          <p class="mt-1 text-xs text-text-secondary">
            {{ activity.assetCode }}
          </p>

        </div>


        <!-- Time -->
        <div class="shrink-0 text-xs text-text-secondary">
          {{ activity.time }}
        </div>

      </div>

    </div>

  </div>

</template>