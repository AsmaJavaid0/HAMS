<script setup lang="ts">

import type {
  AssetHistoryEvent
} from '~/types/asset-history'


defineProps<{
  events: AssetHistoryEvent[]
}>()


const formatDate = (
  value: string
) => {

  return new Date(
    value
  ).toLocaleString(
    'en-AU',
    {
      dateStyle: 'medium',
      timeStyle: 'short'
    }
  )
}

</script>


<template>

  <div
    class="rounded-xl border border-gray-200 bg-white"
  >

    <div
      class="border-b border-gray-200 px-6 py-5"
    >

      <h2
        class="text-lg font-semibold text-text-primary"
      >
        Asset History
      </h2>

      <p
        class="mt-1 text-sm text-text-secondary"
      >
        Traceable asset changes, movement and lifecycle activity.
      </p>

    </div>


    <div
      v-if="events.length"
      class="divide-y divide-gray-100"
    >

      <div
        v-for="event in events"
        :key="event.id"
        class="px-6 py-5"
      >

        <div
          class="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between"
        >

          <div>

            <div
              class="flex flex-wrap items-center gap-2"
            >

              <span
                class="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-primary"
              >
                {{ event.action }}
              </span>

              <span
                class="text-sm font-semibold text-text-primary"
              >
                {{ event.actorName }}
              </span>

            </div>


            <p
              class="mt-2 text-sm text-gray-600"
            >
              {{ event.summary }}
            </p>

          </div>


          <p
            class="text-xs text-gray-400"
          >
            {{ formatDate(event.timestamp) }}
          </p>

        </div>


        <div
          v-if="event.changes.length"
          class="mt-4 overflow-hidden rounded-lg border border-gray-200"
        >

          <div
            v-for="change in event.changes"
            :key="`${event.id}-${change.field}`"
            class="grid gap-1 border-b border-gray-100 px-4 py-3 last:border-0 sm:grid-cols-[160px_1fr]"
          >

            <p
              class="text-xs font-semibold uppercase tracking-wide text-gray-400"
            >
              {{ change.label }}
            </p>


            <p
              class="text-sm text-gray-600"
            >
              <span
                class="line-through opacity-60"
              >
                {{ change.oldValue }}
              </span>

              <span
                class="mx-2 text-gray-400"
              >
                →
              </span>

              <span
                class="font-medium text-text-primary"
              >
                {{ change.newValue }}
              </span>
            </p>

          </div>

        </div>

      </div>

    </div>


    <div
      v-else
      class="px-6 py-12 text-center text-sm text-gray-500"
    >
      No asset history has been recorded yet.
    </div>

  </div>

</template>