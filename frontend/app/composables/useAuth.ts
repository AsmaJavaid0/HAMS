import { computed } from 'vue'

import {
  navigateTo,
  useCookie
} from '#app'

import type {
  User,
  UserRole
} from '~/types/auth'

import {
  getRoleHome
} from '~/config/permissions'

type DemoAccount = {
  password: string
  user: User
}

/*
|--------------------------------------------------------------------------
| DEMO ACCOUNTS
|--------------------------------------------------------------------------
|
| Backend / Supabase abhi connected nahi hai.
| Is liye Sprint 1 frontend testing ke liye fixed demo accounts use
| kar rahe hain.
|
| Later sirf login implementation replace hogi.
| UI aur RBAC architecture same rahega.
|
*/

const DEMO_ACCOUNTS:
Record<string, DemoAccount> = {

  /*
  |--------------------------------------------------------------------------
  | ADMIN
  |--------------------------------------------------------------------------
  */

  'admin@assetcare.test': {
    password: 'Demo@123',

    user: {
      id: 'usr-admin-001',

      name: 'Sarah Mitchell',

      email: 'admin@assetcare.test',

      role: 'admin',

      hospital_id: 'hosp-001',

      hospital_name:
        'AssetCare Demo Hospital',

      department_id: null,

      department_name: null,

      scope: 'hospital'
    }
  },

  /*
  |--------------------------------------------------------------------------
  | MANAGER
  |--------------------------------------------------------------------------
  */

  'manager@assetcare.test': {
    password: 'Demo@123',

    user: {
      id: 'usr-manager-001',

      name: 'James Wilson',

      email: 'manager@assetcare.test',

      role: 'manager',

      hospital_id: 'hosp-001',

      hospital_name:
        'AssetCare Demo Hospital',

      department_id:
        'dept-icu',

      department_name:
        'Intensive Care Unit',

      scope: 'department'
    }
  },

  /*
  |--------------------------------------------------------------------------
  | BIOMEDICAL
  |--------------------------------------------------------------------------
  */

  'biomedical@assetcare.test': {
    password: 'Demo@123',

    user: {
      id: 'usr-biomedical-001',

      name: 'Daniel Kim',

      email:
        'biomedical@assetcare.test',

      role: 'biomedical',

      hospital_id:
        'hosp-001',

      hospital_name:
        'AssetCare Demo Hospital',

      department_id:
        'dept-biomedical',

      department_name:
        'Biomedical Engineering',

      scope: 'hospital'
    }
  },

  /*
  |--------------------------------------------------------------------------
  | NURSE
  |--------------------------------------------------------------------------
  */

  'nurse@assetcare.test': {
    password: 'Demo@123',

    user: {
      id: 'usr-nurse-001',

      name: 'Emily Carter',

      email:
        'nurse@assetcare.test',

      role: 'nurse',

      hospital_id:
        'hosp-001',

      hospital_name:
        'AssetCare Demo Hospital',

      department_id:
        'dept-icu',

      department_name:
        'Intensive Care Unit',

      scope: 'department'
    }
  }
}

export const useAuth = () => {

const {
  getStaffByEmail
} = useStaff()

  /*
  |--------------------------------------------------------------------------
  | SESSION
  |--------------------------------------------------------------------------
  */

  const token =
    useCookie<string | null>(
      'auth_token',
      {
        maxAge:
          60 * 60 * 24 * 7,

        sameSite: 'lax'
      }
    )

  const user =
    useCookie<User | null>(
      'auth_user',
      {
        maxAge:
          60 * 60 * 24 * 7,

        sameSite: 'lax'
      }
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

    const normalizedEmail =
      email
        .trim()
        .toLowerCase()

    const account =
      DEMO_ACCOUNTS[
        normalizedEmail
      ]

    /*
    |--------------------------------------------------------------------------
    | INVALID LOGIN
    |--------------------------------------------------------------------------
    */

    if (
      !account ||
      account.password !== password
    ) {
      token.value = null
      user.value = null

      return false
    }

    const staffProfile =
      getStaffByEmail(
        normalizedEmail
      )

    if (
      staffProfile &&
      staffProfile.status !== 'Active'
    ) {
      token.value = null
      user.value = null

      return false
    }

    /*
    |--------------------------------------------------------------------------
    | CREATE DEMO SESSION
    |--------------------------------------------------------------------------
    */

    token.value =
      `demo-token-${Date.now()}`

    user.value = {
      ...account.user
    }

    /*
    |--------------------------------------------------------------------------
    | ROLE DASHBOARD
    |--------------------------------------------------------------------------
    */

    await navigateTo(
      getRoleHome(
        account.user.role
      )
    )

    return true
  }

  /*
  |--------------------------------------------------------------------------
  | LOGOUT
  |--------------------------------------------------------------------------
  */

  const logout = async () => {
    token.value = null
    user.value = null

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

    login,
    logout,

    goToDashboard
  }
}