<template>
  <nav class="bg-gray-800 text-white w-full">
    <div class="max-w-full mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Navigation Links -->
        <div class="flex-1 flex items-center justify-center">
          <div class="flex space-x-4">
            <router-link to="/" class="px-5 py-2 rounded-md text-md font-medium" aria-current="page">Strona główna </router-link>
            <router-link to="/learn" class="px-5 py-2 rounded-md text-md font-medium">Nauka</router-link>
            <a href="#" class="px-5 py-2 rounded-md text-md font-medium">Sprawdź się!</a>
            <a href="#" class="px-5 py-2 rounded-md text-md font-medium text-red-200">Gra z czasem</a>
            <a href="#" class="px-5 py-2 rounded-md text-md font-medium">Społeczność</a>
            <a href="#" class="px-5 py-2 rounded-md text-md font-medium">O projekcie</a>
            <a href="#" class="px-5 py-2 rounded-md text-md font-medium">Pomoc</a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>