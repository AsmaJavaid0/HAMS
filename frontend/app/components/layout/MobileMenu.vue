<script setup lang="ts">
import {
  watch
} from 'vue'

import {
  useRoute
} from '#app'

import {
  useAuth
} from '~/composables/useAuth'

import {
  useAppNavigation
} from '~/composables/useAppNavigation'

const route =
  useRoute()

const {
  user,
  logout
} = useAuth()

const {
  menuItems,

  roleLabel,
  scopeLabel,

  isMobileMenuOpen,
  closeMobileMenu

} = useAppNavigation()

/*
|--------------------------------------------------------------------------
| CLOSE MENU AFTER ROUTE CHANGE
|--------------------------------------------------------------------------
*/

watch(
  () => route.fullPath,

  () => {
    closeMobileMenu()
  }
)

/*
|--------------------------------------------------------------------------
| LOGOUT
|--------------------------------------------------------------------------
*/

const handleLogout =
  async () => {

    closeMobileMenu()

    await logout()
  }
</script>

<template>

  <Teleport to="body">

    <div
      v-if="isMobileMenuOpen"

      class="
        fixed
        inset-0
        z-[100]
        lg:hidden
      "
    >

      <!-- Background Overlay -->
      <button
        type="button"

        class="
          absolute
          inset-0
          bg-black/40
        "

        aria-label="Close navigation menu"

        @click="closeMobileMenu"
      />


      <!-- Drawer -->
      <aside
        class="
          relative
          flex
          h-full
          w-[86%]
          max-w-sm
          flex-col
          bg-primary
          text-white
          shadow-2xl
        "
      >

        <!-- Header -->
        <div
          class="
            flex
            items-center
            justify-between
            border-b
            border-white/10
            px-5
            py-5
          "
        >

          <div
            class="
              flex
              items-center
              gap-3
            "
          >

            <img
              src="/logo/asset%20care%20logo.png"

              alt="AssetCare logo"

              class="
                h-10
                w-10
                rounded-lg
                bg-white
                object-contain
                p-1
              "
            />

            <div>

              <h2 class="font-bold">
                AssetCare
              </h2>

              <p
                class="
                  text-[10px]
                  uppercase
                  tracking-wide
                  text-blue-100
                "
              >
                Hospital Asset Management
              </p>

            </div>

          </div>


          <!-- Close -->
          <button
            type="button"

            class="
              flex
              h-9
              w-9
              items-center
              justify-center
              rounded-lg
              text-2xl
              text-blue-50
              hover:bg-white/10
            "

            aria-label="Close navigation menu"

            @click="closeMobileMenu"
          >
            ×
          </button>

        </div>


        <!-- User -->
        <div
          class="
            border-b
            border-white/10
            px-5
            py-4
          "
        >

          <p class="font-semibold">
            {{ user?.name }}
          </p>

          <p
            class="
              mt-0.5
              text-xs
              text-blue-100
            "
          >
            {{ roleLabel }}
          </p>

          <p
            class="
              mt-1
              text-[11px]
              text-blue-200
            "
          >
            {{ scopeLabel }}
          </p>

        </div>


        <!-- Navigation -->
        <nav
          class="
            flex-1
            overflow-y-auto
            px-3
            py-4
          "
        >

          <NuxtLink
            v-for="item in menuItems"

            :key="item.to"

            :to="item.to"

            class="
              mb-1
              flex
              items-center
              gap-3
              rounded-lg
              px-4
              py-3
              text-sm
              text-blue-50
              transition
              hover:bg-white/10
            "

            active-class="
              bg-white/15
              font-semibold
              text-white
            "
          >

            <span
              class="
                w-5
                text-center
              "
            >
              {{ item.icon }}
            </span>

            {{ item.label }}

          </NuxtLink>

        </nav>


        <!-- Logout -->
        <div
          class="
            border-t
            border-white/10
            p-3
          "
        >

          <button
            type="button"

            class="
              flex
              w-full
              items-center
              gap-3
              rounded-lg
              px-4
              py-3
              text-sm
              text-blue-50
              hover:bg-white/10
            "

            @click="handleLogout"
          >

            <span
              class="
                w-5
                text-center
              "
            >
              ⇥
            </span>

            Logout

          </button>

        </div>

      </aside>

    </div>

  </Teleport>

</template>