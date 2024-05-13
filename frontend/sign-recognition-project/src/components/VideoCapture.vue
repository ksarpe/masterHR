<template>
  <div>
    <video ref="videoElement" autoplay></video>
    <button @click="captureFrame">Click here to send your answer</button>
  </div>
  <div v-if="result">
    <p>Label: {{ result.label_name }}</p>
    <p>Handedness: {{ result.handedness }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive, onBeforeUnmount } from 'vue'

const videoElement = ref(null)
const result = reactive({ label_name: 'none', handedness: 'none' })

onMounted(() => {
  setupVideo()
})

onBeforeUnmount(() => {
  if (videoElement.value) {
    videoElement.value.srcObject.getTracks().forEach((track) => {
      track.stop()
    })
  }
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
          result.handedness = data.handedness
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
