import type { UserRole } from '~/types/auth'

export const PUBLIC_ROUTES = [
  '/auth/login',
  '/auth/register',
  '/auth/forgot-password'
] as const

export const ROLE_HOME: Record<UserRole, string> = {
  admin: '/admin/dashboard',
  manager: '/dashboard/manager',
  biomedical: '/dashboard/biomedical',
  nurse: '/dashboard/nurse'
}

export const ROLE_LABELS: Record<UserRole, string> = {
  admin: 'Hospital Administrator',
  manager: 'Department Manager',
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
      label: 'Departments',
      icon: '▤',
      to: '/admin/departments'
    },
    {
      label: 'Hospital',
      icon: '▥',
      to: '/admin/hospital'
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
      label: 'Reports',
      icon: '▤',
      to: '/admin/reports'
    }
  ],
  manager: [
    {
      label: 'Dashboard',
      icon: '▦',
      to: '/dashboard/manager'
    },
    {
      label: 'Assets',
      icon: '▣',
      to: '/assets'
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
    }
  ],
  nurse: [
    {
      label: 'Dashboard',
      icon: '▦',
      to: '/dashboard/nurse'
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
    prefix: '/dashboard/manager',
    roles: ['manager']
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
