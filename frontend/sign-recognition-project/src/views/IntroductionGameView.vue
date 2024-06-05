<template>
  <tutorial-game v-if="showTutorial" @close="showTutorial = false" />
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
  <div class="flex items-center text-center pt-4 px-12">
    <p class="text-2xl font-semibold text-white mr-12">GRA I - POSTAWY I</p>
    <div v-if="!testStarted">
      <label class="text-white font-medium">
        <input type="radio" :value="30" v-model.number="testDuration" name="time" class="mr-2" />30
        sekund
      </label>
      <label class="text-white font-medium ml-4">
        <input type="radio" :value="45" v-model.number="testDuration" name="time" class="mr-2" />45
        sekund
      </label>
    </div>
  </div>

  <div class="flex w-full justify-center items-center">
    <div class="mx-auto grid grid-cols-1 lg:grid-cols-2 lg:gap-6">
      <div>
        <video-capture :chapter-number="chapter" @update:result="handleResultUpdate" />
      </div>
      <div class="flex-1 flex flex-col items-center justify-center">
        <div
          class="p-7 bg-gray-400 rounded-lg flex flex-col items-center justify-center w-full text-center"
        >
          <button
            v-if="!testStarted"
            @click="startTest"
            class="bg-blue-500 hover:bg-blue-700 text-white text-6xl font-bold p-8 rounded"
          >
            Start
          </button>
          <div v-if="testStarted">
            <p class="text-4xl font-semibold">
              POKAŻ: <span class="text-yellow-300 font-bold text-6xl">{{ expected }}</span>
            </p>
            <p class="text-2xl text-white mt-2">Czas: {{ timeLeft }} sekund</p>
            <p class="text-2xl text-white mt-2">Wynik: {{ correctAnswers }}</p>
            <div
              v-if="testComplete"
              class="mt-4 p-4 bg-green-500 text-white rounded-lg text-lg text-center w-full"
            >
              <p>Gra zakończona! Twój wynik to {{ correctAnswers }}.</p>
              <button
                @click="restartTest"
                class="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >
                Ponów
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import VideoCapture from '@/components/VideoCapture.vue'
import TutorialGame from '@/components/TutorialGame.vue'
import { API_URL } from '@/config'

const audioSuccess = new Audio('src/assets/audio/success.mp3')
const showSuccess = ref(false)
const showBad = ref(false)
const showUnknown = ref(false)

const testDuration = ref(30)
const chapter = 1
let words = []
const correctAnswers = ref(0)
let showTutorial = ref(true)
const testStarted = ref(false)
const testComplete = ref(false)
const timeLeft = ref(testDuration.value)
const expected = ref('')
const result = ref({ label_name: 'none' })

// watch(testDuration, (newValue) => {
//   timeLeft.value = newValue
//   if (!testStarted.value) {
//     restartTest()
//   }
// })
watch(testDuration, (newDuration) => {
  timeLeft.value = parseInt(newDuration, 10) // Ensure timeLeft is updated when testDuration changes
  correctAnswers.value = 0 // Reset correctAnswers when testDuration changes
})

function handleResultUpdate(newResult) {
  result.value = newResult
  if (testStarted.value && !testComplete.value) {
    checkAnswer()
  }
}

function checkAnswer() {
  if (result.value.label_name === expected.value) {
    showSuccess.value = true
    audioSuccess.play()
    setTimeout(() => {
      showSuccess.value = false
    }, 1000) // Hide success message after 2 seconds
    correctAnswers.value++
    timeLeft.value += 1
  }
  else if(result.value.label_name === 'Spróbuj ponownie!') {
    showUnknown.value = true
    setTimeout(() => {
      showUnknown.value = false
    }, 2000) // Hide success message after 2 second
  }
  else {
    showBad.value = true
    //audioSuccess.play()
    setTimeout(() => {
      showBad.value = false
    }, 1000) // Hide success message after 2 second
  }
  updateTestProgress()
}

function updateTestProgress() {
  const randomIndex = Math.floor(Math.random() * words.length)
  expected.value = words[randomIndex]
}

function startTest() {
  testStarted.value = true
  startTimer()
}

function restartTest() {
  correctAnswers.value = 0
  testStarted.value = false
  testComplete.value = false
  timeLeft.value = testDuration
  fetchWords()
}

function finishTest() {
  testComplete.value = true
}

function startTimer() {
  const interval = setInterval(() => {
    if (timeLeft.value > 0 && testStarted.value) {
      timeLeft.value--
    } else {
      clearInterval(interval)
      if (testStarted.value) {
        finishTest()
      }
    }
  }, 1000)
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
