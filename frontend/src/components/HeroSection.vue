<template>
  <div class="hero-section">
    <div class="content">
      <div class="hero-left">
        <div class="title">
          <h1>{{ owner.identity || '设计工程师' }}</h1>
        </div>
        <div class="description">
          <p>
            {{ owner.bio || '我是adgo，一名在FLY工作的设计工程师，专注于打造直观的用户体验。工作之余，我也会构建自己的项目。' }}
          </p>
        </div>
        <div class="button-container">
          <a class="button" href="/about">
            <div class="button-content">
              <div class="avatar">
                <img :src="owner.avatar_url || '/public/images/pt.jpg'" alt="Avatar" />
              </div>
              <span>关于我</span>
            </div>
            <div class="arrow">
              <span class="arrow-icon">→</span>
            </div>
          </a>
          <a class="button secondary" href="/work">
            <div class="button-content">
              <span>查看作品</span>
            </div>
          </a>
        </div>
        <div class="social-links">
          <a :href="owner.github_url" class="social-link" title="GitHub" target="_blank" v-if="owner.github_url">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
          </a>
          <a href="#" class="social-link" title="Twitter">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 4s-.7 2.1-2 3.4c1.6 10-9.4 17.3-18 11.6 2.2.1 4.4-.6 6-2C3 15.5.5 9.6 3 5c2.2 2.6 5.6 4.1 9 4-.9-4.2 4-6.6 7-3.8 1.1 0 3-1.2 3-1.2z"></path></svg>
          </a>
          <a href="#" class="social-link" title="LinkedIn">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
          </a>
        </div>
      </div>
      <div class="hero-right">
        <div class="hero-image">
          <img :src="owner.avatar_url || '/public/images/pt.jpg'" alt="Hero Image" />
          <div class="image-overlay"></div>
        </div>
      </div>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      owner: {
        username: '',
        identity: '',
        bio: '',
        avatar_url: '',
        github_url: '',
        github_username: ''
      },
      loading: true,
      error: null
    };
  },
  mounted() {
    this.fetchOwnerInfo();
  },
  methods: {
    async fetchOwnerInfo() {
      try {
        console.log('尝试获取所有者信息...');
        // 获取博客所有者信息的API端点
        const response = await axios.get('http://localhost:8000/api/owner/');
        console.log('API响应:', response);
        
        if (response.data && response.data.results && response.data.results.length > 0) {
          this.owner = response.data.results[0]; // 获取第一个结果
          console.log('成功获取所有者信息:', this.owner);
        } else {
          console.log('API返回空数据，使用默认值');
          this.owner = {
            username: 'adgo',
            identity: '设计工程师和开发者',
            bio: '我是adgo，一名在FLY工作的设计工程师，专注于打造直观的用户体验。工作之余，我也会构建自己的项目。',
            avatar_url: '/public/images/pt.jpg'
          };
        }
      } catch (error) {
        console.error('获取所有者信息失败:', error);
        this.error = '无法连接到API服务器';
        // 使用默认值
        this.owner = {
          username: 'adgo',
          identity: '设计工程师和开发者',
          bio: '我是adgo，一名在FLY工作的设计工程师，专注于打造直观的用户体验。工作之余，我也会构建自己的项目。',
          avatar_url: '/public/images/pt.jpg'
        };
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.hero-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 1400px;
  padding: 5rem 2rem;
  color: #fff;
  margin: 0 auto;
}

.content {
  display: flex;
  width: 100%;
  gap: 4rem;
}

.hero-left {
  flex: 1.2;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-image {
  width: 100%;
  height: 500px;
  border-radius: 1.5rem;
  overflow: hidden;
  position: relative;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  transform: perspective(1000px) rotateY(-5deg);
  transition: transform 0.5s ease;
}

.hero-image:hover {
  transform: perspective(1000px) rotateY(0deg);
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 5s ease;
}

.hero-image:hover img {
  transform: scale(1.1);
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom right, rgba(61, 214, 208, 0.3), rgba(0, 0, 0, 0.5));
}

.title {
  display: flex;
  justify-content: flex-start;
  width: 100%;
  margin-bottom: 2rem;
}

.title h1 {
  font-size: 4.5rem;
  font-weight: bold;
  color: #fff;
  line-height: 1.2;
  background: linear-gradient(to right, #ffffff, #3dd6d0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: fadeIn 1s ease-out;
}

.description {
  padding-bottom: 2.5rem;
  display: flex;
  justify-content: flex-start;
  width: 100%;
  animation: fadeIn 1.2s ease-out;
}

.description p {
  font-size: 1.5rem;
  line-height: 1.7;
  color: rgba(255, 255, 255, 0.8);
}

.button-container {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  animation: fadeIn 1.4s ease-out;
}

.button {
  display: flex;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #3dd6d0;
  border-radius: 2rem;
  text-decoration: none;
  color: #000;
  font-weight: 600;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(61, 214, 208, 0.3);
}

.button:hover {
  background-color: #2bc4be;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(61, 214, 208, 0.4);
}

.button.secondary {
  background-color: transparent;
  border: 2px solid #3dd6d0;
  color: #3dd6d0;
  box-shadow: none;
}

.button.secondary:hover {
  background-color: rgba(61, 214, 208, 0.1);
  transform: translateY(-3px);
}

.button-content {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 2.2rem;
  height: 2.2rem;
  border: 2px solid #000;
  border-radius: 50%;
  overflow: hidden;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.arrow {
  display: flex;
  align-items: center;
  margin-left: 0.8rem;
  opacity: 0;
  transition: all 0.3s ease;
}

.arrow-icon {
  font-size: 1.3rem;
  transition: transform 0.3s ease;
}

.button:hover .arrow {
  opacity: 1;
}

.button:hover .arrow-icon {
  transform: translateX(5px);
}

.social-links {
  display: flex;
  gap: 1.2rem;
  margin-top: 1.5rem;
  animation: fadeIn 1.6s ease-out;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
  transition: all 0.3s ease;
}

.social-link:hover {
  background-color: #3dd6d0;
  color: #000;
  transform: translateY(-3px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式样式 */
@media (max-width: 1600px) {
  .hero-section {
    max-width: 1200px;
  }
}

@media (max-width: 1200px) {
  .title h1 {
    font-size: 3.8rem;
  }
  
  .description p {
    font-size: 1.4rem;
  }
  
  .hero-image {
    height: 450px;
  }
}

@media (max-width: 992px) {
  .content {
    flex-direction: column;
  }
  
  .hero-left {
    order: 2;
  }
  
  .hero-right {
    order: 1;
    margin-bottom: 2rem;
  }
  
  .hero-image {
    height: 400px;
    transform: perspective(1000px) rotateY(0deg);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 3rem 1rem;
  }
  
  .title h1 {
    font-size: 3rem;
  }
  
  .description p {
    font-size: 1.2rem;
  }
  
  .button-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .button {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 2rem 1rem;
  }
  
  .title h1 {
    font-size: 2.5rem;
  }
  
  .description p {
    font-size: 1.1rem;
  }
  
  .hero-image {
    height: 250px;
  }
}

.loading {
  text-align: center;
  margin-top: 20px;
  font-size: 1.2rem;
  color: #3dd6d0;
}

.error {
  text-align: center;
  margin-top: 20px;
  color: #ff6b6b;
  font-size: 1.2rem;
}
</style>