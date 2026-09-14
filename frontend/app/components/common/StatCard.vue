<script setup lang="ts">

defineProps<{
  title: string
  value: string | number
  color?: string
  subtitle?: string
}>()

</script>

<template>

  <div
    class="rounded-lg border border-gray-100 bg-white p-4 shadow-sm"
  >

    <p class="text-[10px] font-semibold uppercase tracking-wide text-gray-500">
      {{ title }}
    </p>

    <div class="mt-2 flex items-end justify-between">

      <h3
        class="text-2xl font-bold"
        :class="color || 'text-text-primary'"
      >
        {{ value }}
      </h3>

      <span
        v-if="subtitle"
        class="text-[10px] text-gray-500"
      >
        {{ subtitle }}
      </span>

    </div>

  </div>

</template>