<script setup lang="ts">
import {
  computed
} from 'vue'

import {
  useAuth
} from '~/composables/useAuth'

import {
  useAppNavigation
} from '~/composables/useAppNavigation'

const {
  user
} = useAuth()

const {
  roleLabel,
  scopeLabel,
  toggleMobileMenu
} = useAppNavigation()

/*
|--------------------------------------------------------------------------
| USER INITIALS
|--------------------------------------------------------------------------
|
| Sarah Mitchell → SM
| James Wilson → JW
|
*/

const initials =
  computed(() => {

    const name =
      user.value?.name?.trim()

    if (!name) {
      return 'AC'
    }

    return name
      .split(/\s+/)
      .slice(0, 2)
      .map(
        part =>
          part
            .charAt(0)
            .toUpperCase()
      )
      .join('')
  })
</script>

<template>

  <header
    class="
      flex
      min-h-16
      items-center
      justify-between
      border-b
      border-gray-200
      bg-white
      px-4
      py-3
      sm:px-6
    "
  >

    <!-- Left -->
    <div
      class="
        flex
        min-w-0
        items-center
        gap-3
      "
    >

      <!-- Mobile Menu Button -->
      <button
        type="button"

        class="
          flex
          h-10
          w-10
          items-center
          justify-center
          rounded-lg
          border
          border-gray-200
          text-xl
          text-gray-600
          transition
          hover:bg-gray-50
          lg:hidden
        "

        aria-label="Open navigation menu"

        @click="toggleMobileMenu"
      >
        ☰
      </button>


      <!-- Scope -->
      <div class="min-w-0">

        <p
          class="
            text-xs
            font-medium
            uppercase
            tracking-wide
            text-gray-400
          "
        >
          Current Scope
        </p>

        <p
          class="
            truncate
            text-sm
            font-semibold
            text-gray-800
          "
        >
          {{ scopeLabel }}
        </p>

      </div>

    </div>


    <!-- Right -->
    <div
      class="
        ml-4
        flex
        items-center
        gap-3
        sm:gap-4
      "
    >

      <!-- Notifications -->
      <button
        type="button"

        class="
          hidden
          h-9
          w-9
          items-center
          justify-center
          rounded-full
          text-gray-500
          transition
          hover:bg-gray-100
          sm:flex
        "

        aria-label="Notifications"
      >
        🔔
      </button>


      <!-- User Info -->
      <div
        class="
          hidden
          text-right
          sm:block
        "
      >

        <p
          class="
            max-w-44
            truncate
            text-sm
            font-semibold
            text-gray-800
          "
        >
          {{
            user?.name ||
            'AssetCare User'
          }}
        </p>

        <p
          class="
            text-xs
            text-gray-500
          "
        >
          {{ roleLabel }}
        </p>

      </div>


      <!-- Avatar -->
      <div
        class="
          flex
          h-10
          w-10
          items-center
          justify-center
          rounded-full
          bg-primary/10
          text-sm
          font-bold
          text-primary
        "

        :title="user?.name"
      >
        {{ initials }}
      </div>

    </div>

  </header>

</template>