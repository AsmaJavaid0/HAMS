<script setup lang="ts">

import {
  ASSET_CONDITIONS
} from '~/types/asset'

import type {
  Asset,
  AssetCondition,
  AssetOperationalStatus,
  AssetOperationalUpdatePayload
} from '~/types/asset'


const props = defineProps<{
  asset: Asset

  allowedStatuses:
    AssetOperationalStatus[]
}>()


const emit = defineEmits<{
  close: []

  save: [
    payload:
      AssetOperationalUpdatePayload
  ]
}>()


const condition =
  ref<AssetCondition>(
    props.asset.condition
  )


const operationalStatus =
  ref<AssetOperationalStatus>(
    props.asset.operationalStatus
  )


const errorMessage =
  ref('')


const statusOptions =
  computed(() => {

    const currentStatus =
      props.asset.operationalStatus

    return Array.from(
      new Set([
        currentStatus,
        ...props.allowedStatuses
      ])
    )
  })


const handleSubmit = () => {

  errorMessage.value = ''


  if (
    condition.value ===
      props.asset.condition &&

    operationalStatus.value ===
      props.asset.operationalStatus
  ) {

    errorMessage.value =
      'No operational changes were selected.'

    return
  }


  const statusIsAllowed =
    operationalStatus.value ===
      props.asset.operationalStatus ||
    props.allowedStatuses.includes(
      operationalStatus.value
    )

  if (!statusIsAllowed) {
    errorMessage.value =
      'You are not allowed to set this operational status.'

    return
  }


  emit('save', {

    condition:
      condition.value,

    operationalStatus:
      operationalStatus.value
  })
}

</script>


<template>

  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/40 px-4"
    @click.self="emit('close')"
  >

    <div
      class="w-full max-w-lg rounded-2xl bg-white shadow-xl"
    >

      <div
        class="flex justify-between border-b border-gray-200 px-6 py-5"
      >

        <div>

          <h2
            class="text-lg font-semibold"
          >
            Update Status
          </h2>

          <p
            class="mt-1 text-sm text-gray-500"
          >
            {{ asset.assetId }} · {{ asset.name }}
          </p>

        </div>


        <button
          type="button"
          aria-label="Close"
          class="text-xl text-gray-400"
          @click="emit('close')"
        >
          ×
        </button>

      </div>


      <form
        class="space-y-5 p-6"
        @submit.prevent="handleSubmit"
      >

        <div
          v-if="errorMessage"
          class="rounded-lg bg-red-50 px-4 py-3 text-sm text-red-600"
        >
          {{ errorMessage }}
        </div>


        <div>

          <label
            for="assetCondition"
            class="mb-2 block text-sm font-medium"
          >
            Condition
          </label>

          <select
            id="assetCondition"
            v-model="condition"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm"
          >

            <option
              v-for="item in ASSET_CONDITIONS"
              :key="item"
              :value="item"
            >
              {{ item }}
            </option>

          </select>

        </div>


        <div>

          <label
            for="assetOperationalStatus"
            class="mb-2 block text-sm font-medium"
          >
            Operational Status
          </label>

          <select
            id="assetOperationalStatus"
            v-model="operationalStatus"
            class="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm"
          >

            <option
              v-for="item in statusOptions"
              :key="item"
              :value="item"
              :disabled="
                item === asset.operationalStatus &&
                !allowedStatuses.includes(item)
              "
            >
              {{
                item === asset.operationalStatus &&
                !allowedStatuses.includes(item)
                  ? `${item} (Current)`
                  : item
              }}
            </option>

          </select>

        </div>


        <div
          class="flex justify-end gap-3 border-t border-gray-200 pt-5"
        >

          <button
            type="button"
            class="rounded-lg border border-gray-300 px-5 py-2.5 text-sm"
            @click="emit('close')"
          >
            Cancel
          </button>

          <button
            type="submit"
            class="rounded-lg bg-primary px-5 py-2.5 text-sm font-semibold text-white"
          >
            Save Status
          </button>

        </div>

      </form>

    </div>

  </div>

</template>