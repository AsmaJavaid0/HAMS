import type {
  Asset
} from '~/types/asset'

import type {
  AssetMutationActor
} from '~/types/asset-history'

import type {
  AssetDocument,
  AssetDocumentUploadPayload
} from '~/types/asset-document'

import { useAssetHistory } from '~/composables/useAssetHistory'
import {
  canViewAssetInScope,
  hasAssetPermission
} from '~/config/assetPermissions'
import { useMockPersistence } from '~/composables/useMockPersistence'

type DocumentOperationResult =
  | {
      ok: true
      document: AssetDocument
    }
  | {
      ok: false
      message: string
    }


export const useAssetDocuments = () => {

  const {
    addAssetHistoryEvent
  } = useAssetHistory()

  const {
    user,
    userRole
  } = useAuth()

  const {
    getStaffByEmail
  } = useStaff()


  /*
  |--------------------------------------------------------------------------
  | SHARED FRONTEND STATE
  |--------------------------------------------------------------------------
  |
  | Demo only.
  |
  | Frontend demo persistence keeps document metadata available after a
  | browser refresh. Actual file bytes remain browser-session preview data
  | until the backend/Storage integration is connected.
  |
  */

  const documents =
    useMockPersistence<AssetDocument[]>(
      'assetcare-asset-documents',
      () => [],
      2
    )


  /*
  |--------------------------------------------------------------------------
  | CURRENT ACCESS CONTEXT
  |--------------------------------------------------------------------------
  |
  | Permission is derived inside the mutation composable rather than being
  | trusted from the page caller.
  |
  */

  const currentDepartmentId =
    computed(() => {

      if (!user.value) {
        return null
      }

      return getStaffByEmail(
        user.value.email
      )?.departmentId ?? null
    })


  /*
  |--------------------------------------------------------------------------
  | LOOKUP
  |--------------------------------------------------------------------------
  */

  const getDocumentsForAsset = (
    assetId: string
  ) => {

    return documents.value
      .filter(
        document =>
          document.assetId ===
          assetId
      )
      .sort(
        (a, b) =>
          new Date(
            b.uploadedAt
          ).getTime() -
          new Date(
            a.uploadedAt
          ).getTime()
      )
  }


  /*
  |--------------------------------------------------------------------------
  | ADD DOCUMENT
  |--------------------------------------------------------------------------
  */

  const addAssetDocument = (
    asset: Asset,
    payload: AssetDocumentUploadPayload,
    actor: AssetMutationActor
  ): DocumentOperationResult => {

    if (!user.value || !userRole.value) {
      return {
        ok: false,
        message:
          'Authenticated user could not be resolved.'
      }
    }


    if (
      !hasAssetPermission(
        userRole.value,
        'manageDocuments'
      ) ||
      !canViewAssetInScope(
        userRole.value,
        user.value.hospital_id,
        currentDepartmentId.value,
        asset
      )
    ) {
      return {
        ok: false,
        message:
          'You do not have permission to upload documents for this asset.'
      }
    }

    if (!payload.fileName.trim()) {

      return {
        ok: false,
        message:
          'A document file is required.'
      }
    }


    if (
      payload.sizeBytes <= 0
    ) {

      return {
        ok: false,
        message:
          'The selected file is invalid.'
      }
    }


    const document:
      AssetDocument = {

      id:
        `${Date.now()}-${documents.value.length + 1}`,

      assetId:
        asset.assetId,

      hospitalId:
        asset.hospitalId,

      fileName:
        payload.fileName.trim(),

      documentType:
        payload.documentType,

      mimeType:
        payload.mimeType,

      sizeBytes:
        payload.sizeBytes,

      uploadedById:
        actor.id,

      uploadedByName:
        actor.name,

      uploadedAt:
        new Date().toISOString(),

      previewUrl:
        payload.previewUrl,

      /*
       * Later backend can return something like:
       *
       * hospital-id/assets/asset-id/file.pdf
       */
      storagePath:
        null
    }


    documents.value.unshift(
      document
    )


    /*
     * Asset-specific history.
     */

    addAssetHistoryEvent({

      assetId:
        asset.assetId,

      hospitalId:
        asset.hospitalId,

      action:
        'Document Added',

      actorId:
        actor.id,

      actorName:
        actor.name,

      summary:
        `Added ${document.documentType.toLowerCase()} ${document.fileName}.`,

      changes: [
        {
          field:
            'document',

          label:
            'Document',

          oldValue:
            '—',

          newValue:
            `${document.documentType}: ${document.fileName}`
        }
      ]
    })


    return {
      ok: true,
      document
    }
  }


  return {
    documents,

    getDocumentsForAsset,

    addAssetDocument
  }
}