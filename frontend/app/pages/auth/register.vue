<script setup lang="ts">
definePageMeta({
  layout: 'auth'
})

// Hospital Information
const hospitalName = ref('')
const registrationNumber = ref('')
const hospitalType = ref('')
const hospitalEmail = ref('')
const hospitalPhone = ref('')
const address = ref('')
const city = ref('')
const country = ref('')

// Administrator Information
const adminName = ref('')
const adminEmail = ref('')
const adminPhone = ref('')
const password = ref('')
const confirmPassword = ref('')
const profilePhoto = ref<File | null>(null)

// UI states
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isLoading = ref(false)
const registerError = ref('')
const successMessage = ref('')

// Validation errors
const hospitalNameError = ref('')
const registrationNumberError = ref('')
const hospitalTypeError = ref('')
const hospitalEmailError = ref('')
const hospitalPhoneError = ref('')
const addressError = ref('')
const cityError = ref('')
const countryError = ref('')

const adminNameError = ref('')
const adminEmailError = ref('')
const adminPhoneError = ref('')
const passwordError = ref('')
const confirmPasswordError = ref('')
const profilePhotoError = ref('')

const validateForm = async () => {
  // Clear previous errors
  hospitalNameError.value = ''
  registrationNumberError.value = ''
  hospitalTypeError.value = ''
  hospitalEmailError.value = ''
  hospitalPhoneError.value = ''
  addressError.value = ''
  cityError.value = ''
  countryError.value = ''

  adminNameError.value = ''
  adminEmailError.value = ''
  adminPhoneError.value = ''
  passwordError.value = ''
  confirmPasswordError.value = ''
  profilePhotoError.value = ''

  registerError.value = ''
  successMessage.value = ''

  let isValid = true

  // -------------------------
  // Hospital validation
  // -------------------------

  if (!hospitalName.value.trim()) {
    hospitalNameError.value = 'Hospital name is required.'
    isValid = false
  }

  if (!registrationNumber.value.trim()) {
    registrationNumberError.value =
      'Hospital registration number is required.'
    isValid = false
  }

  if (!hospitalType.value) {
    hospitalTypeError.value = 'Please select a hospital type.'
    isValid = false
  }

  if (!hospitalEmail.value.trim()) {
    hospitalEmailError.value = 'Hospital email is required.'
    isValid = false
  } else if (
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(hospitalEmail.value)
  ) {
    hospitalEmailError.value =
      'Please enter a valid hospital email address.'
    isValid = false
  }

  if (!hospitalPhone.value.trim()) {
    hospitalPhoneError.value = 'Hospital phone is required.'
    isValid = false
  }

  if (!address.value.trim()) {
    addressError.value = 'Address is required.'
    isValid = false
  }

  if (!city.value.trim()) {
    cityError.value = 'City is required.'
    isValid = false
  }

  if (!country.value.trim()) {
    countryError.value = 'Country is required.'
    isValid = false
  }

  // -------------------------
  // Administrator validation
  // -------------------------

  if (!adminName.value.trim()) {
    adminNameError.value = 'Full name is required.'
    isValid = false
  }

  if (!adminEmail.value.trim()) {
    adminEmailError.value = 'Admin email is required.'
    isValid = false
  } else if (
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(adminEmail.value)
  ) {
    adminEmailError.value =
      'Please enter a valid email address.'
    isValid = false
  }

  // Admin phone is optional
  if (
    adminPhone.value.trim() &&
    !/^[0-9+\-\s()]{7,20}$/.test(adminPhone.value)
  ) {
    adminPhoneError.value =
      'Please enter a valid phone number.'
    isValid = false
  }

  if (!password.value) {
    passwordError.value = 'Password is required.'
    isValid = false
  } else if (password.value.length < 8) {
    passwordError.value =
      'Password must be at least 8 characters.'
    isValid = false
  }

  if (!confirmPassword.value) {
    confirmPasswordError.value =
      'Please confirm your password.'
    isValid = false
  } else if (password.value !== confirmPassword.value) {
    confirmPasswordError.value =
      'Passwords do not match.'
    isValid = false
  }

  if (!isValid) {
    return
  }

  // ---------------------------------------
  // API will be connected here later
  // ---------------------------------------

  isLoading.value = true

  try {
    /*
      IMPORTANT:
      Do not add dummy/mock registration data here.

      Later this form will send the following data
      to the backend registration endpoint:

      POST /api/auth/register-hospital

      Hospital:
      - hospitalName
      - registrationNumber
      - hospitalType
      - hospitalEmail
      - hospitalPhone
      - address
      - city
      - country

      Administrator:
      - adminName
      - adminEmail
      - adminPhone
      - password
      - profilePhoto
    */

    await new Promise(resolve => setTimeout(resolve, 500))

    registerError.value =
      'Registration service is not connected yet. Please try again when the API is available.'
  } catch (error) {
    console.error('Registration error:', error)

    registerError.value =
      'Unable to create your account. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleProfilePhoto = (
  event: Event
) => {
  profilePhotoError.value = ''

  const target = event.target as HTMLInputElement

  if (!target.files || target.files.length === 0) {
    profilePhoto.value = null
    return
  }

  const file = target.files[0]

  if (!file) {
    profilePhoto.value = null
    return
  }

  // Optional field — only basic frontend validation
  if (!file.type.startsWith('image/')) {
    profilePhotoError.value =
      'Please select a valid image file.'
    profilePhoto.value = null
    return
  }

  profilePhoto.value = file
}

const handleGoogleSignup = () => {
  registerError.value =
    'Google registration will be connected when OAuth is configured.'
}
</script>

<template>
  <div
    class="min-h-screen bg-background px-4 py-8 sm:px-6 lg:py-12"
  >
    <div class="mx-auto w-full max-w-3xl">

      <!-- Logo + Heading -->
      <div class="mb-8 text-center">
        <img
          src="/logo/asset%20care%20logo.png"
          alt="AssetCare logo"
          class="mx-auto h-16 w-16 object-contain"
        />

        <h1
          class="mt-4 text-2xl font-bold text-text-primary sm:text-3xl"
        >
          Create an Account
        </h1>

        <p
          class="mt-2 text-sm text-text-secondary"
        >
          Register your hospital and create the first administrator account
        </p>
      </div>

      <!-- Registration Card -->
      <div
        class="rounded-2xl bg-white p-6 shadow-sm sm:p-8 lg:p-10"
      >

        <form
          class="space-y-8"
          @submit.prevent="validateForm"
        >

          <!-- ========================= -->
          <!-- Hospital Information -->
          <!-- ========================= -->

          <section>
            <div class="mb-5">
              <h2
                class="text-lg font-semibold text-text-primary"
              >
                Hospital Information
              </h2>

              <p
                class="mt-1 text-sm text-text-secondary"
              >
                Enter your hospital's official information.
              </p>
            </div>

            <div
              class="grid grid-cols-1 gap-5 sm:grid-cols-2"
            >

              <!-- Hospital Name -->
              <div class="sm:col-span-2">
                <label
                  for="hospitalName"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Hospital Name
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="hospitalName"
                  v-model="hospitalName"
                  type="text"
                  autocomplete="organization"
                  placeholder="Enter hospital name"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="hospitalNameError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ hospitalNameError }}
                </p>
              </div>

              <!-- Registration Number -->
              <div>
                <label
                  for="registrationNumber"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Hospital Registration Number
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="registrationNumber"
                  v-model="registrationNumber"
                  type="text"
                  placeholder="Enter registration number"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="registrationNumberError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ registrationNumberError }}
                </p>
              </div>

              <!-- Hospital Type -->
              <div>
                <label
                  for="hospitalType"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Hospital Type
                  <span class="text-red-500">*</span>
                </label>

                <select
                  id="hospitalType"
                  v-model="hospitalType"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition focus:border-primary focus:ring-2 focus:ring-primary/10"
                >
                  <option value="" disabled>
                    Select hospital type
                  </option>

                  <option value="public">
                    Public Hospital
                  </option>

                  <option value="private">
                    Private Hospital
                  </option>

                  <option value="teaching">
                    Teaching Hospital
                  </option>

                  <option value="specialized">
                    Specialized Hospital
                  </option>

                  <option value="other">
                    Other
                  </option>
                </select>

                <p
                  v-if="hospitalTypeError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ hospitalTypeError }}
                </p>
              </div>

              <!-- Hospital Email -->
              <div>
                <label
                  for="hospitalEmail"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Hospital Email
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="hospitalEmail"
                  v-model="hospitalEmail"
                  type="email"
                  autocomplete="email"
                  placeholder="Enter hospital email"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="hospitalEmailError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ hospitalEmailError }}
                </p>
              </div>

              <!-- Hospital Phone -->
              <div>
                <label
                  for="hospitalPhone"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Hospital Phone
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="hospitalPhone"
                  v-model="hospitalPhone"
                  type="tel"
                  autocomplete="tel"
                  placeholder="Enter hospital phone"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="hospitalPhoneError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ hospitalPhoneError }}
                </p>
              </div>

              <!-- Address -->
              <div class="sm:col-span-2">
                <label
                  for="address"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Address
                  <span class="text-red-500">*</span>
                </label>

                <textarea
                  id="address"
                  v-model="address"
                  rows="3"
                  placeholder="Enter hospital address"
                  class="w-full resize-none rounded-lg border border-gray-300 bg-white px-4 py-3 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="addressError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ addressError }}
                </p>
              </div>

              <!-- City -->
              <div>
                <label
                  for="city"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  City
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="city"
                  v-model="city"
                  type="text"
                  autocomplete="address-level2"
                  placeholder="Enter city"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="cityError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ cityError }}
                </p>
              </div>

              <!-- Country -->
              <div>
                <label
                  for="country"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Country
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="country"
                  v-model="country"
                  type="text"
                  autocomplete="country-name"
                  placeholder="Enter country"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="countryError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ countryError }}
                </p>
              </div>

            </div>
          </section>

          <!-- Divider -->
          <div class="h-px bg-gray-200"></div>

          <!-- ========================= -->
          <!-- Administrator Information -->
          <!-- ========================= -->

          <section>
            <div class="mb-5">
              <h2
                class="text-lg font-semibold text-text-primary"
              >
                Administrator Information
              </h2>

              <p
                class="mt-1 text-sm text-text-secondary"
              >
                Create the account for the first hospital administrator.
              </p>
            </div>

            <div
              class="grid grid-cols-1 gap-5 sm:grid-cols-2"
            >

              <!-- Admin Name -->
              <div class="sm:col-span-2">
                <label
                  for="adminName"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Admin Full Name
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="adminName"
                  v-model="adminName"
                  type="text"
                  autocomplete="name"
                  placeholder="Enter administrator full name"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="adminNameError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ adminNameError }}
                </p>
              </div>

              <!-- Admin Email -->
              <div>
                <label
                  for="adminEmail"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Admin Email
                  <span class="text-red-500">*</span>
                </label>

                <input
                  id="adminEmail"
                  v-model="adminEmail"
                  type="email"
                  autocomplete="email"
                  placeholder="Enter admin email"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="adminEmailError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ adminEmailError }}
                </p>
              </div>

              <!-- Admin Phone -->
              <div>
                <label
                  for="adminPhone"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Admin Phone
                  <span class="text-gray-400">
                    (Optional)
                  </span>
                </label>

                <input
                  id="adminPhone"
                  v-model="adminPhone"
                  type="tel"
                  autocomplete="tel"
                  placeholder="Enter admin phone"
                  class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                />

                <p
                  v-if="adminPhoneError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ adminPhoneError }}
                </p>
              </div>

              <!-- Password -->
              <div>
                <label
                  for="password"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Password
                  <span class="text-red-500">*</span>
                </label>

                <div class="relative">
                  <input
                    id="password"
                    v-model="password"
                    :type="
                      showPassword
                        ? 'text'
                        : 'password'
                    "
                    autocomplete="new-password"
                    placeholder="Enter your password"
                    class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 pr-16 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                  />

                  <button
                    type="button"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500 hover:text-primary"
                    @click="
                      showPassword =
                        !showPassword
                    "
                  >
                    {{
                      showPassword
                        ? 'Hide'
                        : 'Show'
                    }}
                  </button>
                </div>

                <p
                  v-if="passwordError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ passwordError }}
                </p>
              </div>

              <!-- Confirm Password -->
              <div>
                <label
                  for="confirmPassword"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Confirm Password
                  <span class="text-red-500">*</span>
                </label>

                <div class="relative">
                  <input
                    id="confirmPassword"
                    v-model="confirmPassword"
                    :type="
                      showConfirmPassword
                        ? 'text'
                        : 'password'
                    "
                    autocomplete="new-password"
                    placeholder="Re-enter your password"
                    class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 pr-16 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
                  />

                  <button
                    type="button"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500 hover:text-primary"
                    @click="
                      showConfirmPassword =
                        !showConfirmPassword
                    "
                  >
                    {{
                      showConfirmPassword
                        ? 'Hide'
                        : 'Show'
                    }}
                  </button>
                </div>

                <p
                  v-if="confirmPasswordError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ confirmPasswordError }}
                </p>
              </div>

              <!-- Profile Photo -->
              <div class="sm:col-span-2">
                <label
                  for="profilePhoto"
                  class="mb-2 block text-sm font-medium text-text-primary"
                >
                  Profile Photo
                  <span class="text-gray-400">
                    (Optional)
                  </span>
                </label>

                <input
                  id="profilePhoto"
                  type="file"
                  accept="image/*"
                  class="block w-full rounded-lg border border-gray-300 bg-white text-sm text-gray-600 file:mr-4 file:border-0 file:bg-gray-100 file:px-4 file:py-3 file:text-sm file:font-medium hover:file:bg-gray-200"
                  @change="handleProfilePhoto"
                />

                <p
                  v-if="profilePhotoError"
                  class="mt-1.5 text-xs text-red-500"
                >
                  {{ profilePhotoError }}
                </p>
              </div>

            </div>
          </section>

          <!-- Server Error -->
          <div
            v-if="registerError"
            class="rounded-lg bg-red-50 px-4 py-3 text-center text-sm text-red-600"
          >
            {{ registerError }}
          </div>

          <!-- Success -->
          <div
            v-if="successMessage"
            class="rounded-lg bg-green-50 px-4 py-3 text-center text-sm text-green-600"
          >
            {{ successMessage }}
          </div>

          <!-- Create Account -->
          <button
            type="submit"
            :disabled="isLoading"
            class="h-12 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <span v-if="isLoading">
              Creating account...
            </span>

            <span v-else>
              Create Account
            </span>
          </button>

        </form>

        <!-- Divider -->
        <div class="my-6 flex items-center gap-4">
          <div class="h-px flex-1 bg-gray-200"></div>

          <span class="text-xs text-gray-400">
            OR
          </span>

          <div class="h-px flex-1 bg-gray-200"></div>
        </div>

        <!-- Google -->
        <button
          type="button"
          class="flex h-12 w-full items-center justify-center gap-3 rounded-lg border border-gray-300 bg-white text-sm font-medium text-gray-700 transition hover:bg-gray-50"
          @click="handleGoogleSignup"
        >
          <span class="font-bold text-base">
            G
          </span>

          Continue with Google
        </button>

        <!-- Sign In -->
        <p
          class="mt-6 text-center text-sm text-text-secondary"
        >
          Already have an account?

          <NuxtLink
            to="/auth/login"
            class="font-semibold text-primary hover:underline"
          >
            Sign In
          </NuxtLink>
        </p>

      </div>
    </div>
  </div>
</template>