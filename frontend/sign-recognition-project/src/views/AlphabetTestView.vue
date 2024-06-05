<template>
  <div class="flex w-full h-screen justify-center items-center">
    <tutorial-test v-if="showTutorial" @close="showTutorial = false" />
    <div v-if="showSuccess" class="absolute inset-0 flex justify-center items-center">
      <div class="animate-bounce bg-green-500 text-white font-bold p-10 rounded-2xl text-xl">
        DOBRZE!
      </div>
    </div>
    <div v-if="showBad" class="absolute inset-0 flex justify-center items-center">
      <div class="animate-bounce bg-red-500 text-white font-bold p-10 rounded-2xl text-xl">
        ŹLE :(
      </div>
    </div>
    <div v-if="showUnknown" class="absolute inset-0 flex justify-center items-center">
      <div class="animate-bounce bg-yellow-500 text-white font-bold p-10 rounded-2xl text-xl">
        Nie wykryto! <br />
        Spróbuj jeszcze raz.
      </div>
    </div>
    <div class="mx-auto flex w-full">
      <div class="flex-1">
        <video-capture :chapter-number="chapter" @update:result="handleResultUpdate" />
      </div>
      <div class="flex-1 flex flex-col items-center justify-center pr-12">
        <div
          v-if="result"
          class="p-7 bg-gray-400 rounded-lg flex flex-col items-center justify-center w-full text-center"
        >
        <div v-if="questionsAnswered != totalQuestions">
          <p class="text-4xl font-semibold">
            POKAŻ: <span class="text-yellow-300 font-bold text-6xl">{{ expected }}</span>
          </p>
          <p class="text-2xl text-white mt-2">Wynik: {{ correctAnswers }}/{{ totalQuestions }}</p>
          <p class="text-2xl text-white mt-2">
            Pozostało: {{ totalQuestions - questionsAnswered }}
          </p>
        </div>
          <div
            v-if="totalQuestions === questionsAnswered"
            class="mt-4 p-4 bg-green-500 text-white rounded-lg text-lg text-center w-full"
          >
            <p>Test zakończony! Twój wynik to {{ correctAnswers }} na {{ totalQuestions }}.</p>
            <p v-if="badWords.length > 0">Niepoprawne odpowiedzi: {{ badWords.join(', ') }}</p>
            <p>Popracuj nad tymi znakami!</p>
          </div>
          <button
            v-if="questionsAnswered === totalQuestions"
            @click="restartTest"
            class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Ponów
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import VideoCapture from '@/components/VideoCapture.vue'
import TutorialTest from '@/components/TutorialTest.vue'
import { API_URL } from '@/config'

const audioSuccess = new Audio('src/assets/audio/success.mp3')

const totalQuestions = ref(5)
const chapter = 2
let words = []
let badWords = []
const correctAnswers = ref(0)
let questionsAnswered = ref(0)
let showTutorial = ref(true)
const showSuccess = ref(false)
const showBad = ref(false)
const showUnknown = ref(false)
const expected = ref('')
const result = ref({ label_name: 'none' })

function handleResultUpdate(newResult) {
  result.value = newResult
  console.log(result.value)
  if (result.value.label_name === expected.value) {
    showSuccess.value = true
    audioSuccess.play()
    correctAnswers.value++
    questionsAnswered.value++
    setTimeout(() => {
      showSuccess.value = false
    }, 1000)
    if (questionsAnswered.value < totalQuestions.value) {
      updateTestProgress()
    }
  } else if (result.value.label_name === 'Spróbuj ponownie!') {
    showUnknown.value = true
    setTimeout(() => {
      showUnknown.value = false
    }, 1000)
  } else {
    showBad.value = true
    badWords.push(expected.value)
    questionsAnswered.value++
    setTimeout(() => {
      showBad.value = false
    }, 1000)
    if (questionsAnswered.value < totalQuestions.value) {
      updateTestProgress()
    }
  }
}

function updateTestProgress() {
  words.shift()
  expected.value = words[0]
}

function restartTest() {
  correctAnswers.value = 0
  questionsAnswered.value = 0
  badWords = []
  fetchWords()
}

async function fetchWords() {
  try {
    const response = await fetch(`${API_URL}/get_words?chapter=${chapter}`)
    const data = await response.json()
    words = data.words
    expected.value = words[0]
  } catch (error) {
    console.error('Error fetching words:', error)
  }
}

onMounted(() => {
  fetchWords()
})
</script>

<style scoped>
.max-height {
  max-height: 80vh;
}

.animate-bounce {
  animation: bounce 1s;
}
@keyframes bounce {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(2);
  }
}
</style>
