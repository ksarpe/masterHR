<template>
  <div class="mx-auto grid grid-cols-2 gap-6">
    <div>
      <video-capture @update:result="handleResultUpdate" />
    </div>
    <div class="flex h-screen">
    <div class="w-full p-12">
      <div class="bg-gray-400 shadow-lg rounded-3xl p-4">
        <!-- miejsce na zdjęcie -->
      </div>
      <div v-if="result" class="mt-4 p-4 bg-gray-400 rounded-lg flex space-x-4 text-gray-700 justify-center">
        <p class="text-lg font-semibold">Znak: Z API</p>
        <p class="text-lg font-semibold">Ręka: Z API</p>
      </div>
    </div>
  </div>  
  </div>
</template>

<script setup>
import { ref } from 'vue';
import VideoCapture from '@/components/VideoCapture.vue'

const result = ref({ label_name: 'none', handedness: 'none' });
const expected = ref({ label_name: 'none', handedness: 'none' });

function handleResultUpdate(newResult) {
  result.value = newResult;
}

</script>