<template>
  <div v-if="showTutorial" class="fixed inset-0 bg-black bg-opacity-85 flex justify-center items-center text-gray-800 p-4 overflow-auto">
    <div class="bg-white p-5 rounded-lg text-center border-blue-500 border-4 max-w-full md:max-w-2xl overflow-auto">
      <h2 class="text-2xl md:text-3xl font-bold mb-4">Witaj w samouczku!</h2>
      <div class="text-lg md:text-2xl font-medium">
        <p>Po <strong>lewej stronie (lub u góry na urządzeniu mobilnym)</strong> znajduje się podgląd Twojej kamery.</p>
        <p>Po <strong>prawej stronie (lub na dole na urządzeniu mobilnym)</strong> widzisz gest, którego obecnie się uczysz.</p>
        <p>Znak zostanie zweryfikowany po wykonaniu poniższych czynności.</p>
        <p class="font-semibold">
          <span class="text-red-400 font-semibold">Kliknij myszką (bądź palcem) na przycisk pod Twoją kamerą</span>, a po dwóch sekundach zostanie zrobione zdjęcie.
        </p>
        <p class="font-semibold">
          bądź po prostu <span class="text-red-400 font-semibold">naciśnij enter (tylko na PC)</span>, a również po dwóch sekundach zostanie zrobione zdjęcie.
        </p>
        <p class="text-base md:text-xl">
          (w lewym dolnym rogu znajduje się również podpowiedź ostatnio wykrytego znaku)
        </p>
        <br>
        <p class="text-lg md:text-2xl text-red-500 font-bold p-1">
          Staraj się być w odległości maksymalnie 1 metra od kamery! <br>
          Siedź w dobrze oświetlonym otoczeniu.<br>
          Pokazuj znaki tak jakbyś faktycznie rozmawiał z drugą osobą.
        </p>
      </div>
      <button
        @click="closeTutorial"
        class="mt-8 bg-blue-500 text-white rounded px-4 py-2 font-semibold text-xl hover:bg-green-600"
      >
        Rozpocznij naukę!
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'

const emit = defineEmits(['close'])
const showTutorial = ref(true)

function closeTutorial() {
  emit('close')
  showTutorial.value = false
}

// Watch for changes in showTutorial to add/remove parent class
watch(showTutorial, (newVal) => {
  const appElement = document.getElementById('app')
  if (newVal) {
    appElement.classList.add('lock-scroll')
  } else {
    appElement.classList.remove('lock-scroll')
  }
})

// Ensure the parent class is added when the component is mounted
onMounted(() => {
  const appElement = document.getElementById('app')
  if (showTutorial.value) {
    appElement.classList.add('lock-scroll')
  }
})

// Ensure the parent class is removed when the component is unmounted
onUnmounted(() => {
  const appElement = document.getElementById('app')
  appElement.classList.remove('lock-scroll')
})
</script>

<style scoped>
@media (max-width: 768px) {
  .text-lg {
    font-size: 1rem;
  }
  .text-xl {
    font-size: 1.25rem;
  }
  .text-2xl {
    font-size: 1.5rem;
  }
  .p-5 {
    padding: 1.25rem;
  }
  .p-4 {
    padding: 1rem;
  }
  .mt-8 {
    margin-top: 2rem;
  }
}

#app.lock-scroll {
  overflow: hidden;
}
</style>
