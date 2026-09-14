import {
  computed
} from 'vue'

import {
  useState
} from '#app'

import {
  NAVIGATION_BY_ROLE
} from '~/config/navigation'

import {
  getRoleLabel
} from '~/config/permissions'

import {
  useAuth
} from '~/composables/useAuth'

export const useAppNavigation = () => {

  const {
    user,
    userRole
  } = useAuth()

  /*
  |--------------------------------------------------------------------------
  | MOBILE MENU STATE
  |--------------------------------------------------------------------------
  */

  const isMobileMenuOpen =
    useState<boolean>(
      'assetcare-mobile-menu-open',
      () => false
    )

  /*
  |--------------------------------------------------------------------------
  | ROLE NAVIGATION
  |--------------------------------------------------------------------------
  */

  const menuItems =
    computed(() => {

      if (!userRole.value) {
        return []
      }

      return NAVIGATION_BY_ROLE[
        userRole.value
      ]
    })

  /*
  |--------------------------------------------------------------------------
  | ROLE LABEL
  |--------------------------------------------------------------------------
  */

  const roleLabel =
    computed(() => {

      if (!userRole.value) {
        return ''
      }

      return getRoleLabel(
        userRole.value
      )
    })

  /*
  |--------------------------------------------------------------------------
  | ACCESS SCOPE LABEL
  |--------------------------------------------------------------------------
  */

  const scopeLabel =
    computed(() => {

      if (!user.value) {
        return ''
      }

      if (
        user.value.scope ===
        'hospital'
      ) {
        return (
          user.value.hospital_name ??
          'Hospital-wide access'
        )
      }

      return (
        user.value.department_name ??
        'Department access'
      )
    })

  /*
  |--------------------------------------------------------------------------
  | MOBILE MENU ACTIONS
  |--------------------------------------------------------------------------
  */

  const openMobileMenu = () => {
    isMobileMenuOpen.value = true
  }

  const closeMobileMenu = () => {
    isMobileMenuOpen.value = false
  }

  const toggleMobileMenu = () => {
    isMobileMenuOpen.value =
      !isMobileMenuOpen.value
  }

  return {
    menuItems,

    roleLabel,
    scopeLabel,

    isMobileMenuOpen,

    openMobileMenu,
    closeMobileMenu,
    toggleMobileMenu
  }
}