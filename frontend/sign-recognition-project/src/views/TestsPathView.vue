<template>
  <div class="p-8 bg-gray-700 min-h-screen">
    <div class="max-w-7xl mx-auto grid grid-cols-1 gap-6">
      <!-- Iterating through each learning path item -->
      <router-link
        v-for="node in learningPath"
        :key="node.id"
        :to="node.link"
        class="block border-2 text-white border-gray-300 rounded-lg shadow-lg p-16 text-center transition-colors hover:cursor-pointer hover:bg-gray-800 hover:text-white hover:border-white"
      >
        <h2 class="text-3xl font-bold">{{ node.title }}</h2>
        <h3 class="text-3xl font-bold">{{ node.description }}</h3>
      </router-link>
    </div>
  </div>
</template>

<script setup>
const learningPath = [
  { id: 1, title: 'TEST I (PODSTAWY I)', link: '/tests/test-introduction', description: 'Test zawierający pytania z zakresu podstaw I'},
  { id: 2, title: 'TEST II (ALFABET)', link: '/tests/alphabet', description: 'Test zawierający pytania z zakresu alfabetu migowego.'},
  { id: 3, title: 'TEST III (WKRÓTCE)', link: '/tests', description: '...'},
  { id: 4, title: 'TEST IV (WKRÓTCE...)', link: '/tests', description: '...'},
  { id: 5, title: 'TEST V (WKRÓTCE...)', link: '/tests', description: '...'},
  { id: 6, title: 'TEST VI (WKRÓTCE...)', link: '/tests', description: '...'}
]
</script>
