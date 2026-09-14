<script setup lang="ts">
type InputType =
  | 'text'
  | 'email'
  | 'tel'
  | 'date'
  | 'number'
  | 'password'

withDefaults(
  defineProps<{
    id: string
    label?: string
    type?: InputType
    placeholder?: string
    required?: boolean
    disabled?: boolean
    readonly?: boolean
    autocomplete?: string
    error?: string
    hint?: string
  }>(),
  {
    label: '',
    type: 'text',
    placeholder: '',
    required: false,
    disabled: false,
    readonly: false,
    autocomplete: undefined,
    error: '',
    hint: ''
  }
)

const model = defineModel<string>({
  default: ''
})
</script>

<template>
  <div>
    <label
      v-if="label"
      :for="id"
      class="mb-2 block text-sm font-medium text-text-primary"
    >
      {{ label }}

      <span
        v-if="required"
        class="text-red-500"
      >
        *
      </span>
    </label>

    <input
      :id="id"
      v-model="model"
      :type="type"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      :readonly="readonly"
      :autocomplete="autocomplete"
      class="h-11 w-full rounded-lg border bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500"
      :class="
        error
          ? 'border-red-300 focus:border-red-500 focus:ring-2 focus:ring-red-500/10'
          : 'border-gray-300 focus:border-primary focus:ring-2 focus:ring-primary/10'
      "
    />

    <p
      v-if="error"
      class="mt-1.5 text-xs text-red-500"
    >
      {{ error }}
    </p>

    <p
      v-else-if="hint"
      class="mt-1.5 text-xs text-text-secondary"
    >
      {{ hint }}
    </p>
  </div>
</template>