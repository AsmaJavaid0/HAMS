<!-- <script setup lang="ts">
const { login, errorMessage } = useAuth()
// definePageMeta({
//   layout: 'auth'
// })

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)

const emailError = ref('')
const passwordError = ref('')

const isLoading = ref(false)
const loginError = ref('')

// const validateForm = async () => {
//   emailError.value = ''
//   passwordError.value = ''
//   loginError.value = ''

//   let isValid = true

//   if (!email.value.trim()) {
//     emailError.value = 'Email is required.'
//     isValid = false
//   } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
//     emailError.value = 'Please enter a valid email address.'
//     isValid = false
//   }

//   if (!password.value) {
//     passwordError.value = 'Password is required.'
//     isValid = false
//   }

//   if (!isValid) {
//     return
//   }

//   isLoading.value = true

//   // API will be connected here later
//   await new Promise(resolve => setTimeout(resolve, 1000))

//   isLoading.value = false

//   loginError.value = 'Unable to sign in. Please try again.'
// }
const validateForm = async () => {
  emailError.value = ''
  passwordError.value = ''
  loginError.value = ''

  let isValid = true

  if (!email.value.trim()) {
    emailError.value = 'Email is required.'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Please enter a valid email address.'
    isValid = false
  }

  if (!password.value) {
    passwordError.value = 'Password is required.'
    isValid = false
  }

  if (!isValid) {
    return
  }

  isLoading.value = true

  const success = await login(email.value, password.value)

  isLoading.value = false

  if (!success) {
    loginError.value = errorMessage.value
  }
}
</script> -->
<script setup lang="ts">
import { ref } from 'vue'

import { useAuth } from '~/composables/useAuth'

definePageMeta({
  layout: 'auth'
})

const { login } = useAuth()

const email = ref('')
const password = ref('')
const showPassword = ref(false)
const rememberMe = ref(false)

const emailError = ref('')
const passwordError = ref('')
const isLoading = ref(false)
const loginError = ref('')

const validateForm = async () => {
  emailError.value = ''
  passwordError.value = ''
  loginError.value = ''

  let isValid = true

  if (!email.value.trim()) {
    emailError.value = 'Email is required.'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Please enter a valid email address.'
    isValid = false
  }

  if (!password.value) {
    passwordError.value = 'Password is required.'
    isValid = false
  }

  if (!isValid) {
    return
  }

  isLoading.value = true

  const success = await login(email.value, password.value)

  isLoading.value = false

  if (!success) {
    loginError.value = 'Unable to sign in. Please try again.'
  }
}

</script>
<template>
  <div class="flex min-h-screen items-center justify-center bg-background px-4 py-8">

    <div class="w-full max-w-md">

      <!-- Logo -->
      <div class="mb-8 text-center">
        <img
          src="/logo/asset%20care%20logo.png"
          alt="AssetCare logo"
          class="mx-auto h-16 w-16 object-contain"
        />

        <h1 class="mt-4 text-2xl font-bold text-text-primary">
          Welcome Back!
        </h1>

        <p class="mt-2 text-sm text-text-secondary">
          Sign in to your AssetCare account
        </p>
      </div>


      <!-- Login Card -->
      <div class="rounded-2xl bg-white p-6 shadow-sm sm:p-8">

     <form
  class="space-y-5"
  @submit.prevent="validateForm"
>

          <!-- Email -->
          <div>
            <label
              for="email"
              class="mb-2 block text-sm font-medium text-text-primary"
            >
              Email
            </label>

            <input
              id="email"
              v-model="email"
              type="email"
              autocomplete="email"
              placeholder="Enter your email"
              class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
            />
          </div>


          <!-- Password -->
          <div>
            <label
              for="password"
              class="mb-2 block text-sm font-medium text-text-primary"
            >
              Password
            </label>

            <div class="relative">

              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                placeholder="Enter your password"
                class="h-12 w-full rounded-lg border border-gray-300 bg-white px-4 pr-12 text-sm text-gray-900 outline-none transition placeholder:text-gray-400 focus:border-primary focus:ring-2 focus:ring-primary/10"
              />
<p
  v-if="emailError"
  class="mt-1.5 text-xs text-red-500"
>
  {{ emailError }}
</p>
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-500 hover:text-primary"
                @click="showPassword = !showPassword"
              >
                {{ showPassword ? 'Hide' : 'Show' }}
              </button>
<p
  v-if="passwordError"
  class="mt-1.5 text-xs text-red-500"
>
  {{ passwordError }}
</p>
            </div>
          </div>


          <!-- Remember + Forgot -->
          <div class="flex items-center justify-between gap-4">

            <label class="flex cursor-pointer items-center gap-2">
              <input
                v-model="rememberMe"
                type="checkbox"
                class="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary"
              />

              <span class="text-sm text-text-secondary">
                Remember me
              </span>
            </label>

            <NuxtLink
              to="/auth/forgot-password"
              class="text-sm font-medium text-primary hover:underline"
            >
              Forgot password?
            </NuxtLink>

          </div>


          <!-- Sign In -->
        <button
  type="submit"
  :disabled="isLoading"
  class="h-12 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
>
  <span v-if="isLoading">
    Signing in...
  </span>

  <span v-else>
    Sign In
  </span>
</button>
<p
  v-if="loginError"
  class="rounded-lg bg-red-50 px-4 py-3 text-center text-sm text-red-600"
>
  {{ loginError }}
</p>

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
        >
          <span class="font-bold">
            G
          </span>

          Continue with Google
        </button>


        <!-- Register -->
        <p class="mt-6 text-center text-sm text-text-secondary">

          Don't have an account?

          <NuxtLink
            to="/auth/register"
            class="font-semibold text-primary hover:underline"
          >
            Get Started
          </NuxtLink>

        </p>

      </div>

    </div>

  </div>
</template>
