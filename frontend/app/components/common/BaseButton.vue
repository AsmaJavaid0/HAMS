<script setup lang="ts">
import { computed } from 'vue'

type ButtonVariant =
  | 'primary'
  | 'secondary'
  | 'danger'
  | 'success'
  | 'warning'
  | 'ghost'

type ButtonSize =
  | 'sm'
  | 'md'

const props = withDefaults(
  defineProps<{
    variant?: ButtonVariant
    size?: ButtonSize
    type?: 'button' | 'submit' | 'reset'
    disabled?: boolean
  }>(),
  {
    variant: 'primary',
    size: 'md',
    type: 'button',
    disabled: false
  }
)

const variantClasses = computed(() => {
  const classes: Record<
    ButtonVariant,
    string
  > = {
    primary:
      'bg-primary text-white hover:bg-blue-700 border border-transparent',

    secondary:
      'bg-white text-gray-700 border border-gray-300 hover:bg-gray-50',

    danger:
      'bg-white text-red-600 border border-red-200 hover:bg-red-50',

    success:
      'bg-white text-green-700 border border-green-200 hover:bg-green-50',

    warning:
      'bg-white text-yellow-700 border border-yellow-200 hover:bg-yellow-50',

    ghost:
      'bg-transparent text-gray-700 border border-transparent hover:bg-gray-100'
  }

  return classes[
    props.variant
  ]
})

const sizeClasses = computed(() => {
  return props.size === 'sm'
    ? 'px-3 py-1.5 text-xs'
    : 'px-4 py-2.5 text-sm'
})
</script>

<template>
  <button
    :type="type"
    :disabled="disabled"
    class="inline-flex items-center justify-center rounded-lg font-medium transition disabled:cursor-not-allowed disabled:opacity-50"
    :class="[
      variantClasses,
      sizeClasses
    ]"
  >
    <slot />
  </button>
</template>