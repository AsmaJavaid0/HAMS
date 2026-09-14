import type {
  AuditEvent,
  AuditEventPayload
} from '~/types/audit'

import { mockAuditLogs } from '~/config/data/auditLogs'
import { useMockPersistence } from '~/composables/useMockPersistence'

export const useAuditLog = () => {
  const auditEvents = useMockPersistence<AuditEvent[]>(
    'assetcare-audit-events',
    () => [...mockAuditLogs],
    2
  )

  const addAuditEvent = (
    payload: AuditEventPayload
  ) => {
    const event: AuditEvent = {
      id: Date.now(),

      action: payload.action,

      entityType: payload.entityType,

      entityId: String(
        payload.entityId
      ),

      entityName:
        payload.entityName,

      hospitalId:
        payload.hospitalId,

      actorId:
        payload.actorId,

      actorName:
        payload.actorName,

      description:
        payload.description,

      timestamp:
        new Date().toISOString()
    }

    auditEvents.value.unshift(event)

    return event
  }

  const clearAuditLog = () => {
    auditEvents.value = []
  }

  return {
    auditEvents,
    addAuditEvent,
    clearAuditLog
  }
}