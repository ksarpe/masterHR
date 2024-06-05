<template>
  <nav class="bg-gray-800 text-white w-full">
    <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo and Menu Button for Mobile -->
        <div class="flex items-center">
          <button class="lg:hidden mr-4 z-50" @click="toggleMenu">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16m-7 6h7"
              />
            </svg>
          </button>
        </div>

        <!-- Navigation Links for Large Screens -->
        <div class="lg:flex flex-1 items-center justify-center links">
          <div class="flex space-x-4">
            <router-link to="/" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500" aria-current="page">Strona główna</router-link>
            <router-link to="/learn" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Nauka</router-link>
            <router-link to="/tests" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Testy</router-link>
            <router-link to="/games" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Gra z czasem</router-link>
            <router-link to="/community" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Społeczność</router-link>
            <router-link to="/help" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Pomoc</router-link>
          </div>
        </div>
      </div>

      <!-- Mobile menu, show/hide based on menu state. -->
      <div v-show="menuOpen" class="lg:hidden">
        <div class="px-2 pt-2 pb-3 space-y-1 sm:px-3">
          <router-link to="/" @click="menuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium hover:text-blue-500">Strona główna</router-link>
          <router-link to="/learn" @click="menuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium hover:text-blue-500">Nauka</router-link>
          <router-link to="/tests" @click="menuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium hover:text-blue-500">Testy</router-link>
          <router-link to="/games" @click="menuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium hover:text-blue-500">Gra z czasem</router-link>
          <router-link to="/community" @click="menuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium hover:text-blue-500">Społeczność</router-link>
          <router-link to="/help" @click="menuOpen = false" class="block px-3 py-2 rounded-md text-base font-medium hover:text-blue-500">Pomoc</router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

// State to manage menu open/close
const menuOpen = ref(false);

const toggleMenu = () => {
  menuOpen.value = !menuOpen.value;
};
</script>

<style scoped>
/* Add styles to ensure the mobile menu appears correctly */
.hidden {
  display: none;
}

@media (max-width: 1024px) {
  .links {
    display: none;
  }
}
</style>
