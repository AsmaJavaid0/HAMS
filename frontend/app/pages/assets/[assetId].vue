<script setup lang="ts">

import AssetDetail
  from '~/components/assets/AssetDetail.vue'

import AssetHistory
  from '~/components/assets/AssetHistory.vue'

import AssetMoveForm
  from '~/components/assets/AssetMoveForm.vue'

import AssetOperationalForm
  from '~/components/assets/AssetOperationalForm.vue'

import AssetForm
  from '~/components/Forms/AssetForm.vue'

import type {
  AssetFormPayload,
  AssetMovePayload,
  AssetOperationalUpdatePayload
} from '~/types/asset'

import type {
  AssetMutationActor
} from '~/types/asset-history'

import type {
  AssetAccessContext
} from '~/config/assetPermissions'

import {
  canViewAssetInScope,
  canChangeAssetDepartment,
  getAllowedOperationalStatuses,
  hasAssetPermission
} from '~/config/assetPermissions'

import AssetDocuments
  from '~/components/assets/AssetDocuments.vue'

import type {
  AssetDocumentUploadPayload
} from '~/types/asset-document'

definePageMeta({
  layout: 'dashboard'
})


const route =
  useRoute()


const {
  user,
  userRole
} = useAuth()


const {
  getStaffByEmail
} = useStaff()


const {
  departments,
  getDepartmentById
} = useDepartments()


const {
  locations,
  getLocationById,
  getLocationPath
} = useLocations()


const {
  getAssetByAssetId,

  updateAsset,

  updateAssetOperationalState,

  moveAsset
} = useAssets()


const {
  getHistoryForAsset
} = useAssetHistory()

const {
  getDocumentsForAsset,

  addAssetDocument
} = useAssetDocuments()


const {
  recordAssetAudit
} = useAssetAudit()

const {
  operationError,
  successMessage,
  clearFeedback,
  setError,
  setSuccess
} = useOperationFeedback()

/*
|--------------------------------------------------------------------------
| ASSET
|--------------------------------------------------------------------------
*/

const asset =
  computed(() => {

    return getAssetByAssetId(
      String(
        route.params.assetId ??
        ''
      )
    )
  })


if (!asset.value) {

  throw createError({
    statusCode: 404,
    statusMessage:
      'Asset not found'
  })
}


/*
|--------------------------------------------------------------------------
| CURRENT STAFF
|--------------------------------------------------------------------------
*/

const currentStaff =
  computed(() => {

    if (!user.value) {
      return null
    }


    return getStaffByEmail(
      user.value.email
    )
  })


/*
|--------------------------------------------------------------------------
| SCOPE
|--------------------------------------------------------------------------
*/

const canViewCurrentAsset =
  computed(() => {

    if (!asset.value) {
      return false
    }


    return canViewAssetInScope(
      userRole.value,
      user.value?.hospital_id,
      currentStaff.value?.departmentId,
      asset.value
    )
  })


if (!canViewCurrentAsset.value) {

  await navigateTo(
    '/access-denied'
  )
}


/*
|--------------------------------------------------------------------------
| PERMISSIONS
|--------------------------------------------------------------------------
*/

const canEditMaster =
  computed(() =>
    hasAssetPermission(
      userRole.value,
      'editMaster'
    )
  )


const canEditOperational =
  computed(() =>
    hasAssetPermission(
      userRole.value,
      'editOperational'
    )
  )


const canMove =
  computed(() =>
    hasAssetPermission(
      userRole.value,
      'move'
    )
  )


const canManageDocuments =
  computed(() =>
    hasAssetPermission(
      userRole.value,
      'manageDocuments'
    )
  )


const canChangeDepartment =
  computed(() =>
    canChangeAssetDepartment(
      userRole.value
    )
  )


const allowedStatuses =
  computed(() =>
    getAllowedOperationalStatuses(
      userRole.value
    )
  )


/*
|--------------------------------------------------------------------------
| CURRENT REFERENCES
|--------------------------------------------------------------------------
*/

const department =
  computed(() => {

    return asset.value
      ? getDepartmentById(
          asset.value.departmentId
        )
      : null
  })


const location =
  computed(() => {

    return asset.value
      ? getLocationById(
          asset.value.locationId
        )
      : null
  })


const locationPath =
  computed(() => {

    return asset.value
      ? getLocationPath(
          asset.value.locationId
        )
      : ''
  })


/*
|--------------------------------------------------------------------------
| HISTORY
|--------------------------------------------------------------------------
*/

const historyEvents =
  computed(() => {

    if (!asset.value) {
      return []
    }


    return getHistoryForAsset(
      asset.value.assetId
    )
  })


const assetDocuments =
  computed(() => {

    if (!asset.value) {
      return []
    }


    return getDocumentsForAsset(
      asset.value.assetId
    )
  })


/*
|--------------------------------------------------------------------------
| ACTOR
|--------------------------------------------------------------------------
*/

const actor =
  computed<AssetMutationActor | null>(
    () => {

      if (!user.value) {
        return null
      }


      return {
        id:
          user.value.id,

        name:
          user.value.name
      }
    }
  )


const assetAccessContext =
  computed<AssetAccessContext | null>(
    () => {

      if (
        !user.value ||
        !userRole.value
      ) {
        return null
      }

      return {
        role:
          userRole.value,

        hospitalId:
          user.value.hospital_id,

        departmentId:
          currentStaff.value
            ?.departmentId ??
          null
      }
    }
  )


/*
|--------------------------------------------------------------------------
| MODALS
|--------------------------------------------------------------------------
*/

const showMasterForm =
  ref(false)


const showOperationalForm =
  ref(false)


const showMoveForm =
  ref(false)


/*
|--------------------------------------------------------------------------
| MASTER UPDATE
|--------------------------------------------------------------------------
*/

const saveMaster = (
  payload: AssetFormPayload
) => {

  clearFeedback()


  if (
    !asset.value ||
    !actor.value ||
    !user.value ||
    !canEditMaster.value ||
    !assetAccessContext.value
  ) {

    setError(
      'You do not have permission to edit asset master information.'
    )

    return
  }


  const result =
    updateAsset(
      asset.value.id,
      payload,
      actor.value,
      assetAccessContext.value
    )


  if (!result.ok) {

    setError(
      result.message
    )

    return
  }


  if (user.value) {

    recordAssetAudit(
      'Updated',
      result.asset,
      {
        id:
          user.value.id,

        name:
          user.value.name
      },
      `updated asset master information for ${result.asset.assetId}.`
    )
  }


  setSuccess(
    'Asset master information updated successfully.'
  )


  showMasterForm.value =
    false
}


/*
|--------------------------------------------------------------------------
| DOCUMENT UPLOAD
|--------------------------------------------------------------------------
*/

const saveDocument = (
  payload:
    AssetDocumentUploadPayload
) => {

  clearFeedback()


  if (
    !asset.value ||
    !actor.value ||
    !user.value ||
    !assetAccessContext.value
  ) {

    setError(
      'Authenticated user could not be resolved.'
    )

    return
  }


  if (
    !canManageDocuments.value
  ) {

    setError(
      'You do not have permission to upload asset documents.'
    )

    return
  }


  const result =
    addAssetDocument(
      asset.value,
      payload,
      actor.value
    )


  if (!result.ok) {

    setError(
      result.message
    )

    return
  }


  recordAssetAudit(
    'Document Added',
    asset.value,
    {
      id:
        user.value.id,

      name:
        user.value.name
    },
    `added ${result.document.documentType.toLowerCase()} ${result.document.fileName} to ${asset.value.assetId}.`
  )


  setSuccess(
    'Asset document added successfully.'
  )
}


/*
|--------------------------------------------------------------------------
| OPERATIONAL UPDATE
|--------------------------------------------------------------------------
*/

const saveOperational = (
  payload:
    AssetOperationalUpdatePayload
) => {

  clearFeedback()


  if (
    !asset.value ||
    !actor.value ||
    !user.value ||
    !canEditOperational.value ||
    !assetAccessContext.value
  ) {

    setError(
      'You do not have permission to update this asset.'
    )

    return
  }


  /*
   * Defensive lifecycle permission.
   */

  const keepsCurrentStatus =
    payload.operationalStatus ===
      asset.value.operationalStatus


  if (
    !keepsCurrentStatus &&
    !allowedStatuses.value.includes(
      payload.operationalStatus
    )
  ) {

    setError(
      'Your role cannot apply this lifecycle status.'
    )

    return
  }

  const previousCondition =
    asset.value.condition

  const previousStatus =
    asset.value.operationalStatus


  const result =
    updateAssetOperationalState(
      asset.value.id,
      payload,
      actor.value,
      assetAccessContext.value
    )


  if (!result.ok) {

    setError(
      result.message
    )

    return
  }


  if (user.value) {

    recordAssetAudit(
      'Status Changed',
      result.asset,
      {
        id:
          user.value.id,

        name:
          user.value.name
      },
      `updated ${result.asset.assetId}: condition ${previousCondition} → ${result.asset.condition}, status ${previousStatus} → ${result.asset.operationalStatus}.`
    )
  }


  setSuccess(
    'Asset condition and lifecycle updated.'
  )


  showOperationalForm.value =
    false
}


/*
|--------------------------------------------------------------------------
| MOVE
|--------------------------------------------------------------------------
*/

const saveMove = (
  payload: AssetMovePayload
) => {

  clearFeedback()


  if (
    !asset.value ||
    !actor.value ||
    !user.value ||
    !canMove.value ||
    !assetAccessContext.value
  ) {

    setError(
      'Unable to verify your asset access.'
    )

    return
  }


  /*
   * Manager cannot move across departments.
   */

  if (
    !canChangeDepartment.value &&
    payload.departmentId !==
      asset.value.departmentId
  ) {

    setError(
      'Your role can move assets only within the current department.'
    )

    return
  }


  const oldDepartmentName =
    getDepartmentById(
      asset.value.departmentId
    )?.name ?? 'Unknown'

  const oldLocationName =
    getLocationById(
      asset.value.locationId
    )?.name ?? 'Unknown'


  const result =
    moveAsset(
      asset.value.id,
      payload,
      actor.value,
      assetAccessContext.value
    )


  if (!result.ok) {

    setError(
      result.message
    )

    return
  }


  const newDepartmentName =
    getDepartmentById(
      result.asset.departmentId
    )?.name ?? 'Unknown'

  const newLocationName =
    getLocationById(
      result.asset.locationId
    )?.name ?? 'Unknown'


  if (user.value) {

    recordAssetAudit(
      'Moved',
      result.asset,
      {
        id:
          user.value.id,

        name:
          user.value.name
      },
      `moved ${result.asset.assetId} from ${oldDepartmentName} / ${oldLocationName} to ${newDepartmentName} / ${newLocationName}.`
    )
  }


  setSuccess(
    'Asset movement recorded successfully.'
  )


  showMoveForm.value =
    false
}

</script>


<template>

  <div
    v-if="asset"
    class="space-y-6"
  >

    <!-- Back / Actions -->

    <div
      class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between"
    >

      <NuxtLink
        to="/assets"
        class="text-sm font-medium text-primary hover:underline"
      >
        ← Back to Asset Register
      </NuxtLink>


      <div
        class="flex flex-wrap gap-2"
      >

        <button
          v-if="canEditMaster"
          type="button"
          class="rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm font-medium text-gray-700 hover:bg-gray-50"
          @click="showMasterForm = true"
        >
          Edit Master Data
        </button>


        <button
          v-if="canEditOperational"
          type="button"
          class="rounded-lg border border-primary px-4 py-2.5 text-sm font-medium text-primary hover:bg-blue-50"
          @click="showOperationalForm = true"
        >
          Update Status
        </button>


        <button
          v-if="canMove"
          type="button"
          class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
          @click="showMoveForm = true"
        >
          Move Asset
        </button>

      </div>

    </div>


    <!-- Messages -->

    <CommonFeedbackAlert
      :message="operationError"
      type="error"
    />

    <CommonFeedbackAlert
      :message="successMessage"
      type="success"
    />


    <!-- Detail -->

    <AssetDetail
      :asset="asset"
      :department="department"
      :location="location"
      :location-path="locationPath"
    />


    <!-- Documents -->

    <AssetDocuments
      :documents="assetDocuments"
      :can-manage="canManageDocuments"
      @upload="saveDocument"
    />


    <!-- History -->

    <AssetHistory
      :events="historyEvents"
    />


    <!-- Master Edit -->

    <AssetForm
      v-if="showMasterForm && canEditMaster"
      :asset="asset"
      :departments="departments"
      :locations="locations"
      @close="showMasterForm = false"
      @save="saveMaster"
    />


    <!-- Operational -->

    <AssetOperationalForm
      v-if="showOperationalForm && canEditOperational"
      :asset="asset"
      :allowed-statuses="allowedStatuses"
      @close="showOperationalForm = false"
      @save="saveOperational"
    />


    <!-- Move -->

    <AssetMoveForm
      v-if="showMoveForm && canMove"
      :asset="asset"
      :departments="departments"
      :locations="locations"
      :can-change-department="canChangeDepartment"
      @close="showMoveForm = false"
      @save="saveMove"
    />

  </div>

</template>