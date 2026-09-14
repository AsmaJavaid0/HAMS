import type {
  AssetHistoryEvent,
  AssetHistoryEventPayload
} from '~/types/asset-history'
import { useMockPersistence } from '~/composables/useMockPersistence'


export const useAssetHistory = () => {

  const assetHistory =
    useMockPersistence<AssetHistoryEvent[]>(
      'assetcare-asset-history',
      () => [
        {
          id: 'seed-asset-1',

          assetId:
            'AC-AST-0001',

          hospitalId:
            'hosp-001',

          action:
            'Created',

          actorId:
            'usr-admin-001',

          actorName:
            'Sarah Mitchell',

          summary:
            'Asset registered in AssetCare.',

          changes: [],

          timestamp:
            '2026-08-01T09:00:00.000Z'
        },

        {
          id: 'seed-asset-2',

          assetId:
            'AC-AST-0002',

          hospitalId:
            'hosp-001',

          action:
            'Created',

          actorId:
            'usr-admin-001',

          actorName:
            'Sarah Mitchell',

          summary:
            'Asset registered in AssetCare.',

          changes: [],

          timestamp:
            '2026-08-02T09:00:00.000Z'
        },

        {
          id: 'seed-asset-3',

          assetId:
            'AC-AST-0003',

          hospitalId:
            'hosp-001',

          action:
            'Created',

          actorId:
            'usr-admin-001',

          actorName:
            'Sarah Mitchell',

          summary:
            'Asset registered in AssetCare.',

          changes: [],

          timestamp:
            '2026-08-03T09:00:00.000Z'
        },

        {
          id: 'seed-asset-4',

          assetId:
            'AC-AST-0004',

          hospitalId:
            'hosp-001',

          action:
            'Created',

          actorId:
            'usr-admin-001',

          actorName:
            'Sarah Mitchell',

          summary:
            'Asset registered in AssetCare.',

          changes: [],

          timestamp:
            '2026-08-04T09:00:00.000Z'
        }
      ],
      2
    )


  const addAssetHistoryEvent = (
    payload: AssetHistoryEventPayload
  ) => {

    const event:
      AssetHistoryEvent = {

      id:
        `${Date.now()}-${assetHistory.value.length + 1}`,

      assetId:
        payload.assetId,

      hospitalId:
        payload.hospitalId,

      action:
        payload.action,

      actorId:
        payload.actorId,

      actorName:
        payload.actorName,

      summary:
        payload.summary,

      changes:
        payload.changes ?? [],

      timestamp:
        new Date().toISOString()
    }


    assetHistory.value.unshift(
      event
    )


    return event
  }


  const getHistoryForAsset = (
    assetId: string
  ) => {

    return assetHistory.value
      .filter(
        event =>
          event.assetId ===
          assetId
      )
      .sort(
        (a, b) =>
          new Date(
            b.timestamp
          ).getTime() -
          new Date(
            a.timestamp
          ).getTime()
      )
  }


  return {
    assetHistory,

    addAssetHistoryEvent,

    getHistoryForAsset
  }
}