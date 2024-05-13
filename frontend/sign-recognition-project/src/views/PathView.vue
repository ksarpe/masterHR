<template>
  <div class="p-8 bg-gray-700 min-h-screen">
    <div class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Iterating through each learning path item -->
      <router-link v-for="node in learningPath" :key="node.id" :to="node.link"
         class="block border-2 text-white border-gray-300 rounded-lg shadow-lg p-24 text-center transition-colors hover:cursor-pointer hover:bg-gray-800 hover:text-white hover:border-white">
        <h2 class="text-3xl font-bold">{{ node.title }}</h2>
      </router-link>
    </div>
  </div>
</template>

<script setup>
const learningPath = [
  { id: 1, title: "PODSTAWY I", link: "/learn/introduction" },
  { id: 2, title: "PODSTAWY II", link: "/learn/basics" },
  { id: 3, title: "DOM", link: "/learn/intermediate" },
  { id: 4, title: "WKRÓTCE...", link: "/learn" },
  { id: 5, title: "WKRÓTCE...", link: "/learn" },
  { id: 6, title: "WKRÓTCE...", link: "/learn" }
];
</script>
