import {
  defineNuxtRouteMiddleware,
  navigateTo
} from '#app'

import {
  useAuth
} from '~/composables/useAuth'

import {
  canRoleAccessPath,
  getRoleHome,
  isPublicRoute
} from '~/config/permissions'

export default defineNuxtRouteMiddleware(
  (to) => {

    const {
      isAuthenticated,
      userRole
    } = useAuth()

    const publicRoute =
      isPublicRoute(to.path)

    /*
    |--------------------------------------------------------------------------
    | 1. LOGGED OUT USER
    |--------------------------------------------------------------------------
    |
    | Protected route open kare to login par redirect.
    |
    */

    if (
      !isAuthenticated.value &&
      !publicRoute
    ) {
      return navigateTo({
        path: '/auth/login',

        query:
          to.path !== '/'
            ? {
                redirect:
                  to.fullPath
              }
            : undefined
      })
    }

    /*
    |--------------------------------------------------------------------------
    | 2. LOGGED-IN USER OPENING AUTH PAGE
    |--------------------------------------------------------------------------
    |
    | Login/register page dobara open kare to apne dashboard par jaye.
    |
    */

    if (
      isAuthenticated.value &&
      publicRoute
    ) {

      if (userRole.value) {
        return navigateTo(
          getRoleHome(
            userRole.value
          )
        )
      }

      return navigateTo(
        '/auth/login'
      )
    }

    /*
    |--------------------------------------------------------------------------
    | 3. PUBLIC PAGE
    |--------------------------------------------------------------------------
    */

    if (
      !isAuthenticated.value
    ) {
      return
    }

    /*
    |--------------------------------------------------------------------------
    | 4. INVALID SESSION
    |--------------------------------------------------------------------------
    |
    | Token/user hai lekin role missing hai.
    |
    */

    if (!userRole.value) {
      return navigateTo(
        '/auth/login'
      )
    }

    /*
    |--------------------------------------------------------------------------
    | 5. STRICT ROLE BASED ACCESS CONTROL
    |--------------------------------------------------------------------------
    |
    | Example:
    |
    | Nurse → /admin/departments
    | Manager → /dashboard/nurse
    | Admin → /dashboard/manager
    |
    | Result:
    | /access-denied
    |
    */

    if (
      !canRoleAccessPath(
        userRole.value,
        to.path
      )
    ) {
      return navigateTo({
        path:
          '/access-denied',

        query: {
          from:
            to.fullPath
        }
      })
    }
  }
)