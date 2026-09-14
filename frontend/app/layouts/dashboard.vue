<template>

  <div
    class="
      min-h-screen
      bg-background
    "
  >

    <div
      class="
        flex
        min-h-screen
      "
    >

      <!-- Desktop Navigation -->
      <LayoutSidebar />


      <!-- Mobile Navigation -->
      <LayoutMobileMenu />


      <!-- Main Application -->
      <div
        class="
          flex
          min-w-0
          flex-1
          flex-col
        "
      >

        <!-- Navbar -->
        <LayoutNavbar />


        <!-- Page -->
        <main
          class="
            flex-1
            p-4
            sm:p-6
            lg:p-8
          "
        >
          <slot />
        </main>

      </div>

    </div>

  </div>

</template>