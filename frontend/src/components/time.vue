<script setup lang="ts">
import { ref, onMounted } from 'vue';

const currentTime = ref('');
const currentDate = ref('');

const updateTime = () => {
  const now = new Date();
  
  // 更新时间
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  currentTime.value = `${hours}:${minutes}:${seconds}`;
  
  // 更新日期
  const options: Intl.DateTimeFormatOptions = { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric', 
    weekday: 'long' 
  };
  currentDate.value = now.toLocaleDateString('zh-CN', options);
};

onMounted(() => {
  updateTime();
  setInterval(updateTime, 1000);
});
</script>

<template>
  <div class="time-container">
    <div class="time-icon">
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <polyline points="12 6 12 12 16 14"></polyline>
      </svg>
    </div>
    <div class="time-content">
      <div class="current-time">{{ currentTime }}</div>
      <div class="current-date">{{ currentDate }}</div>
    </div>
  </div>
</template>

<style scoped>
.time-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  width: 33.3%;
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.time-container:hover {
  color: #fff;
}

.time-icon {
  display: flex;
  align-items: center;
  color: #3dd6d0;
}

.time-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.current-time {
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.5px;
}

.current-date {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.6);
}

@media (max-width: 992px) {
  .current-date {
    display: none;
  }
}

@media (max-width: 768px) {
  .time-container {
    width: 100%;
    justify-content: center;
  }
  
  .time-content {
    align-items: center;
  }
}
</style>