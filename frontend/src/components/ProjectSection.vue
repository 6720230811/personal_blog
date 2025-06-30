<template>
  <div class="project-section">
    <h2 class="section-title">精选项目</h2>
    <div v-if="!loading && currentProject" class="project">
      <div class="project-carousel">
        <img 
          v-for="(image, index) in projectImages" 
          :key="index" 
          :src="image" 
          :alt="`项目图片 ${index + 1}`" 
          v-show="currentImageIndex === index" 
          class="carousel-image"
        />
        <div class="carousel-overlay">
          <div class="overlay-content">
            <span class="project-tag">{{ currentProject.language || '案例展示' }}</span>
          </div>
        </div>
        <button class="nav-button prev" @click.stop="prevImage">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>
        <button class="nav-button next" @click.stop="nextImage">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
      <div class="carousel-indicators">
        <div 
          v-for="(image, index) in projectImages" 
          :key="index" 
          :class="{ active: currentImageIndex === index }"
          @click="setImage(index)"
        ></div>
      </div>
      <div class="project-details">
        <div class="left">
          <h3>{{ currentProject.name }}</h3>
          <div class="tech-tags">
            <span class="tech-tag" v-if="currentProject.language">{{ currentProject.language }}</span>
            <!-- <span class="tech-tag" v-for="(tag, index) in currentProject.tags" :key="index">{{ tag.name }}</span> -->
            <span class="tech-tag" v-if="!currentProject.tags || currentProject.tags.length === 0">开源项目</span>
          </div>
        </div>
        <div class="right">
          <p>{{ currentProject.description || '这是一个精彩的项目，包含了许多创新的功能和设计理念。' }}</p>
          <div class="action-buttons">
            <!-- <router-link to="/work" class="case-study-link">
              查看案例研究
              <span class="arrow-icon">→</span>
            </router-link> -->
            <a :href="currentProject.url" target="_blank" class="demo-link">
              查看项目
            </a>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="loading" class="loading">
      正在加载项目数据...
    </div>
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    <div v-else class="no-content">
      暂无精选项目
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      projects: [],
      featuredProjects: [], // 存储多个精选项目
      projectImages: [
        '/public/images/pt1.jpg',
        '/public/images/pt2.jpg',
        '/public/images/pt3.jpg',
      ],
      currentImageIndex: 0,
      autoplayInterval: null,
      loading: true,
      error: null
    };
  },
  computed: {
    // 当前显示的项目
    currentProject() {
      return this.featuredProjects.length > 0 ? 
        this.featuredProjects[this.currentImageIndex % this.featuredProjects.length] : null;
    }
  },
  mounted() {
    // 自动播放轮播图
    this.startAutoplay();
    // 获取项目数据
    this.fetchProjects();
  },
  beforeUnmount() {
    // 组件销毁时清除定时器
    this.stopAutoplay();
  },
  methods: {
    async fetchProjects() {
      try {
        this.loading = true;
        const response = await axios.get('http://localhost:8000/api/projects/');
        console.log('项目API响应:', response);
        
        if (response.data && response.data.results && response.data.results.length > 0) {
          this.projects = response.data.results;
          console.log('成功获取项目数据:', this.projects);
          
          // 获取精选项目（优先选择is_favorite为true的项目，然后是前3个项目）
          const favoriteProjects = this.projects.filter(project => project.is_favorite);
          if (favoriteProjects.length > 0) {
            this.featuredProjects = favoriteProjects;
          } else {
            // 如果没有标记为收藏的项目，就取前三个
            this.featuredProjects = this.projects.slice(0, 3);
          }
          
          // 确保featuredProjects长度不超过projectImages长度
          if (this.featuredProjects.length > this.projectImages.length) {
            this.featuredProjects = this.featuredProjects.slice(0, this.projectImages.length);
          }
          
          // 如果项目数少于图片数，复制项目填充
          while (this.featuredProjects.length < this.projectImages.length) {
            this.featuredProjects.push(this.featuredProjects[0]);
          }
        } else {
          console.log('API返回空数据，使用默认项目');
          // 如果没有数据，设置默认项目
          this.featuredProjects = [
            {
              id: 1,
              name: 'SFD-KD',
              description: '本研究提出结构化特征解耦知识蒸馏框架，以解决传统MSE蒸馏因对齐一阶统计量导致学生模型特征过度平滑的问题。同时创新性地解耦教师特征为均值主导的一阶分量与保留高阶细节的多阶分量，通过统计重建实现高效蒸馏，有效克服了协方差建模带来的各种挑战。',
              language: 'Python',
              url: 'https://github.com/user/sfd-kd',
              tags: [
                { name: 'Python' },
                { name: '深度学习' }
              ]
            },
            {
              id: 2,
              name: '编织你的独特人生之旅',
              description: '使用Next.js开发的灵活且高度可定制的设计系统，结合Figma进行设计协作，创造出独特的用户体验。通过精心设计的组件库和交互模式，帮助用户构建个性化的数字体验平台。',
              language: 'Next.js',
              url: 'https://github.com/user/project',
              tags: [
                { name: 'Figma' },
                { name: 'UI/UX' }
              ]
            },
            {
              id: 3,
              name: '智能助手系统',
              description: '基于Vue3和TypeScript开发的智能助手系统，整合多种API服务，提供智能问答、日程管理和数据分析功能。采用模块化设计，支持插件扩展，适配多种设备。',
              language: 'Vue',
              url: 'https://github.com/user/assistant',
              tags: [
                { name: 'TypeScript' },
                { name: 'Vue3' }
              ]
            }
          ];
        }
      } catch (error) {
        console.error('获取项目数据失败:', error);
        this.error = '无法连接到API服务器';
        // 出错时设置默认项目
        this.featuredProjects = [
          {
            id: 1,
            name: 'SFD-KD',
            description: '本研究提出结构化特征解耦知识蒸馏框架，以解决传统MSE蒸馏因对齐一阶统计量导致学生模型特征过度平滑的问题。同时创新性地解耦教师特征为均值主导的一阶分量与保留高阶细节的多阶分量，通过统计重建实现高效蒸馏，有效克服了协方差建模带来的各种挑战。',
            language: 'Python',
            url: 'https://github.com/user/sfd-kd',
            tags: [
              { name: 'Python' },
              { name: '深度学习' }
            ]
          },
          {
            id: 2,
            name: '编织你的独特人生之旅',
            description: '使用Next.js开发的灵活且高度可定制的设计系统，结合Figma进行设计协作，创造出独特的用户体验。通过精心设计的组件库和交互模式，帮助用户构建个性化的数字体验平台。',
            language: 'Next.js',
            url: 'https://github.com/user/project',
            tags: [
              { name: 'Figma' },
              { name: 'UI/UX' }
            ]
          },
          {
            id: 3,
            name: '智能助手系统',
            description: '基于Vue3和TypeScript开发的智能助手系统，整合多种API服务，提供智能问答、日程管理和数据分析功能。采用模块化设计，支持插件扩展，适配多种设备。',
            language: 'Vue',
            url: 'https://github.com/user/assistant',
            tags: [
              { name: 'TypeScript' },
              { name: 'Vue3' }
            ]
          }
        ];
      } finally {
        this.loading = false;
      }
    },
    nextImage() {
      this.currentImageIndex = (this.currentImageIndex + 1) % this.projectImages.length;
      this.resetAutoplay();
    },
    prevImage() {
      this.currentImageIndex = (this.currentImageIndex - 1 + this.projectImages.length) % this.projectImages.length;
      this.resetAutoplay();
    },
    setImage(index) {
      this.currentImageIndex = index;
      this.resetAutoplay();
    },
    startAutoplay() {
      this.autoplayInterval = setInterval(() => {
        this.nextImage();
      }, 4000);
    },
    stopAutoplay() {
      if (this.autoplayInterval) {
        clearInterval(this.autoplayInterval);
      }
    },
    resetAutoplay() {
      this.stopAutoplay();
      this.startAutoplay();
    }
  }
};
</script>

<style scoped>
.project-section {
  display: flex;
  flex-direction: column;
  width: 100%;
  margin-top: 60px;
  margin-bottom: 60px;
  padding: 2rem 0;
  color: #fff;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 3rem;
  text-align: left;
  position: relative;
  padding-left: 1.5rem;
  width: 95%;
}

.section-title::before {
  content: "";
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 8px;
  height: 70%;
  background: linear-gradient(to bottom, #3dd6d0, #2bc4be);
  border-radius: 4px;
}

.project {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 1.5rem;
  padding: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  width: 95%;
  margin: 0 auto;
}

.project:hover {
  box-shadow: 0 16px 60px rgba(0, 0, 0, 0.5);
  transform: translateY(-8px);
}

.project-carousel {
  width: 100%;
  height: 700px;
  border-radius: 1.2rem;
  margin-bottom: 1.5rem;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 1.2rem;
  position: absolute;
  top: 0;
  left: 0;
  transition: opacity 0.8s ease, transform 8s ease;
}

.carousel-image:hover {
  transform: scale(1.08);
}

.carousel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0,0,0,0.1), rgba(0,0,0,0.7));
  display: flex;
  align-items: flex-end;
  padding: 3rem;
  box-sizing: border-box;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.project-carousel:hover .carousel-overlay {
  opacity: 1;
}

.nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 20;
  opacity: 0;
}

.project-carousel:hover .nav-button {
  opacity: 1;
}

.nav-button.prev {
  left: 20px;
}

.nav-button.next {
  right: 20px;
}

.nav-button:hover {
  background-color: rgba(61, 214, 208, 0.8);
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 0 15px rgba(61, 214, 208, 0.5);
}

.nav-button svg {
  width: 24px;
  height: 24px;
}

.project-tag {
  background-color: rgba(61, 214, 208, 0.9);
  color: #000;
  font-weight: bold;
  padding: 0.6rem 2rem;
  border-radius: 2rem;
  font-size: 1.2rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.carousel-indicators {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 2rem 0;
}

.carousel-indicators div {
  width: 60px;
  height: 5px;
  margin: 0 8px;
  background-color: rgba(255, 255, 255, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 3px;
}

.carousel-indicators div:hover {
  background-color: rgba(255, 255, 255, 0.5);
}

.carousel-indicators div.active {
  background-color: #3dd6d0;
  width: 80px;
}

.project-details {
  display: flex;
  justify-content: space-between;
  width: 100%;
  padding: 2rem;
  gap: 4rem;
}

.project-details .left {
  flex: 1;
  text-align: left;
}

.project-details .left h3 {
  font-size: 2.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  line-height: 1.3;
  background: linear-gradient(to right, #ffffff, #3dd6d0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}

.tech-tag {
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1.2rem;
  border-radius: 2rem;
  font-size: 1rem;
  color: #ccc;
  transition: all 0.3s ease;
}

.tech-tag:hover {
  background-color: rgba(61, 214, 208, 0.1);
  border-color: rgba(61, 214, 208, 0.3);
  color: #3dd6d0;
  transform: translateY(-3px);
}

.project-details .right {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex: 2;
  text-align: left;
}

.project-details .right p {
  margin-bottom: 2.5rem;
  line-height: 1.8;
  font-size: 1.3rem;
  color: rgba(255, 255, 255, 0.8);
}

.action-buttons {
  display: flex;
  gap: 1.5rem;
  width: 100%;
}

.case-study-link {
  font-size: 1.2rem;
  color: #3dd6d0;
  text-decoration: none;
  padding: 1rem 2rem;
  background-color: rgba(61, 214, 208, 0.1);
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(61, 214, 208, 0.3);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1;
  justify-content: center;
}

.demo-link {
  font-size: 1.2rem;
  color: #fff;
  text-decoration: none;
  padding: 1rem 2rem;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 0.5rem;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
  flex: 1;
  text-align: center;
}

.demo-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.1);
}

.arrow-icon {
  transition: transform 0.3s ease;
}

.case-study-link:hover {
  background-color: rgba(61, 214, 208, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(61, 214, 208, 0.2);
}

.case-study-link:hover .arrow-icon {
  transform: translateX(8px);
}

@media (max-width: 1600px) {
  .project {
    max-width: 1600px;
  }
  
  .project-carousel {
    height: 600px;
  }
  
  .project-details .left h3 {
    font-size: 2.4rem;
  }
  
  .project-details .right p {
    font-size: 1.2rem;
  }
}

@media (max-width: 1200px) {
  .project-carousel {
    height: 500px;
  }
  
  .project-details .left h3 {
    font-size: 2.2rem;
  }
  
  .section-title {
    font-size: 2.5rem;
  }
}

@media (max-width: 992px) {
  .project-carousel {
    height: 450px;
  }
  
  .project-details {
    flex-direction: column;
    gap: 2rem;
  }
  
  .project-details .left {
    margin-right: 0;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .project-section {
    padding: 1.5rem 0;
    margin-top: 40px;
    margin-bottom: 40px;
  }
  
  .section-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }
  
  .project {
    padding: 1.5rem;
  }
  
  .project-carousel {
    height: 400px;
  }
  
  .project-details {
    padding: 1.5rem 1rem;
  }
  
  .project-details .left h3 {
    font-size: 1.8rem;
  }
  
  .project-details .right p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }
  
  .nav-button {
    width: 40px;
    height: 40px;
  }
  
  .nav-button.prev {
    left: 10px;
  }
  
  .nav-button.next {
    right: 10px;
  }
  
  .nav-button svg {
    width: 20px;
    height: 20px;
  }
}

@media (max-width: 576px) {
  .project {
    width: 92%;
    padding: 1rem;
  }
  
  .section-title {
    font-size: 1.8rem;
    width: 92%;
  }
  
  .project-carousel {
    height: 300px;
  }
  
  .project-details .left h3 {
    font-size: 1.6rem;
  }
  
  .project-details .right p {
    font-size: 1rem;
  }
  
  .carousel-indicators div {
    width: 40px;
  }
  
  .case-study-link, .demo-link {
    width: 100%;
    padding: 0.8rem 1.5rem;
    font-size: 1.1rem;
  }
  
  .carousel-overlay {
    padding: 1.5rem;
  }
  
  .project-tag {
    padding: 0.4rem 1.2rem;
    font-size: 0.9rem;
  }
  
  .nav-button {
    width: 36px;
    height: 36px;
    opacity: 0.7;
  }
  
  .nav-button svg {
    width: 16px;
    height: 16px;
  }
}

.loading {
  font-size: 1.2rem;
  color: #ccc;
  margin: 2rem 0;
  text-align: center;
  padding: 3rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 95%;
  margin: 0 auto;
}

.error {
  font-size: 1.2rem;
  color: #ff6b6b;
  margin: 2rem 0;
  text-align: center;
  padding: 3rem;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 1rem;
  border: 1px solid rgba(255, 107, 107, 0.2);
  width: 95%;
  margin: 0 auto;
}

.no-content {
  font-size: 1.2rem;
  color: #ccc;
  margin: 2rem 0;
  text-align: center;
  padding: 3rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 95%;
  margin: 0 auto;
}
</style>