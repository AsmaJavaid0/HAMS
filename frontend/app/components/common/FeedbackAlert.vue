<script setup lang="ts">
import { computed } from 'vue'

type AlertType =
  | 'success'
  | 'error'
  | 'warning'
  | 'info'

const props = withDefaults(
  defineProps<{
    message: string
    type?: AlertType
  }>(),
  {
    type: 'info'
  }
)

const alertClasses = computed(() => {
  const classes: Record<
    AlertType,
    string
  > = {
    success:
      'border-green-100 bg-green-50 text-green-700',

    error:
      'border-red-100 bg-red-50 text-red-600',

    warning:
      'border-yellow-100 bg-yellow-50 text-yellow-700',

    info:
      'border-blue-100 bg-blue-50 text-blue-700'
  }

  return classes[
    props.type
  ]
})
</script>

<template>
  <div
    v-if="message"
    class="rounded-lg border px-4 py-3 text-sm"
    :class="alertClasses"
    role="status"
  >
    {{ message }}
  </div>
</template>