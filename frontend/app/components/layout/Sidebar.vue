<script setup lang="ts">
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
  scopeLabel
} = useAppNavigation()

const isActive = (
  to: string
) => {
  return (
    route.path === to ||
    (
      to !== '/' &&
      route.path.startsWith(
        `${to}/`
      )
    )
  )
}
</script>

<template>
  <aside
    class="
      hidden
      w-64
      shrink-0
      flex-col
      bg-primary
      text-white
      lg:flex
    "
  >

    <!-- Logo -->
    <div
      class="
        border-b
        border-white/10
        px-5
        pb-5
        pt-6
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

        <div class="min-w-0">

          <h1
            class="
              text-lg
              font-bold
            "
          >
            AssetCare
          </h1>

          <p
            class="
              truncate
              text-[10px]
              uppercase
              tracking-wider
              text-blue-100
            "
          >
            Hospital Asset Management
          </p>

        </div>
      </div>
    </div>


    <!-- Logged User -->
    <div
      class="
        border-b
        border-white/10
        px-5
        py-4
      "
    >

      <p
        class="
          truncate
          text-sm
          font-semibold
        "
      >
        {{
          user?.name ||
          'AssetCare User'
        }}
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
          truncate
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
        mt-4
        flex-1
        px-3
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
          py-2.5
          text-sm
          transition
        "

        :class="
          isActive(item.to)
            ? 'bg-white/15 font-semibold text-white'
            : 'text-blue-50 hover:bg-white/10'
        "
      >

        <span
          class="
            w-5
            text-center
            text-base
          "
        >
          {{ item.icon }}
        </span>

        <span>
          {{ item.label }}
        </span>

      </NuxtLink>

    </nav>


    <!-- Logout -->
    <div
      class="
        border-t
        border-white/10
        px-3
        py-4
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
          py-2.5
          text-sm
          text-blue-50
          transition
          hover:bg-white/10
        "

        @click="logout"
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
</template>