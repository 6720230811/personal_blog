<template>
  <!-- 应用根组件 -->
  <div id="app">
    <!-- 头部导航组件 -->
    <Header />
    
    <!-- 主要内容容器 -->
    <main class="main-content">
      <!-- 路由视图容器，用于显示当前路由对应的组件 -->
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>
    
    <!-- 页脚 -->
    <footer class="footer">
      <div class="container">
        <p>&copy; {{ new Date().getFullYear() }} adgo. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script lang="ts">
/**
 * Vue应用根组件
 * 功能：作为整个应用的容器，提供路由视图
 * 作者：GitHub Sentinel Team
 * 版本：0.0.1
 */
import { defineComponent } from 'vue'
import Header from './components/Header.vue'

export default defineComponent({
  name: 'App',
  components: {
    Header
  }
})
</script>

<style>
/* 全局样式已迁移至style.css */
/* 仅保留App组件特有样式 */

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: var(--spacing-md) 0;
  width: 100%;
  max-width: 100%;
  animation: fadeIn 0.5s ease-out;
}

.footer {
  padding: var(--spacing-md) 0;
  background-color: rgba(0, 0, 0, 0.2);
  text-align: center;
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 

