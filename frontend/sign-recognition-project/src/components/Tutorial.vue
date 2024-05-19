<template>
  <div class="fixed inset-0 bg-black bg-opacity-85 flex justify-center items-center text-gray-800">
    <div class="bg-white p-5 rounded-lg text-center border-blue-500 border-4">
      <h2 class="text-3xl font-bold mb-4">Witaj w samouczku!</h2>
      <div class="text-2xl font-medium">
        <p>Po lewej stronie znajduje się podgląd Twojej kamery.</p>
        <p>Po prawej stronie możesz zobaczyć znak, którego obecnie się uczysz.</p>
        <br />
        <p class="font-semibold">
          <span class="text-red-400 font-semibold">Kliknij myszką na przycisk pod Twoją kamerą</span
          >, a za dwie sekundy zostanie zrobione zdjęcie.
        </p>
        <p class="font-semibold">
          bądź po prostu <span class="text-red-400 font-semibold">naciśnij enter</span>, a również
          za dwie sekundy zostanie zrobione zdjęcie.
        </p>
        <p class="text-xl">
          (w lewym dolnym rogu znajduje się również podpowiedź ostatnio wykrytego znaku)
        </p>
        <br>
        <p class="text-2xl">
          U góry znajdziesz również <span class="text-blue-400 font-semibold">modyfikatory</span>, które pozwolą Ci dostosować sposób nauki do swoich oczekiwań.
        </p>
      </div>
      <button
        @click="closeTutorial"
        class="mt-8 bg-blue-500 text-white rounded px-4 py-2 font-semibold text-xl hover:bg-green-600"
      >
        Przejdź do nauki!
      </button>
    </div>
  </div>
</template>

<script setup>
const emit = defineEmits(['close'])

function closeTutorial() {
  emit('close')
}
</script>
