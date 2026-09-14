<script setup lang="ts">
import {
  ASSET_CONDITIONS
} from '~/types/asset'

const { assets } = useAssets()

const conditionStats = computed(() => {
  const totalAssets = assets.value.length

  return ASSET_CONDITIONS.map(condition => {
    const count = assets.value.filter(
      asset => asset.condition === condition
    ).length

    return {
      condition,
      count,
      percentage: totalAssets
        ? Math.round((count / totalAssets) * 100)
        : 0
    }
  })
})
</script>

<template>
  <div class="rounded-xl bg-white p-5 shadow-sm">
    
    <h2 class="text-base font-semibold text-text-primary">
      Asset Condition Overview
    </h2>

    <div
      v-if="assets.length"
      class="mt-6 space-y-4"
    >
      <div
        v-for="stat in conditionStats"
        :key="stat.condition"
      >
        <div class="mb-1 flex items-center justify-between text-sm">
          <span class="font-medium text-text-primary">{{ stat.condition }}</span>
          <span class="text-text-secondary">{{ stat.count }} ({{ stat.percentage }}%)</span>
        </div>

        <div class="h-2 w-full overflow-hidden rounded-full bg-gray-100">
          <div
            class="h-full rounded-full bg-primary transition-all duration-500"
            :style="{ width: `${stat.percentage}%` }"
          />
        </div>
      </div>
    </div>

    <div
      v-else
      class="mt-6 flex min-h-32 items-center justify-center rounded-lg border border-dashed border-gray-200 px-4 text-center text-sm text-text-secondary"
    >
      No asset condition data available.
    </div>

  </div>
</template>
