<script setup lang="ts">
import { computed } from 'vue'

type BadgeTone =
  | 'success'
  | 'warning'
  | 'danger'
  | 'info'
  | 'neutral'

const props = withDefaults(
  defineProps<{
    label: string
    tone?: BadgeTone
  }>(),
  {
    tone: 'neutral'
  }
)

const toneClasses = computed(() => {
  const classes: Record<
    BadgeTone,
    string
  > = {
    success:
      'bg-green-50 text-green-700',

    warning:
      'bg-yellow-50 text-yellow-700',

    danger:
      'bg-red-50 text-red-700',

    info:
      'bg-blue-50 text-primary',

    neutral:
      'bg-gray-100 text-gray-600'
  }

  return classes[
    props.tone
  ]
})
</script>

<template>
  <span
    class="inline-flex rounded-full px-2.5 py-1 text-xs font-medium"
    :class="toneClasses"
  >
    {{ label }}
  </span>
</template>