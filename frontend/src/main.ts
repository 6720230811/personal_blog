/**
 * Vue应用入口文件
 * 功能：创建Vue实例，加载路由和全局组件
 * 作者：GitHub Sentinel Team
 * 版本：0.0.1
 */

import { createApp } from 'vue'
import axios from 'axios'
import App from './App.vue'
import router from './router'
import './style.css' // 全局CSS

// 配置axios默认值
axios.defaults.baseURL = 'http://localhost:8000'  // 后端API服务器地址
axios.defaults.headers.common['Content-Type'] = 'application/json'

// 创建Vue实例
const app = createApp(App)

// 使用路由
app.use(router)

// 路由准备就绪后挂载应用
router.isReady().then(() => {
  // 挂载应用到DOM
  app.mount('#app')
}) 