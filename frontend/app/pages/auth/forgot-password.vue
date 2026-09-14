<script setup lang="ts">

definePageMeta({
  layout: 'auth'
})

const email = ref('')

const emailError = ref('')
const isLoading = ref(false)
const successMessage = ref('')

const handleSubmit = async () => {
  emailError.value = ''
  successMessage.value = ''

  if (!email.value.trim()) {
    emailError.value = 'Email is required.'
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Please enter a valid email address.'
    return
  }

  isLoading.value = true

  // Password reset API will be connected here later
  await new Promise(resolve => setTimeout(resolve, 1000))

  isLoading.value = false

  successMessage.value =
    'If an account exists with this email, you will receive a password reset link.'
}

</script>

<template>
  <div
    class="relative flex min-h-screen w-full items-center justify-center overflow-hidden bg-background px-4 py-8"
  >

    <!-- Background Decoration -->
    <div
      class="pointer-events-none absolute -left-32 -top-32 h-80 w-80 rounded-full bg-primary/10 blur-3xl"
    ></div>

    <div
      class="pointer-events-none absolute -bottom-40 -right-32 h-96 w-96 rounded-full bg-blue-200/30 blur-3xl"
    ></div>


    <!-- Content -->
    <div class="relative z-10 w-full max-w-md">

      <!-- Logo -->
      <div class="mb-8 text-center">

        <div
          class="mx-auto flex h-20 w-20 items-center justify-center rounded-2xl bg-white shadow-md"
        >
          <img
            src="/logo/asset%20care%20logo.png"
            alt="AssetCare Logo"
            class="h-16 w-16 object-contain"
          />
        </div>

        <h1 class="mt-5 text-3xl font-bold text-text-primary">
          Forgot Password?
        </h1>

        <p class="mt-2 text-sm leading-6 text-text-secondary">
          Enter your email address and we'll send you a link
          to reset your password.
        </p>

      </div>


      <!-- Card -->
      <div
        class="rounded-2xl border border-gray-200 bg-white/95 p-6 shadow-xl backdrop-blur-sm sm:p-8"
      >

        <form
          class="space-y-5"
          @submit.prevent="handleSubmit"
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

            <p
              v-if="emailError"
              class="mt-1.5 text-xs text-red-500"
            >
              {{ emailError }}
            </p>

          </div>


          <!-- Submit -->
          <button
            type="submit"
            :disabled="isLoading"
            class="h-12 w-full rounded-lg bg-primary px-4 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <span v-if="isLoading">
              Sending...
            </span>

            <span v-else>
              Send Reset Link
            </span>
          </button>


          <!-- Success -->
          <p
            v-if="successMessage"
            class="rounded-lg bg-green-50 px-4 py-3 text-center text-sm text-green-600"
          >
            {{ successMessage }}
          </p>

        </form>


        <!-- Back to Login -->
        <div class="mt-7 text-center">

          <NuxtLink
            to="/auth/login"
            class="text-sm font-semibold text-primary hover:underline"
          >
            ← Back to Sign In
          </NuxtLink>

        </div>

      </div>

    </div>

  </div>
</template>