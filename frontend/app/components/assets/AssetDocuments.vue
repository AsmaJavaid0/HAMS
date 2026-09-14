<script setup lang="ts">

import {
  ASSET_DOCUMENT_TYPES
} from '~/types/asset-document'

import type {
  AssetDocument,
  AssetDocumentType,
  AssetDocumentUploadPayload
} from '~/types/asset-document'


defineProps<{
  documents: AssetDocument[]

  canManage: boolean
}>()


const emit = defineEmits<{
  upload: [
    payload:
      AssetDocumentUploadPayload
  ]
}>()


const documentType =
  ref<AssetDocumentType>(
    'Manual'
  )


const selectedFile =
  ref<File | null>(
    null
  )


const errorMessage =
  ref('')


const fileInputKey =
  ref(0)


const handleFileChange = (
  event: Event
) => {

  const input =
    event.target as HTMLInputElement


  selectedFile.value =
    input.files?.[0] ??
    null


  errorMessage.value = ''
}


const uploadDocument = () => {

  errorMessage.value = ''


  if (!selectedFile.value) {

    errorMessage.value =
      'Select a file first.'

    return
  }


  const file =
    selectedFile.value


  /*
   * Browser-session preview only.
   *
   * Later this becomes a real
   * Supabase Storage public/signed URL.
   */

  const previewUrl =
    import.meta.client
      ? URL.createObjectURL(file)
      : null


  emit('upload', {

    fileName:
      file.name,

    documentType:
      documentType.value,

    mimeType:
      file.type ||
      'application/octet-stream',

    sizeBytes:
      file.size,

    previewUrl
  })


  selectedFile.value =
    null

  documentType.value =
    'Manual'

  fileInputKey.value += 1
}


const formatSize = (
  bytes: number
) => {

  if (bytes < 1024) {
    return `${bytes} B`
  }


  if (
    bytes <
    1024 * 1024
  ) {

    return (
      `${(
        bytes / 1024
      ).toFixed(1)} KB`
    )
  }


  return (
    `${(
      bytes /
      (1024 * 1024)
    ).toFixed(1)} MB`
  )
}


const formatDate = (
  value: string
) => {

  return new Date(
    value
  ).toLocaleString(
    'en-AU',
    {
      dateStyle:
        'medium',

      timeStyle:
        'short'
    }
  )
}

</script>


<template>

  <section
    class="rounded-xl border border-gray-200 bg-white"
  >

    <!-- Header -->

    <div
      class="border-b border-gray-200 px-6 py-5"
    >

      <h2
        class="text-lg font-semibold text-text-primary"
      >
        Asset Documents
      </h2>

      <p
        class="mt-1 text-sm text-text-secondary"
      >
        Photos, manuals, warranty and service documents related to this asset.
      </p>

    </div>


    <!-- Demo Storage Notice -->

    <div
      class="mx-6 mt-5 rounded-lg border border-amber-100 bg-amber-50 px-4 py-3 text-xs leading-5 text-amber-700"
    >
      Frontend demo mode: uploaded files are previewable during this browser session, but file bytes are not persisted yet. Supabase Storage will provide permanent storage later.
    </div>


    <!-- Upload -->

    <div
      v-if="canManage"
      class="border-b border-gray-100 p-6"
    >

      <h3
        class="text-sm font-semibold text-text-primary"
      >
        Add Document
      </h3>


      <div
        class="mt-4 grid gap-3 md:grid-cols-[180px_1fr_auto]"
      >

        <select
          v-model="documentType"
          class="rounded-lg border border-gray-300 bg-white px-3 py-2.5 text-sm"
        >

          <option
            v-for="type in ASSET_DOCUMENT_TYPES"
            :key="type"
            :value="type"
          >
            {{ type }}
          </option>

        </select>


        <input
          :key="fileInputKey"
          type="file"
          accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
          class="rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm"
          @change="handleFileChange"
        />


        <button
          type="button"
          class="rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
          @click="uploadDocument"
        >
          Upload
        </button>

      </div>


      <p
        v-if="errorMessage"
        class="mt-2 text-xs text-red-500"
      >
        {{ errorMessage }}
      </p>

    </div>


    <!-- Documents -->

    <div
      v-if="documents.length"
      class="divide-y divide-gray-100"
    >

      <div
        v-for="document in documents"
        :key="document.id"
        class="flex flex-col gap-3 px-6 py-4 sm:flex-row sm:items-center sm:justify-between"
      >

        <div class="min-w-0">

          <div
            class="flex flex-wrap items-center gap-2"
          >

            <p
              class="truncate text-sm font-semibold text-text-primary"
            >
              {{ document.fileName }}
            </p>


            <span
              class="rounded-full bg-blue-50 px-2 py-1 text-xs font-medium text-primary"
            >
              {{ document.documentType }}
            </span>

          </div>


          <p
            class="mt-1 text-xs text-gray-400"
          >
            {{ formatSize(document.sizeBytes) }}
            ·
            {{ document.uploadedByName }}
            ·
            {{ formatDate(document.uploadedAt) }}
          </p>

        </div>


        <a
          v-if="document.previewUrl"
          :href="document.previewUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="shrink-0 text-sm font-medium text-primary hover:underline"
        >
          View
        </a>


        <span
          v-else
          class="shrink-0 text-xs text-gray-400"
        >
          Storage preview unavailable
        </span>

      </div>

    </div>


    <div
      v-else
      class="px-6 py-10 text-center text-sm text-gray-500"
    >
      No documents have been attached to this asset.
    </div>

  </section>

</template>