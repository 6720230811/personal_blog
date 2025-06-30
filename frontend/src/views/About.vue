<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import userinfo from '../components/userinfo.vue';
import WorkExperience from '../components/WorkExperience.vue';
import study from '../components/study.vue';
import skills from '../components/skills.vue';

const components = ref([]);
const owner = ref({
  github_url:'',
  country: '',
  city: '',
  avatar_url: '/images/pt2.jpg'
});
const isLoaded = ref(false);

// 获取博客所有者信息
async function fetchOwnerInfo() {
  try {
    const response = await axios.get('http://localhost:8000/api/owner/');
    if (response.data && response.data.results && response.data.results.length > 0) {
      owner.value = response.data.results[0];
    } else {
      // 如果没有数据，设置默认值
      owner.value = {
        github_url:'',
        country: '中国',
        city: '江西',
        avatar_url: '/images/pt2.jpg'
      };
    }
  } catch (error) {
    console.error('Failed to fetch owner location info:', error);
    // 出错时设置默认值
    owner.value = {
      github_url:'',
      country: 'Asia',
      city: 'Jakarta',
      avatar_url: '/images/pt2.jpg'
    };
  } finally {
    // 无论成功或失败，都标记为已加载
    setTimeout(() => {
      isLoaded.value = true;
    }, 300);
  }
}

onMounted(() => {
  fetchOwnerInfo();
});
</script>

<template>
  <div class="about-container" :class="{ 'loaded': isLoaded }">
    <div class="about-content">
      <div class="left-content fixed-element">
        <div class="profile-card">
          <div class="profile-picture">
            <img :src="owner.avatar_url || '/images/pt2.jpg'" alt="Profile Picture">
            <div class="profile-glow"></div>
          </div>
          <div class="location-info">
            <i class="location-icon"></i>
            {{ owner.country || 'Asia' }}/{{ owner.city || 'Jakarta' }}
          </div>
          <div class="social-links">
            <a :href="owner.github_url" class="social-link" title="GitHub">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
            </a>
            <a href="#" class="social-link" title="LinkedIn">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
            </a>
            <a href="#" class="social-link" title="Twitter">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
            </a>
            <a href="#" class="social-link" title="Dribbble">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M8.56 2.75c4.37 6.03 6.02 9.42 8.03 17.72m2.54-15.38c-3.72 4.35-8.94 5.66-16.88 5.85m19.5 1.9c-3.5-.93-6.63-.82-8.94 0-2.58.92-5.01 2.86-7.44 6.32"></path></svg>
            </a>
          </div>
        </div>
      </div>
      <div class="right-content">
        <div class="section-wrapper">
          <userinfo/>
        </div>
        <div class="section-wrapper">
          <WorkExperience/>
        </div>
        <div class="section-wrapper">
          <study/>
        </div>
        <div class="section-wrapper">
          <skills/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-container {
  width: 100%;
  min-height: calc(100vh - 60px);
  padding: 3rem 0;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.about-container.loaded {
  opacity: 1;
  transform: translateY(0);
}

.about-content {
  display: flex;
  max-width: 1600px;
  margin: 0 auto;
  gap: 4rem;
  padding: 0 2rem;
}

.left-content {
  width: 30%;
  position: sticky;
  top: 120px;
  height: fit-content;
}

.profile-card {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 20px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.profile-card:hover {
  border-color: rgba(61, 214, 208, 0.3);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(61, 214, 208, 0.1);
  transform: translateY(-5px);
}

.profile-picture {
  width: 180px;
  height: 180px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 1.5rem;
  position: relative;
  border: 3px solid rgba(61, 214, 208, 0.3);
  box-shadow: 0 0 20px rgba(61, 214, 208, 0.2);
}

.profile-picture img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.profile-picture:hover img {
  transform: scale(1.05);
}

.profile-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 50%;
  background: radial-gradient(circle at 50% 50%, rgba(61, 214, 208, 0.2), transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.profile-picture:hover .profile-glow {
  opacity: 1;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 2rem;
  padding: 0.6rem 1.2rem;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 50px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.location-info:hover {
  background: rgba(61, 214, 208, 0.1);
  border-color: rgba(61, 214, 208, 0.3);
  transform: translateY(-2px);
}

.location-icon {
  display: inline-block;
  width: 16px;
  height: 16px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%233dd6d0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z'%3E%3C/path%3E%3Ccircle cx='12' cy='10' r='3'%3E%3C/circle%3E%3C/svg%3E");
  background-size: contain;
  background-repeat: no-repeat;
  margin-right: 5px;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 0.5rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.social-link:hover {
  background: rgba(61, 214, 208, 0.1);
  color: #3dd6d0;
  border-color: rgba(61, 214, 208, 0.3);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.right-content {
  width: 70%;
  padding-top: 1rem;
}

.section-wrapper {
  margin-bottom: 5rem;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.8s ease forwards;
}

.section-wrapper:nth-child(1) {
  animation-delay: 0.2s;
}

.section-wrapper:nth-child(2) {
  animation-delay: 0.4s;
}

.section-wrapper:nth-child(3) {
  animation-delay: 0.6s;
}

.section-wrapper:nth-child(4) {
  animation-delay: 0.8s;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1200px) {
  .about-content {
    gap: 3rem;
  }
}

@media (max-width: 992px) {
  .about-content {
    flex-direction: column;
  }
  
  .left-content {
    width: 100%;
    position: relative;
    top: 0;
    margin-bottom: 3rem;
  }
  
  .right-content {
    width: 100%;
  }
  
  .profile-card {
    max-width: 500px;
    margin: 0 auto;
  }
}

@media (max-width: 576px) {
  .about-container {
    padding: 2rem 0;
  }
  
  .about-content {
    padding: 0 1rem;
  }
  
  .profile-picture {
    width: 150px;
    height: 150px;
  }
}
</style>
