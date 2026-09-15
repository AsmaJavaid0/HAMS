import { computed, nextTick, ref } from 'vue'
import { $fetch } from 'ofetch'

import {
  navigateTo,
  useCookie,
  useRuntimeConfig,
  useState
} from '#app'

import type {
  User,
  UserRole
} from '~/types/auth'

import {
  getRoleHome
} from '~/config/permissions'

type BackendLoginResponse = {
  access_token: string
  user: {
    id: number
    hospital_id: number
    hospital_name: string
    full_name: string
    email: string
    role: UserRole
    department_id: number | null
  }
}

export const useAuth = () => {

  const errorMessage = ref('')

  /*
  |--------------------------------------------------------------------------
  | SESSION
  |--------------------------------------------------------------------------
  */

  const tokenCookie =
    useCookie<string | null>(
      'auth_token',
      {
        maxAge:
          60 * 60 * 24 * 7,

        sameSite: 'lax'
      }
    )

  const userCookie =
    useCookie<User | null>(
      'auth_user',
      {
        maxAge:
          60 * 60 * 24 * 7,

        sameSite: 'lax'
      }
    )

  const token =
    useState<string | null>(
      'auth-token',
      () => tokenCookie.value
    )

  const user =
    useState<User | null>(
      'auth-user',
      () => userCookie.value
    )

  /*
  |--------------------------------------------------------------------------
  | AUTH STATE
  |--------------------------------------------------------------------------
  */

  const isAuthenticated =
    computed(() => {
      return Boolean(
        token.value &&
        user.value
      )
    })

  const userRole =
    computed<UserRole | null>(
      () =>
        user.value?.role ?? null
    )

  /*
  |--------------------------------------------------------------------------
  | LOGIN
  |--------------------------------------------------------------------------
  */

  const login = async (
    email: string,
    password: string
  ): Promise<boolean> => {

    const apiBase =
      useRuntimeConfig().public.apiBase

    try {
      errorMessage.value = ''

      const response =
        await $fetch<BackendLoginResponse>(
          '/api/auth/login',
          {
            baseURL: apiBase,
            method: 'POST',
            body: { email, password }
          }
        )

      token.value = response.access_token
      tokenCookie.value = response.access_token

      user.value = {
        id: String(response.user.id),
        name: response.user.full_name,
        email: response.user.email,
        role: response.user.role,
        hospital_id: String(response.user.hospital_id),
        hospital_name: response.user.hospital_name,
        department_id: response.user.department_id === null
          ? null
          : String(response.user.department_id),
        scope: response.user.role === 'nurse'
          ? 'department'
          : 'hospital'
      }
      userCookie.value = user.value

      await nextTick()

      await navigateTo(
        getRoleHome(response.user.role)
      )

      return true
    } catch (error: any) {
      token.value = null
      user.value = null
      tokenCookie.value = null
      userCookie.value = null
      errorMessage.value =
        error?.data?.detail ??
        error?.message ??
        'Unable to reach the authentication service.'

      return false
    }

  }

  /*
  |--------------------------------------------------------------------------
  | LOGOUT
  |--------------------------------------------------------------------------
  */

  const logout = async () => {
    token.value = null
    user.value = null
    tokenCookie.value = null
    userCookie.value = null

    await navigateTo(
      '/auth/login'
    )
  }

  /*
  |--------------------------------------------------------------------------
  | DASHBOARD HELPER
  |--------------------------------------------------------------------------
  */

  const goToDashboard =
    async () => {

      if (!userRole.value) {
        await navigateTo(
          '/auth/login'
        )

        return
      }

      await navigateTo(
        getRoleHome(
          userRole.value
        )
      )
    }

  return {
    user,
    token,

    isAuthenticated,
    userRole,
    errorMessage,

    login,
    logout,

    goToDashboard
  }
}
