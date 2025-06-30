<script setup lang="ts">
import { ref, onMounted } from 'vue';
import HeroSection from '../components/HeroSection.vue';
import ProjectSection from '../components/ProjectSection.vue';
import BlogSection from '../components/BlogSection.vue';
import SubscribeSection from '../components/SubscribeSection.vue';
import Gallery from '../components/gallyer.vue';
import Footer from '../components/Footer.vue';

// 可以添加任何首页所需的数据和逻辑
const pageReady = ref(false);

onMounted(() => {
  // 延迟一小段时间确保组件完全加载
  setTimeout(() => {
    pageReady.value = true;
  }, 100);
});
</script>
<template>
      <div class="main-content">
    <div class="content-container">
          <HeroSection />
    </div>
    <div class="full-width-section">
          <ProjectSection />
    </div>
    <div class="content-container">
          <BlogSection />
      <Gallery />
          <SubscribeSection />
      </div>
      </div>
</template>

<style scoped>
.main-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin: 0 auto;
  padding: var(--spacing-lg) 0;
  animation: fadeIn 0.5s ease;
}

.content-container {
  max-width: 1400px;
  margin: 0 auto;
  width: 95%;
}

.full-width-section {
  width: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: center;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@media (max-width: 1600px) {
  .content-container {
    max-width: 1200px;
  }
}

@media (max-width: 768px) {
  .content-container {
    width: 95%;
}

.main-content {
    padding: var(--spacing-md) 0;
  }
}

@media (max-width: 576px) {
  .content-container {
    width: 100%;
    padding: 0 var(--spacing-sm);
}
}
</style>

