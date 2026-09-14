<script setup lang="ts">
import type { AuditAction, AuditEntityType } from '~/types/audit'

definePageMeta({ layout: 'dashboard' })

const { auditEvents } = useAuditLog()
const { user } = useAuth()

const searchQuery = ref('')
const entityFilter = ref<'All' | AuditEntityType>('All')
const actionFilter = ref<'All' | AuditAction>('All')
const dateFilter = ref('')

const entityTypes: Array<'All' | AuditEntityType> = [
  'All', 'Hospital', 'Department', 'Location', 'Staff', 'Asset',
  'Maintenance', 'Fault Report', 'Compliance'
]

const actions: Array<'All' | AuditAction> = [
  'All', 'Created', 'Updated', 'Activated', 'Deactivated', 'Suspended',
  'Moved', 'Status Changed', 'Document Added', 'Reported', 'Resolved',
  'Scheduled', 'Completed', 'Cancelled', 'Expired', 'Deleted'
]

const hospitalEvents = computed(() =>
  auditEvents.value.filter(event => event.hospitalId === user.value?.hospital_id)
)

const filteredEvents = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()

  return hospitalEvents.value.filter(event => {
    const matchesSearch = !query ||
      event.actorName.toLowerCase().includes(query) ||
      event.entityName.toLowerCase().includes(query) ||
      event.description.toLowerCase().includes(query)

    const matchesEntity = entityFilter.value === 'All' || event.entityType === entityFilter.value
    const matchesAction = actionFilter.value === 'All' || event.action === actionFilter.value
    const matchesDate = !dateFilter.value || event.timestamp.startsWith(dateFilter.value)

    return matchesSearch && matchesEntity && matchesAction && matchesDate
  })
})

const formatDate = (value: string) => new Date(value).toLocaleString()

const exportCsv = () => {
  const rows = [
    ['Date', 'Action', 'Entity', 'Entity Name', 'Actor', 'Description'],
    ...filteredEvents.value.map(event => [
      event.timestamp,
      event.action,
      event.entityType,
      event.entityName,
      event.actorName,
      event.description
    ])
  ]

  const csv = rows
    .map(row => row.map(value => `"${String(value).replace(/"/g, '""')}"`).join(','))
    .join('\n')

  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = 'assetcare-audit-log.csv'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-bold text-text-primary">Audit Log</h1>
      <p class="mt-1 text-sm text-text-secondary">
        Review important actions recorded in your hospital.
      </p>
    </div>

    <section class="rounded-xl border border-gray-200 bg-white p-4">
      <div class="grid grid-cols-1 gap-3 md:grid-cols-4">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search activity..."
          class="rounded-lg border border-gray-300 px-4 py-2.5 text-sm outline-none focus:border-primary"
        >
        <select v-model="entityFilter" class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm">
          <option v-for="type in entityTypes" :key="type" :value="type">
            {{ type === 'All' ? 'All Entity Types' : type }}
          </option>
        </select>
        <select v-model="actionFilter" class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm">
          <option v-for="action in actions" :key="action" :value="action">
            {{ action === 'All' ? 'All Actions' : action }}
          </option>
        </select>
        <input v-model="dateFilter" type="date" class="rounded-lg border border-gray-300 px-4 py-2.5 text-sm">
      </div>
      <div class="mt-3 flex items-center justify-between">
        <p class="text-sm text-text-secondary">{{ filteredEvents.length }} recorded events</p>
        <button type="button" class="rounded-lg bg-primary px-4 py-2.5 text-sm font-medium text-white hover:opacity-90" @click="exportCsv">
          Export CSV
        </button>
      </div>
    </section>

    <section v-if="filteredEvents.length" class="overflow-hidden rounded-xl border border-gray-200 bg-white">
      <div class="divide-y divide-gray-100">
        <div v-for="event in filteredEvents" :key="event.id" class="flex flex-col gap-2 px-5 py-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="text-sm text-text-primary">
              <span class="font-semibold">{{ event.actorName }}</span> {{ event.description }}
            </p>
            <p class="mt-1 text-xs text-gray-400">
              {{ event.entityType }} · {{ event.entityName }} · {{ event.action }}
            </p>
          </div>
          <p class="shrink-0 text-xs text-gray-400">{{ formatDate(event.timestamp) }}</p>
        </div>
      </div>
    </section>

    <section v-else class="rounded-xl border border-gray-200 bg-white px-6 py-16 text-center">
      <h2 class="text-lg font-semibold text-text-primary">No audit activity found</h2>
      <p class="mt-2 text-sm text-text-secondary">Try changing your filters or search criteria.</p>
    </section>
  </div>
</template>
