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

export type NavigationItem = {
  label: string
  icon: string
  to: string
}

export const NAVIGATION_BY_ROLE: Record<
  UserRole,
  NavigationItem[]
> = {
  admin: [
    {
      label: 'Dashboard',
      icon: '▦',
      to: '/admin/dashboard'
    },
    {
      label: 'Assets',
      icon: '▣',
      to: '/admin/assets'
    },
    {
      label: 'Maintenance',
      icon: '⚙',
      to: '/admin/maintenance'
    },
    {
      label: 'Staff',
      icon: '♙',
      to: '/admin/staff'
    },
    {
      label: 'Audit Log',
      icon: '≡',
      to: '/admin/audit'
    },
    {
      label: 'Logout',
      icon: '⏏',
      to: '/auth/logout'
    }
  ],
  biomedical: [
    {
      label: 'Dashboard',
      icon: '▦',
      to: '/dashboard/biomedical'
    },
    {
      label: 'Assets',
      icon: '▣',
      to: '/assets'
    },
    {
      label: 'Maintenance',
      icon: '⚙',
      to: '/maintenance'
    },
    {
      label: 'Logout',
      icon: '⏏',
      to: '/auth/logout'
    }
  ],
  nurse: [
    {
      label: 'Dashboard',
      icon: '▦',
      to: '/dashboard/nurse'
    },
    {
      label: 'My Assets',
      icon: '▣',
      to: '/assets/my'
    },
    {
      label: 'Report Fault',
      icon: '⚠',
      to: '/fault-report'
    },
    {
      label: 'Logout',
      icon: '⏏',
      to: '/auth/logout'
    }
  ]
}

type RoutePermissionRule = {
  prefix: string
  roles: UserRole[]
}

const ROUTE_PERMISSION_RULES: RoutePermissionRule[] = [
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
  },
  {
    prefix: '/assets',
    roles: ['admin', 'biomedical', 'nurse']
  },
  {
    prefix: '/maintenance',
    roles: ['admin', 'biomedical']
  },
  {
    prefix: '/fault-report',
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
