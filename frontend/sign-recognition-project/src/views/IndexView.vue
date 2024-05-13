<template>
  <div>
    <video ref="videoElement" autoplay></video>
    <button @click="captureFrame">Capture Frame</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const videoElement = ref(null);

onMounted(() => {
  setupVideo();
});

const setupVideo = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    if (videoElement.value) {
      videoElement.value.srcObject = stream;
    }
  } catch (error) {
    console.error("Error accessing the camera:", error);
  }
};

const captureFrame = () => {
  const canvas = document.createElement('canvas');
  if (videoElement.value) {
    canvas.width = videoElement.value.videoWidth;
    canvas.height = videoElement.value.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement.value, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(async (blob) => {
      const formData = new FormData();
      formData.append('file', blob, 'frame.png');

      try {
        const response = await fetch('http://localhost:5000/process_frame', {
          method: 'POST',
          body: formData,
        });
        const result = await response.json();
        console.log(result);
      } catch (error) {
        console.error('Error:', error);
      }
    });
  }
};
</script>