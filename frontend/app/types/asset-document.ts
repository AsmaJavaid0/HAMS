export const ASSET_DOCUMENT_TYPES = [
  'Photo',
  'Manual',
  'Warranty Document',
  'Service Document',
  'Other'
] as const

export type AssetDocumentType =
  typeof ASSET_DOCUMENT_TYPES[number]

export interface AssetDocument {
  id: string

  assetId: string
  hospitalId: string

  fileName: string
  documentType: AssetDocumentType

  mimeType: string
  sizeBytes: number

  uploadedById: string
  uploadedByName: string
  uploadedAt: string

  /*
   * Frontend demo only.
   * Later previewUrl comes from Supabase Storage.
   */
  previewUrl: string | null

  /*
   * Reserved for backend/storage integration.
   */
  storagePath: string | null
}

export interface AssetDocumentUploadPayload {
  fileName: string

  documentType: AssetDocumentType

  mimeType: string
  sizeBytes: number

  previewUrl: string | null
}