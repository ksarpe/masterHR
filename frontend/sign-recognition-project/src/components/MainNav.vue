<template>
  <nav class="bg-gray-800 text-white w-full">
    <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Navigation Links -->
        <div class="flex-1 flex items-center justify-center">
          <div class="flex space-x-4">
            <router-link to="/" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500" aria-current="page">Strona główna </router-link>
            <router-link to="/learn" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Nauka</router-link>
            <router-link to="/tests" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Testy</router-link>
            <router-link to="/games" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Gra z czasem</router-link>
            <router-link to="/community" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Społeczność</router-link>
            <router-link to="/help" class="px-5 py-2 rounded-md text-md font-medium hover:text-blue-500">Pomoc</router-link>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>