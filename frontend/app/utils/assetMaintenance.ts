import type {
  MaintenancePriority
} from '~/types/asset'


const parseDateOnly = (
  value: string
) => {

  const [
    year,
    month,
    day
  ] = value
    .split('-')
    .map(Number)


  if (
    !year ||
    !month ||
    !day
  ) {

    return null
  }


  return new Date(
    year,
    month - 1,
    day
  )
}


const startOfToday = (
  now = new Date()
) => {

  return new Date(
    now.getFullYear(),
    now.getMonth(),
    now.getDate()
  )
}


export const getDaysUntilMaintenance = (
  nextMaintenanceDate: string,
  now = new Date()
): number | null => {

  if (!nextMaintenanceDate) {
    return null
  }


  const maintenanceDate =
    parseDateOnly(
      nextMaintenanceDate
    )


  if (!maintenanceDate) {
    return null
  }


  const today =
    startOfToday(now)


  const difference =
    maintenanceDate.getTime() -
    today.getTime()


  return Math.ceil(
    difference /
    (1000 * 60 * 60 * 24)
  )
}


export const getMaintenancePriority = (
  nextMaintenanceDate: string,
  now = new Date()
): MaintenancePriority => {

  const days =
    getDaysUntilMaintenance(
      nextMaintenanceDate,
      now
    )


  if (days === null) {
    return 'Not Scheduled'
  }


  if (days < 0) {
    return 'Overdue'
  }


  if (days <= 14) {
    return 'High'
  }


  if (days <= 30) {
    return 'Medium'
  }


  return 'Low'
}


export const getMaintenancePriorityClass = (
  priority: MaintenancePriority
) => {

  switch (priority) {

    case 'Overdue':
      return 'bg-red-100 text-red-700'

    case 'High':
      return 'bg-orange-100 text-orange-700'

    case 'Medium':
      return 'bg-yellow-100 text-yellow-700'

    case 'Low':
      return 'bg-green-100 text-green-700'

    case 'Not Scheduled':
      return 'bg-gray-100 text-gray-600'
  }
}