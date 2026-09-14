import type { UserRole } from '~/types/auth'

export const PUBLIC_ROUTES = [
  '/auth/login',
  '/auth/register',
  '/auth/forgot-password'
] as const

export const ROLE_HOME: Record<UserRole, string> = {
  admin: '/admin/dashboard',
  biomedical: '/dashboard/biomedical',
  nurse: '/dashboard/nurse'
}

export const ROLE_LABELS: Record<UserRole, string> = {
  admin: 'Hospital Administrator',
  biomedical: 'Biomedical Engineer',
  nurse: 'Clinical Staff'
}

export const ROLE_SHORT_LABELS:
Record<UserRole, string> = {
  admin: 'Admin',


  biomedical: 'Biomedical',

  nurse: 'Nurse'
}

export type RoutePermissionRule = {
  prefix: string
  roles: UserRole[]
}



export const ROUTE_PERMISSION_RULES: RoutePermissionRule[] = [

  {
    prefix: '/assets',

    roles: [
      'admin',
      'biomedical',
      'nurse'
    ]
  },

  {
    prefix: '/admin',
    roles: ['admin']
  },

  {
    prefix: '/dashboard/biomedical',
    roles: ['biomedical']
  },

  {
    prefix: '/dashboard/nurse',
    roles: ['nurse']
  }
]

export const isPublicRoute = (
  path: string
) => {
  return PUBLIC_ROUTES.some(
    route => route === path
  )
}

export const getRoleHome = (
  role: UserRole
) => {
  return ROLE_HOME[role]
}

export const getRoleLabel = (
  role: UserRole
) => {
  return ROLE_LABELS[role]
}

export const getShortRoleLabel = (
  role: UserRole
) => {
  return ROLE_SHORT_LABELS[role]
}

export const getAllowedRolesForPath = (
  path: string
): UserRole[] | null => {
  const rule = ROUTE_PERMISSION_RULES.find(
    ({ prefix }) =>
      path === prefix ||
      path.startsWith(`${prefix}/`)
  )

  return rule?.roles ?? null
}

export const canRoleAccessPath = (
  role: UserRole,
  path: string
) => {
  const allowedRoles =
    getAllowedRolesForPath(path)

  return allowedRoles
    ? allowedRoles.includes(role)
    : true
}