<script setup lang="ts">
import {
  computed
} from 'vue'

import {
  useAuth
} from '~/composables/useAuth'

import {
  getRoleHome,
  getRoleLabel
} from '~/config/permissions'

definePageMeta({
  layout: 'default'
})

const {
  user,
  userRole,
  logout
} = useAuth()

/*
|--------------------------------------------------------------------------
| DASHBOARD
|--------------------------------------------------------------------------
*/

const dashboardPath =
  computed(() => {

    if (!userRole.value) {
      return '/auth/login'
    }

    return getRoleHome(
      userRole.value
    )
  })

/*
|--------------------------------------------------------------------------
| ROLE LABEL
|--------------------------------------------------------------------------
*/

const roleLabel =
  computed(() => {

    if (!userRole.value) {
      return 'User'
    }

    return getRoleLabel(
      userRole.value
    )
  })
</script>

<template>

  <div
    class="
      relative
      flex
      min-h-screen
      items-center
      justify-center
      overflow-hidden
      bg-background
      px-4
      py-10
    "
  >

    <!-- Background -->
    <div
      class="
        pointer-events-none
        absolute
        -left-32
        -top-32
        h-80
        w-80
        rounded-full
        bg-primary/10
        blur-3xl
      "
    />

    <div
      class="
        pointer-events-none
        absolute
        -bottom-40
        -right-32
        h-96
        w-96
        rounded-full
        bg-blue-200/40
        blur-3xl
      "
    />


    <!-- Card Wrapper -->
    <div
      class="
        relative
        z-10
        w-full
        max-w-lg
      "
    >

      <div
        class="
          rounded-2xl
          border
          border-gray-200
          bg-white
          p-7
          text-center
          shadow-xl
          sm:p-10
        "
      >

        <!-- Logo -->
        <div
          class="
            mx-auto
            flex
            h-16
            w-16
            items-center
            justify-center
            rounded-2xl
            bg-blue-50
          "
        >

          <img
            src="/logo/asset%20care%20logo.png"

            alt="AssetCare logo"

            class="
              h-12
              w-12
              object-contain
            "
          />

        </div>


        <!-- Error -->
        <div
          class="
            mx-auto
            mt-7
            inline-flex
            items-center
            rounded-full
            bg-red-50
            px-3
            py-1
            text-xs
            font-semibold
            uppercase
            tracking-wide
            text-red-600
          "
        >
          Error 403
        </div>


        <h1
          class="
            mt-4
            text-3xl
            font-bold
            text-text-primary
          "
        >
          Access Denied
        </h1>


        <p
          class="
            mx-auto
            mt-3
            max-w-md
            text-sm
            leading-6
            text-text-secondary
          "
        >
          You do not have permission to access this area of AssetCare.
          Access is limited by your assigned hospital role and scope.
        </p>


        <!-- Current User -->
        <div
          class="
            mt-6
            rounded-xl
            border
            border-gray-200
            bg-gray-50
            px-4
            py-3
          "
        >

          <p
            class="
              text-xs
              font-medium
              uppercase
              tracking-wide
              text-gray-400
            "
          >
            Signed in as
          </p>

          <p
            class="
              mt-1
              text-sm
              font-semibold
              text-text-primary
            "
          >
            {{ user?.name }}
            ·
            {{ roleLabel }}
          </p>

        </div>


        <!-- Actions -->
        <div
          class="
            mt-7
            flex
            flex-col
            gap-3
            sm:flex-row
          "
        >

          <NuxtLink
            :to="dashboardPath"

            class="
              flex
              h-11
              flex-1
              items-center
              justify-center
              rounded-lg
              bg-primary
              px-5
              text-sm
              font-semibold
              text-white
              transition
              hover:opacity-90
            "
          >
            Return to Dashboard
          </NuxtLink>


          <button
            type="button"

            class="
              h-11
              flex-1
              rounded-lg
              border
              border-gray-300
              bg-white
              px-5
              text-sm
              font-semibold
              text-gray-700
              transition
              hover:bg-gray-50
            "

            @click="logout"
          >
            Sign Out
          </button>

        </div>

      </div>


      <!-- Footer -->
      <p
        class="
          mt-5
          text-center
          text-xs
          text-text-secondary
        "
      >
        AssetCare · Hospital Asset Management System
      </p>

    </div>

  </div>

</template>