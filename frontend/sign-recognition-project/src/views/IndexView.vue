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
    canvas.toBlob((blob) => {
      // Send this blob to the backend
      console.log(blob); // Just for demonstration, replace with API call
    });
  }
};
</script>