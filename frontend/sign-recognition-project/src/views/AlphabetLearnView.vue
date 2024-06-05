<template>
  <tutorial v-if="showTutorial" @close="showTutorial = false" />
  <div class="flex items-center text-center pt-4 px-12">
    <p class="text-2xl font-semibold text-white mr-4">CHAPTER I - POSTAWY I</p>
    <input type="checkbox" v-model="showImagesRandomly" class="form-checkbox h-5 w-5 mr-2 ml-12" />
    <span class="text-white">Losowo pokazuj bez zdjęć (50%)</span>
  </div>

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
      Nie wykryto! <br>
      Spróbuj jeszcze raz.
    </div>
  </div>
  <div class="mx-auto grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div>
      <video-capture :chapter-number="chapter" @update:result="handleResultUpdate" />
    </div>
    <div class="flex h-screen">
      <div class="w-full max-height p-12">
        <div class="bg-gray-400 shadow-lg rounded-3xl p-4">
          <img
            v-if="imageSrc"
            :src="imageSrc"
            alt="Detected Sign"
            class="w-full h-auto rounded-3xl"
          />
        </div>
        <div
          v-if="result"
          class="mt-4 p-7 bg-gray-400 rounded-lg flex space-x-4 text-gray-700 justify-center h-auto"
        >
          <p class="text-4xl font-semibold">
            POKAŻ: <span class="text-yellow-300 font-bold text-6xl">{{ expected }}</span>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import VideoCapture from '@/components/VideoCapture.vue'
import Tutorial from '@/components/Tutorial.vue'
import { API_URL } from '@/config'

const chapter = 2
const audioSuccess = new Audio('src/assets/audio/success.mp3')
let words = []
let showTutorial = ref(true)

const showSuccess = ref(false)
const showBad = ref(false)
const showUnknown = ref(false)
const expected = ref('')
const result = ref({ label_name: 'none'})
const imageSrc = ref('')
const showImagesRandomly = ref(false) // This will control the random image display

function handleResultUpdate(newResult) {
  result.value = newResult
  console.log(showImagesRandomly.value)
  console.log('Result:', result.value.label_name)
  console.log('Expected:', expected.value)
  if (result.value.label_name === expected.value) {
    showSuccess.value = true
    audioSuccess.play()
    setTimeout(() => {
      showSuccess.value = false
    }, 1000) // Hide success message after 2 seconds

    words.shift()
    if (words.length === 0) {
      fetchWords()
    } else {
      expected.value = words[0]
      if (!showImagesRandomly.value) {
        imageSrc.value = 'src/assets/chapter2_images/' + expected.value + '.png'
      } else {
        // calculate change to not display an image
        let random = Math.floor(Math.random() * 2)
        if (random === 0) {
          imageSrc.value = ''
        } else {
          imageSrc.value = 'src/assets/chapter2_images/' + expected.value + '.png'
        }
      }
    }
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
}

async function fetchWords() {
  try {
    const response = await fetch(`${API_URL}/get_words?chapter=${chapter}`)
    const data = await response.json()
    words = data.words
    expected.value = words[0]
    imageSrc.value = 'src/assets/chapter2_images/' + expected.value + '.png'
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
