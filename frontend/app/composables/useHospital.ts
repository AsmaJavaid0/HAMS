import type {
  HospitalFormPayload,
  HospitalProfile
} from '~/types/hospital'
import { mockHospitals } from '~/config/data/hospitals'
import { useMockPersistence } from '~/composables/useMockPersistence'


type HospitalOperationResult =
  | {
      ok: true
      hospital: HospitalProfile
    }
  | {
      ok: false
      message: string
    }


export const useHospital = () => {

  /*
  |--------------------------------------------------------------------------
  | SHARED HOSPITAL STATE
  |--------------------------------------------------------------------------
  */

  const hospital = useMockPersistence<HospitalProfile>(
    'assetcare-hospital',
    () => ({ ...mockHospitals[0]! }),
    1
  )


  /*
  |--------------------------------------------------------------------------
  | AUSTRALIAN STATES
  |--------------------------------------------------------------------------
  */

  const australianStates = [
    'NSW',
    'VIC',
    'QLD',
    'WA',
    'SA',
    'TAS',
    'ACT',
    'NT'
  ] as const


  /*
  |--------------------------------------------------------------------------
  | TIMEZONES
  |--------------------------------------------------------------------------
  */

  const australianTimezones = [
    'Australia/Sydney',
    'Australia/Melbourne',
    'Australia/Brisbane',
    'Australia/Perth',
    'Australia/Adelaide',
    'Australia/Hobart',
    'Australia/Darwin'
  ] as const


  /*
  |--------------------------------------------------------------------------
  | UPDATE
  |--------------------------------------------------------------------------
  */

  const updateHospital = (
    payload: HospitalFormPayload
  ): HospitalOperationResult => {

    if (!payload.name.trim()) {
      return {
        ok: false,
        message:
          'Hospital name is required.'
      }
    }


    if (!payload.code.trim()) {
      return {
        ok: false,
        message:
          'Hospital code is required.'
      }
    }


    if (
      !payload.email.trim() ||
      !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
        payload.email.trim()
      )
    ) {
      return {
        ok: false,
        message:
          'Please enter a valid hospital email.'
      }
    }


    if (!payload.address.trim()) {
      return {
        ok: false,
        message:
          'Hospital address is required.'
      }
    }


    if (!payload.suburb.trim()) {
      return {
        ok: false,
        message:
          'Suburb is required.'
      }
    }


    if (
      !australianStates.includes(
        payload.state as typeof australianStates[number]
      )
    ) {
      return {
        ok: false,
        message:
          'Please select a valid Australian state or territory.'
      }
    }


    if (
      !/^\d{4}$/.test(
        payload.postcode.trim()
      )
    ) {
      return {
        ok: false,
        message:
          'Australian postcode must contain 4 digits.'
      }
    }


    hospital.value = {
      ...hospital.value,

      name:
        payload.name.trim(),

      code:
        payload.code
          .trim()
          .toUpperCase(),

      registrationNumber:
        payload.registrationNumber
          .trim(),

      email:
        payload.email
          .trim()
          .toLowerCase(),

      phone:
        payload.phone.trim(),

      address:
        payload.address.trim(),

      suburb:
        payload.suburb.trim(),

      state:
        payload.state,

      postcode:
        payload.postcode.trim(),

      timezone:
        payload.timezone,

      status:
        payload.status
    }


    return {
      ok: true,
      hospital:
        hospital.value
    }
  }


  return {
    hospital,

    australianStates,
    australianTimezones,

    updateHospital
  }
}