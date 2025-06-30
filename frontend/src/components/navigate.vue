<template>
    <div class="navigate">
      <nav class="nav-container">
        <div class="nav-links">
          <RouterLink to="/" active-class="active" class="nav-link home">
            <div class="link-content">
              <img src="/public/icon/home.ico" class="icon home-icon">
              <span class="link-text">Home</span>
            </div>
          </RouterLink>
          <RouterLink to="/about" active-class="active" class="nav-link">
            <div class="link-content">
              <img src="/public/icon/about.ico" class="icon">
              <span class="link-text">About</span>
            </div>
          </RouterLink>
          <RouterLink to="/work" active-class="active" class="nav-link">
            <div class="link-content">
              <img src="/public/icon/work.ico" class="icon">
              <span class="link-text">Work</span>
            </div>
          </RouterLink>
          <RouterLink to="/blog" active-class="active" class="nav-link">
            <div class="link-content">
              <img src="/public/icon/blog.ico" class="icon">
              <span class="link-text">Blog</span>
            </div>
          </RouterLink>
          <RouterLink to="/github" active-class="active" class="nav-link">
            <div class="link-content">
              <img src="/public/icon/gallyer.ico" class="icon">
              <span class="link-text">GitHub</span>
            </div>
          </RouterLink>
          <div class="nav-indicator"></div>
        </div>
      </nav>
    </div>
  </template>
  

<script lang="ts" setup>
  import { RouterLink, useRoute } from 'vue-router'
  import { ref, onMounted, watch } from 'vue'
  
  const route = useRoute()
  
  // 更新指示器位置的函数
  const updateIndicator = () => {
    // 简单地查找带有active类的链接
    const activeLink = document.querySelector('.nav-link.active') as HTMLElement
    const indicator = document.querySelector('.nav-indicator') as HTMLElement
    
    if (activeLink && indicator) {
      indicator.style.width = `${activeLink.offsetWidth}px`
      indicator.style.left = `${activeLink.offsetLeft}px`
    }
  }
  
  // 监听路由变化
  watch(() => route.path, () => {
    // 给DOM更新一点时间
    setTimeout(updateIndicator, 50)
  })
  
  onMounted(() => {
    // 初始化时更新指示器
    setTimeout(updateIndicator, 50)
    
    // 窗口大小变化时重新计算
    window.addEventListener('resize', updateIndicator)
  })
</script>

<style scoped>
  .navigate {
    display: flex;
    justify-content: center;
    width: 33.4%;
  }
  
  .nav-container {
    position: relative;
    background-color: rgba(0, 0, 0, 0.3);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 50px;
    padding: 5px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    width: 500px;
    height: 40px;
    transition: all 0.3s ease;
  }
  
  .nav-container:hover {
    box-shadow: 0 8px 25px rgba(61, 214, 208, 0.15);
    border-color: rgba(61, 214, 208, 0.3);
  }
  
  .nav-links {
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    height: 100%;
    position: relative;
  }
  
  .nav-link {
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 500;
    border-radius: 50px;
    padding: 0 15px;
    transition: all 0.3s ease;
    z-index: 2;
  }
  
  .link-content {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  
  .icon {
    width: 18px;
    height: 18px;
    transition: transform 0.3s ease;
  }
  
  .home-icon {
    width: 20px;
    height: 20px;
  }
  
  .link-text {
    font-size: 14px;
    transition: all 0.3s ease;
  }
  
  .nav-link:hover {
    color: #fff;
  }
  
  .nav-link:hover .icon {
    transform: translateY(-2px);
  }
  
  .nav-link.active {
    color: #fff;
  }
  
  .nav-link.active .icon {
    filter: drop-shadow(0 0 2px rgba(61, 214, 208, 0.5));
  }
  
  .nav-link.active .link-text {
    background: linear-gradient(to right, #ffffff, #3dd6d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .nav-indicator {
    position: absolute;
    bottom: 5px;
    height: 30px;
    background-color: rgba(61, 214, 208, 0.15);
    border-radius: 50px;
    transition: all 0.3s cubic-bezier(0.65, 0, 0.35, 1);
    z-index: 1;
  }
  
  @media (max-width: 768px) {
    .navigate {
      width: 100%;
      order: 3;
    }
    
    .nav-container {
      width: 100%;
      max-width: 500px;
    }
    
    .link-text {
      font-size: 12px;
    }
    
    .nav-link {
      padding: 0 10px;
    }
    
    .icon {
      width: 16px;
      height: 16px;
    }
    
    .home-icon {
      width: 18px;
      height: 18px;
    }
  }
  
  @media (max-width: 480px) {
    .nav-container {
      height: 36px;
    }
    
    .link-text {
      display: none;
    }
    
    .nav-link {
      padding: 0 12px;
    }
    
    .icon {
      width: 20px;
      height: 20px;
    }
    
    .home-icon {
      width: 22px;
      height: 22px;
    }
  }
</style>