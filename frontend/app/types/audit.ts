export type AuditEntityType =
  | 'Hospital'
  | 'Department'
  | 'Location'
  | 'Staff'
  | 'Asset'
  | 'Maintenance'
  | 'Fault Report'
  | 'Compliance'

export type AuditAction =
  | 'Created'
  | 'Updated'
  | 'Activated'
  | 'Deactivated'
  | 'Suspended'
  | 'Moved'
  | 'Status Changed'
  | 'Document Added'
  | 'Reported'
  | 'Resolved'
  | 'Scheduled'
  | 'Completed'
  | 'Cancelled'
  | 'Expired'
  | 'Deleted'

export interface AuditEvent {
  id: number
  hospitalId: string
  action: AuditAction
  entityType: AuditEntityType
  entityId: string
  entityName: string
  actorId: string
  actorName: string
  description: string
  timestamp: string
}

export interface AuditEventPayload {
  hospitalId: string
  action: AuditAction
  entityType: AuditEntityType
  entityId: string | number
  entityName: string
  actorId: string
  actorName: string
  description: string
}
