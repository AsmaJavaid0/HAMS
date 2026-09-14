import type {
  Asset,
  AssetFormPayload,
  AssetMovePayload,
  AssetOperationalUpdatePayload
} from '~/types/asset'
import { mockAssets } from '~/config/data/assets'

import type {
  AssetHistoryChange,
  AssetMutationActor
} from '~/types/asset-history'

import {
  canMoveAssetInContext,
  canViewAssetInScope,
  getAllowedOperationalStatuses,
  hasAssetPermission
} from '~/config/assetPermissions'

import type {
  AssetAccessContext
} from '~/config/assetPermissions'

import { useAssetHistory } from '~/composables/useAssetHistory'
import { useDepartments } from '~/composables/useDepartments'
import { useLocations } from '~/composables/useLocations'
import { useMockPersistence } from '~/composables/useMockPersistence' 
import { computed } from 'vue'

type AssetOperationResult =
  | {
      ok: true
      asset: Asset
    }
  | {
      ok: false
      message: string
    }


export const useAssets = () => {

  const {
    getDepartmentById
  } = useDepartments()


  const {
    getLocationById
  } = useLocations()


  const {
    addAssetHistoryEvent
  } = useAssetHistory()


  /*
  |--------------------------------------------------------------------------
  | SHARED STATE
  |--------------------------------------------------------------------------
  */

 const assets = useMockPersistence<Asset[]>(
  'assetcare-assets',
  () => [...mockAssets],
  2
)
 
  /*
  |--------------------------------------------------------------------------
  | HELPERS
  |--------------------------------------------------------------------------
  */

  const displayValue = (
    value:
      string |
      number |
      null |
      undefined
  ) => {

    if (
      value === null ||
      value === undefined ||
      String(value).trim() === ''
    ) {

      return '—'
    }


    return String(value)
  }


  const createChange = (
    field: string,
    label: string,
    oldValue:
      string |
      number |
      null |
      undefined,
    newValue:
      string |
      number |
      null |
      undefined
  ): AssetHistoryChange | null => {

    const before =
      displayValue(oldValue)

    const after =
      displayValue(newValue)


    if (before === after) {
      return null
    }


    return {
      field,
      label,

      oldValue:
        before,

      newValue:
        after
    }
  }


  const recordHistory = (
    asset: Asset,
    actor: AssetMutationActor,
    action:
      'Created' |
      'Master Updated' |
      'Operational Updated' |
      'Moved',
    summary: string,
    changes:
      AssetHistoryChange[] = []
  ) => {

    addAssetHistoryEvent({

      assetId:
        asset.assetId,

      hospitalId:
        asset.hospitalId,

      action,

      actorId:
        actor.id,

      actorName:
        actor.name,

      summary,

      changes
    })
  }


  /*
  |--------------------------------------------------------------------------
  | LOOKUPS
  |--------------------------------------------------------------------------
  */

  const getAssetById = (
    id: number
  ) => {

    return (
      assets.value.find(
        asset =>
          asset.id === id
      ) ?? null
    )
  }


  const getAssetByAssetId = (
    assetId: string
  ) => {

    const normalized =
      assetId
        .trim()
        .toUpperCase()


    return (
      assets.value.find(
        asset =>
          asset.assetId ===
          normalized
      ) ?? null
    )
  }


  /*
  |--------------------------------------------------------------------------
  | GENERATED ASSET ID
  |--------------------------------------------------------------------------
  */

  const generateAssetId = () => {

    const highestNumber =
      assets.value.reduce(
        (
          highest,
          asset
        ) => {

          const match =
            asset.assetId.match(
              /^AC-AST-(\d+)$/
            )


          if (!match) {
            return highest
          }


          return Math.max(
            highest,
            Number(match[1])
          )
        },
        0
      )


    return (
      `AC-AST-${String(
        highestNumber + 1
      ).padStart(4, '0')}`
    )
  }


  const validateAssetAssignment = (
    departmentId: string,
    locationId: number,
    requireActive = false
  ): string | null => {

    const department =
      getDepartmentById(
        departmentId
      )

    if (!department) {
      return 'Selected department was not found.'
    }

    const location =
      getLocationById(
        locationId
      )

    if (!location) {
      return 'Selected location was not found.'
    }

    if (
      location.departmentId !==
      departmentId
    ) {
      return 'Selected location does not belong to the selected department.'
    }

    if (
      requireActive &&
      department.status !== 'Active'
    ) {
      return 'Assets can only be assigned to an active department.'
    }

    if (
      requireActive &&
      location.status !== 'Active'
    ) {
      return 'Assets can only be assigned to an active location.'
    }

    return null
  }


  /*
  |--------------------------------------------------------------------------
  | VALIDATION
  |--------------------------------------------------------------------------
  */

  const validateAsset = (
    payload: AssetFormPayload,
    editingId?: number
  ): string | null => {

    if (!payload.name.trim()) {

      return (
        'Asset name is required.'
      )
    }


    if (!payload.departmentId) {

      return (
        'Department is required.'
      )
    }


    if (!payload.locationId) {

      return (
        'Location is required.'
      )
    }


    const assignmentError =
      validateAssetAssignment(
        payload.departmentId,
        payload.locationId
      )

    if (assignmentError) {
      return assignmentError
    }


    if (
      payload.serialNumber.trim()
    ) {

      const normalizedSerial =
        payload.serialNumber
          .trim()
          .toLowerCase()


      const duplicate =
        assets.value.find(
          asset =>
            asset.serialNumber
              .trim()
              .toLowerCase() ===
              normalizedSerial &&

            asset.id !==
              editingId
        )


      if (duplicate) {

        return (
          `Serial number already belongs to ${duplicate.assetId}.`
        )
      }
    }


    if (
      payload.purchaseDate &&
      payload.warrantyExpiry &&
      payload.warrantyExpiry <
        payload.purchaseDate
    ) {

      return (
        'Warranty expiry cannot be earlier than the purchase date.'
      )
    }


    if (
      payload.lastMaintenanceDate &&
      payload.nextMaintenanceDate &&
      payload.nextMaintenanceDate <
        payload.lastMaintenanceDate
    ) {

      return (
        'Next maintenance date cannot be earlier than the last maintenance date.'
      )
    }


    if (
  payload.serviceEmail.trim() &&
  !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
    payload.serviceEmail.trim()
  )
) {

      return (
        'Please enter a valid service email.'
      )
    }


    return null
  }


  /*
  |--------------------------------------------------------------------------
  | CREATE
  |--------------------------------------------------------------------------
  */

  const createAsset = (
    payload: AssetFormPayload,
    hospitalId: string,
    actor: AssetMutationActor
  ): AssetOperationResult => {

    const validationError =
      validateAsset(payload)


    if (validationError) {

      return {
        ok: false,
        message:
          validationError
      }
    }


    const activeAssignmentError =
      validateAssetAssignment(
        payload.departmentId,
        payload.locationId,
        true
      )

    if (activeAssignmentError) {
      return {
        ok: false,
        message:
          activeAssignmentError
      }
    }


    const now =
      new Date().toISOString()


    const newAsset:
      Asset = {

      id:
        Date.now(),

      assetId:
        generateAssetId(),

      hospitalId,

      name:
        payload.name.trim(),

      category:
        payload.category,

      serialNumber:
        payload.serialNumber.trim(),

      manufacturer:
        payload.manufacturer.trim(),

      model:
        payload.model.trim(),

      departmentId:
        payload.departmentId,

      locationId:
        payload.locationId,

      responsibleTeam:
        payload.responsibleTeam.trim(),

      condition:
        payload.condition,

      operationalStatus:
        payload.operationalStatus,

      lastMaintenanceDate:
        payload.lastMaintenanceDate,

      nextMaintenanceDate:
        payload.nextMaintenanceDate,

      purchaseDate:
        payload.purchaseDate,

      warrantyExpiry:
        payload.warrantyExpiry,

      vendorName:
        payload.vendorName.trim(),

      serviceContact:
        payload.serviceContact.trim(),

      serviceEmail:
        payload.serviceEmail
          .trim()
          .toLowerCase(),

      warrantyNotes:
        payload.warrantyNotes.trim(),

      description:
        payload.description.trim(),

      createdAt:
        now,

      updatedAt:
        now
    }


    if (
      getAssetByAssetId(
        newAsset.assetId
      )
    ) {

      return {
        ok: false,

        message:
          'Unable to generate a unique asset ID.'
      }
    }


    assets.value.unshift(
      newAsset
    )


    recordHistory(
      newAsset,
      actor,
      'Created',
      `Created asset ${newAsset.assetId}.`
    )


    return {
      ok: true,
      asset:
        newAsset
    }
  }


  /*
  |--------------------------------------------------------------------------
  | UPDATE MASTER DATA
  |--------------------------------------------------------------------------
  |
  | Assignment and lifecycle are intentionally protected.
  |
  */

  const updateAsset = (
    id: number,
    payload: AssetFormPayload,
    actor: AssetMutationActor,
    accessContext: AssetAccessContext
  ): AssetOperationResult => {

    const index =
      assets.value.findIndex(
        asset =>
          asset.id === id
      )


    if (index === -1) {

      return {
        ok: false,

        message:
          'Asset was not found.'
      }
    }


    const existing =
      assets.value[index]


    if (!existing) {

      return {
        ok: false,

        message:
          'Asset was not found.'
      }
    }

    if (
      !hasAssetPermission(
        accessContext.role,
        'editMaster'
      ) ||
      !canViewAssetInScope(
        accessContext.role,
        accessContext.hospitalId,
        accessContext.departmentId,
        existing
      )
    ) {
      return {
        ok: false,
        message:
          'You do not have permission to edit this asset.'
      }
    }


    /*
     * Movement must use moveAsset().
     */

    if (
      payload.departmentId !==
        existing.departmentId ||

      payload.locationId !==
        existing.locationId ||

      payload.responsibleTeam.trim() !==
        existing.responsibleTeam
    ) {

      return {
        ok: false,

        message:
          'Department, location and assignment must be changed using Move Asset.'
      }
    }


    /*
     * Lifecycle must use operational update.
     */

    if (
      payload.condition !==
        existing.condition ||

      payload.operationalStatus !==
        existing.operationalStatus
    ) {

      return {
        ok: false,

        message:
          'Condition and operational status must be changed using Update Status.'
      }
    }


    const validationError =
      validateAsset(
        payload,
        id
      )


    if (validationError) {

      return {
        ok: false,

        message:
          validationError
      }
    }


    const updatedAsset:
      Asset = {

      ...existing,

      name:
        payload.name.trim(),

      category:
        payload.category,

      serialNumber:
        payload.serialNumber.trim(),

      manufacturer:
        payload.manufacturer.trim(),

      model:
        payload.model.trim(),

      lastMaintenanceDate:
        payload.lastMaintenanceDate,

      nextMaintenanceDate:
        payload.nextMaintenanceDate,

      purchaseDate:
        payload.purchaseDate,

      warrantyExpiry:
        payload.warrantyExpiry,

      vendorName:
        payload.vendorName.trim(),

      serviceContact:
        payload.serviceContact.trim(),

      serviceEmail:
        payload.serviceEmail
          .trim()
          .toLowerCase(),

      warrantyNotes:
        payload.warrantyNotes.trim(),

      description:
        payload.description.trim(),

      updatedAt:
        new Date().toISOString()
    }


    const changes =
      [
        createChange(
          'name',
          'Asset Name',
          existing.name,
          updatedAsset.name
        ),

        createChange(
          'category',
          'Category',
          existing.category,
          updatedAsset.category
        ),

        createChange(
          'serialNumber',
          'Serial Number',
          existing.serialNumber,
          updatedAsset.serialNumber
        ),

        createChange(
          'manufacturer',
          'Manufacturer',
          existing.manufacturer,
          updatedAsset.manufacturer
        ),

        createChange(
          'model',
          'Model',
          existing.model,
          updatedAsset.model
        ),

        createChange(
          'lastMaintenanceDate',
          'Last Maintenance Date',
          existing.lastMaintenanceDate,
          updatedAsset.lastMaintenanceDate
        ),

        createChange(
          'nextMaintenanceDate',
          'Next Maintenance Date',
          existing.nextMaintenanceDate,
          updatedAsset.nextMaintenanceDate
        ),

        createChange(
          'purchaseDate',
          'Purchase Date',
          existing.purchaseDate,
          updatedAsset.purchaseDate
        ),

        createChange(
          'warrantyExpiry',
          'Warranty Expiry',
          existing.warrantyExpiry,
          updatedAsset.warrantyExpiry
        ),

        createChange(
          'vendorName',
          'Vendor',
          existing.vendorName,
          updatedAsset.vendorName
        ),

        createChange(
          'serviceContact',
          'Service Contact',
          existing.serviceContact,
          updatedAsset.serviceContact
        ),

        createChange(
          'serviceEmail',
          'Service Email',
          existing.serviceEmail,
          updatedAsset.serviceEmail
        ),

        createChange(
          'warrantyNotes',
          'Warranty Notes',
          existing.warrantyNotes,
          updatedAsset.warrantyNotes
        ),

        createChange(
          'description',
          'Description',
          existing.description,
          updatedAsset.description
        )
      ].filter(
        (
          change
        ): change is AssetHistoryChange =>
          Boolean(change)
      )


    assets.value[index] =
      updatedAsset


    if (changes.length) {

      recordHistory(
        updatedAsset,
        actor,
        'Master Updated',
        `Updated master information for ${updatedAsset.assetId}.`,
        changes
      )
    }


    return {
      ok: true,

      asset:
        updatedAsset
    }
  }


  /*
  |--------------------------------------------------------------------------
  | OPERATIONAL UPDATE
  |--------------------------------------------------------------------------
  */

  const updateAssetOperationalState = (
    id: number,
    payload:
      AssetOperationalUpdatePayload,
    actor:
      AssetMutationActor,
    accessContext:
      AssetAccessContext
  ): AssetOperationResult => {

    const index =
      assets.value.findIndex(
        asset =>
          asset.id === id
      )


    if (index === -1) {

      return {
        ok: false,

        message:
          'Asset was not found.'
      }
    }


    const existing =
      assets.value[index]


    if (!existing) {

      return {
        ok: false,

        message:
          'Asset was not found.'
      }
    }


    if (
      !getAllowedOperationalStatuses(
        accessContext.role
      ).includes(
        payload.operationalStatus
      )
    ) {
      return {
        ok: false,
        message:
          'Your role cannot apply this lifecycle status.'
      }
    }


    const updatedAsset:
      Asset = {

      ...existing,

      condition:
        payload.condition,

      operationalStatus:
        payload.operationalStatus,

      updatedAt:
        new Date().toISOString()
    }


    const changes =
      [
        createChange(
          'condition',
          'Condition',
          existing.condition,
          updatedAsset.condition
        ),

        createChange(
          'operationalStatus',
          'Operational Status',
          existing.operationalStatus,
          updatedAsset.operationalStatus
        )
      ].filter(
        (
          change
        ): change is AssetHistoryChange =>
          Boolean(change)
      )


    assets.value[index] =
      updatedAsset


    if (changes.length) {

      recordHistory(
        updatedAsset,
        actor,
        'Operational Updated',
        `Updated condition or lifecycle for ${updatedAsset.assetId}.`,
        changes
      )
    }


    return {
      ok: true,

      asset:
        updatedAsset
    }
  }


  /*
  |--------------------------------------------------------------------------
  | MOVE ASSET
  |--------------------------------------------------------------------------
  */

  const moveAsset = (
    id: number,
    payload: AssetMovePayload,
    actor: AssetMutationActor,
    accessContext: AssetAccessContext
  ): AssetOperationResult => {

    const index =
      assets.value.findIndex(
        asset =>
          asset.id === id
      )


    if (index === -1) {

      return {
        ok: false,

        message:
          'Asset was not found.'
      }
    }


    const existing =
      assets.value[index]


    if (!existing) {

      return {
        ok: false,

        message:
          'Asset was not found.'
      }
    }


    if (
      !canMoveAssetInContext(
        accessContext,
        existing,
        payload.departmentId
      )
    ) {
      return {
        ok: false,
        message:
          'You do not have permission to move this asset.'
      }
    }


    const assignmentError =
      validateAssetAssignment(
        payload.departmentId,
        payload.locationId,
        true
      )

    if (assignmentError) {
      return {
        ok: false,
        message:
          assignmentError
      }
    }


    const department =
      getDepartmentById(
        payload.departmentId
      )

    const location =
      getLocationById(
        payload.locationId
      )

    if (!department || !location) {
      return {
        ok: false,
        message:
          'Selected department or location was not found.'
      }
    }


    const oldDepartment =
      getDepartmentById(
        existing.departmentId
      )


    const oldLocation =
      getLocationById(
        existing.locationId
      )


    const updatedAsset:
      Asset = {

      ...existing,

      departmentId:
        payload.departmentId,

      locationId:
        payload.locationId,

      responsibleTeam:
        payload.responsibleTeam
          .trim(),

      updatedAt:
        new Date().toISOString()
    }


    const changes =
      [
        createChange(
          'departmentId',
          'Department',
          oldDepartment?.name,
          department.name
        ),

        createChange(
          'locationId',
          'Location',
          oldLocation?.name,
          location.name
        ),

        createChange(
          'responsibleTeam',
          'Responsible Team',
          existing.responsibleTeam,
          updatedAsset.responsibleTeam
        )
      ].filter(
        (
          change
        ): change is AssetHistoryChange =>
          Boolean(change)
      )


    if (!changes.length) {

      return {
        ok: false,

        message:
          'Select a different location, department or assignment before moving the asset.'
      }
    }


    assets.value[index] =
      updatedAsset


    recordHistory(
      updatedAsset,
      actor,
      'Moved',
      `Moved ${updatedAsset.assetId}.`,
      changes
    )


    return {
      ok: true,

      asset:
        updatedAsset
    }
  }


  return {
    assets,

    getAssetById,
    getAssetByAssetId,

    generateAssetId,

    createAsset,
    updateAsset,

    updateAssetOperationalState,

    moveAsset
  }
}