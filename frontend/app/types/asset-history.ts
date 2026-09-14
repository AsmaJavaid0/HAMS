export type AssetHistoryAction =
  | 'Created'
  | 'Master Updated'
  | 'Operational Updated'
  | 'Moved'
  | 'Document Added'


export interface AssetHistoryChange {
  field: string

  label: string

  oldValue: string

  newValue: string
}


export interface AssetHistoryEvent {
  id: string

  assetId: string

  hospitalId: string

  action: AssetHistoryAction

  actorId: string

  actorName: string

  summary: string

  changes: AssetHistoryChange[]

  timestamp: string
}


export interface AssetHistoryEventPayload {
  assetId: string

  hospitalId: string

  action: AssetHistoryAction

  actorId: string

  actorName: string

  summary: string

  changes?: AssetHistoryChange[]
}


export interface AssetMutationActor {
  id: string

  name: string
}