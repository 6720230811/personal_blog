<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

const address = ref('正在获取位置...');
const loading = ref(true);

const fetchAddress = async () => {
  try {
    loading.value = true;
    const response = await axios.get('https://ipapi.co/json/');
    address.value = `${response.data.city}/${response.data.region}/${response.data.country_name}`;
  } catch (error) {
    address.value = '无法获取位置';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
   fetchAddress();
});
</script>

<template>
  <div class="address-container">
    <div class="icon-location">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/>
        <circle cx="12" cy="10" r="3"/>
      </svg>
    </div>
    <div class="address-text" :class="{ 'loading': loading }">{{ address }}</div>
  </div>
</template>

<style scoped>
.address-container {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 33.3%;
  color: rgba(255, 255, 255, 0.8);
  font-size: 14px;
  transition: all 0.3s ease;
}

.address-container:hover {
  color: #fff;
}

.icon-location {
  display: flex;
  align-items: center;
  color: #3dd6d0;
}

.address-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.loading {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.6;
  }
}

@media (max-width: 768px) {
  .address-container {
    width: 100%;
    justify-content: center;
  }
}
</style>