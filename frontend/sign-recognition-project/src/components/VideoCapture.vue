<template>
  <div class="flex h-screen">
    <div class="w-full p-12">
      <div class="bg-gray-400 shadow-lg rounded-3xl p-4">
        <video ref="videoElement" autoplay class="w-full h-auto rounded-3xl"></video>
        <button
          @click="captureFrame"
          class="mt-4 w-full bg-gray-800 text-white py-2 rounded-3xl hover:bg-blue-600 font-bold text-xl"
        >
          Naciśnij tutaj aby przesłać obraz, albo po prostu wciśnij enter!
        </button>
      </div>
      <div class="mt-3 p-3 bg-gray-400 rounded-lg flex space-x-4 text-gray-700 justify-center">
        <p class="text-2xl font-bold">
          CO ZOSTAŁO WYKRYTE: <span class="font-bold text-blue-700">{{ result.label_name }}</span>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, onBeforeUnmount, watch } from 'vue'

const videoElement = ref(null)
const result = reactive({ label_name: 'nie wykryto', handedness: 'nie wykryto' })

watch(
  result,
  (newResult) => {
    emit('update:result', newResult)
  },
  { deep: true }
)

defineProps()
const emit = defineEmits(['update:result'])

function handleKeydown(event) {
  if (event.code === 'Enter' || event.keyCode === 13) {
    captureFrame()
  }
}

onMounted(() => {
  setupVideo()
  document.addEventListener('keydown', handleKeydown)
})

onBeforeUnmount(() => {
  if (videoElement.value) {
    videoElement.value.srcObject.getTracks().forEach((track) => {
      track.stop()
    })
  }
  document.removeEventListener('keydown', handleKeydown)
})

const setupVideo = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
    }
  } catch (error) {
    console.error('Error accessing the camera:', error)
  }
}

const convert_data = (data) => {
  if (data === 'Right') {
    return 'Prawa'
  } else if (data === 'Left') {
    return 'Lewa'
  } else {
    return 'nie wykryto'
  }
}

const captureFrame = () => {
  const canvas = document.createElement('canvas')
  if (videoElement.value) {
    canvas.width = videoElement.value.videoWidth
    canvas.height = videoElement.value.videoHeight
    const ctx = canvas.getContext('2d')
    ctx.drawImage(videoElement.value, 0, 0, canvas.width, canvas.height)
    canvas.toBlob(async (blob) => {
      const formData = new FormData()
      formData.append('file', blob, 'frame.png')

      try {
        const response = await fetch('http://localhost:5000/process_frame', {
          method: 'POST',
          body: formData
        })
        const data = await response.json()
        if (response.ok) {
          result.label_name = data.label_name
          result.handedness = convert_data(data.handedness)
        } else {
          console.error('Error from server:', data)
        }
      } catch (error) {
        console.error('Error:', error)
      }
    })
  }
}
</script>
