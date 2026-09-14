<script setup lang="ts">
import {
  navigateTo
} from '#app'

import {
  useAuth
} from '~/composables/useAuth'

import {
  getRoleHome
} from '~/config/permissions'

const {
  isAuthenticated,
  userRole
} = useAuth()

/*
|--------------------------------------------------------------------------
| ROOT REDIRECT
|--------------------------------------------------------------------------
|
| Logged in:
|     role dashboard
|
| Logged out:
|     login
|
*/

if (
  isAuthenticated.value &&
  userRole.value
) {

  await navigateTo(
    getRoleHome(
      userRole.value
    )
  )

} else {

  await navigateTo(
    '/auth/login'
  )

}
</script>

<template>

  <div
    class="
      flex
      min-h-screen
      items-center
      justify-center
      bg-background
    "
  >

    <p
      class="
        text-sm
        text-gray-500
      "
    >
      Redirecting…
    </p>

  </div>

</template>