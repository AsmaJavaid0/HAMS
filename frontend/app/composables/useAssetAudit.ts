import type {
  AuditAction
} from '~/types/audit'

import type {
  Asset
} from '~/types/asset'


export const useAssetAudit = () => {

  const {
    addAuditEvent
  } = useAuditLog()


  const recordAssetAudit = (
    action: AuditAction,
    asset: Asset,
    actor: {
      id: string
      name: string
    },
    description: string
  ) => {

    return addAuditEvent({
      action,

      entityType:
        'Asset',

      entityId:
        asset.assetId,
      hospitalId: asset.hospitalId,
      entityName:
        asset.name,

      actorId:
        actor.id,

      actorName:
        actor.name,

      description
    })
  }


  return {
    recordAssetAudit
  }
}
