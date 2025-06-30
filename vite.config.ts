/**
 * Vite构建工具配置文件
 * 功能：配置Vue项目的构建和开发服务器
 * 作者：GitHub Sentinel Team
 * 版本：0.0.1
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // 使用Vue插件
  plugins: [vue()],
  
  // 设置项目根目录为frontend文件夹
  root: 'frontend',
  
  // 构建配置
  build: {
    outDir: '../dist'  // 输出目录设置为上级目录的dist文件夹
  },
  
  // 开发服务器配置
  server: {
    port: 3001,  // 开发服务器端口改为3001
    host: true,  // 允许外部访问
    
    // 代理配置，用于解决跨域问题
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端API服务器地址
        changeOrigin: true               // 修改请求头中的Origin
      }
    }
  }
}) 