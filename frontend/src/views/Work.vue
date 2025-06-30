<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ProjectSection from '../components/ProjectSection.vue';
</script>

<template>
  <div class="work-container">
    <h1 class="work-title">我的项目作品</h1>
    <ProjectSection />
  </div>
</template>

<style scoped>
.work-container {
  width: 100%;
  max-width: 1800px;
  margin: 0 auto;
  padding: var(--spacing-lg) 0;
  animation: fadeIn 0.5s ease;
}

.work-title {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2.5rem;
  background: linear-gradient(to right, #ffffff, #3dd6d0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 2px 10px rgba(61, 214, 208, 0.3);
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 768px) {
  .work-container {
    padding: var(--spacing-md) 0;
  }
  
  .work-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }
}

@media (max-width: 576px) {
  .work-container {
    padding: var(--spacing-sm) 0;
  }
  
  .work-title {
    font-size: 1.8rem;
    margin-bottom: 1rem;
  }
}
</style>
