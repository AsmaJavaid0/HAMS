<script setup lang="ts">
const emit = defineEmits<{
  close: []
}>()

const props = withDefaults(
  defineProps<{
    title: string
    description?: string
    size?: 'md' | 'lg' | 'xl'
    height?: '90vh' | '92vh'
  }>(),
  {
    description: '',
    size: 'lg',
    height: '90vh'
  }
)

const sizeClasses = {
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl'
}

const heightClasses = {
  '90vh': 'max-h-[90vh]',
  '92vh': 'max-h-[92vh]'
}
</script>

<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
    role="dialog"
    aria-modal="true"
    @click.self="emit('close')"
  >
    <div
      class="flex max-h-full w-full flex-col overflow-hidden rounded-xl bg-white shadow-xl"
      :class="[
        sizeClasses[props.size],
        heightClasses[props.height]
      ]"
    >
      <div
        class="flex items-start justify-between border-b border-gray-200 px-6 py-4"
      >
        <div>
          <h2 class="text-lg font-semibold text-text-primary">
            {{ props.title }}
          </h2>

          <p
            v-if="props.description"
            class="mt-1 text-sm text-text-secondary"
          >
            {{ props.description }}
          </p>
        </div>

        <button
          type="button"
          aria-label="Close"
          class="rounded-lg p-2 text-gray-400 transition hover:bg-gray-100 hover:text-gray-700"
          @click="emit('close')"
        >
          ✕
        </button>
      </div>

      <div class="min-h-0 flex-1 overflow-y-auto p-6">
        <slot />
      </div>

      <div
        v-if="$slots.footer"
        class="flex justify-end gap-3 border-t border-gray-200 px-6 py-4"
      >
        <slot name="footer" />
      </div>
    </div>
  </div>
</template>