import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'


// 导入博客系统的组件
import Home from '../views/Home.vue'
import About from '../views/About.vue'
import Work from '../views/Work.vue'
import Blog from '../views/Blog.vue'
import BlogPostDetail from '../views/BlogPostDetail.vue'
import GitHub from '../views/GitHub.vue'

// 定义路由规则
const routes: Array<RouteRecordRaw> = [
  {
    path: '/',           // 根路径
    name: 'Home',        // 路由名称
    component: Home      // 对应的组件
  },
  {
    path: '/home',       // 明确的home路径
    redirect: '/'        // 重定向到根路径
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/work',
    name: 'Work',
    component: Work
  },
  {
    path: '/blog',
    name: 'Blog',
    component: Blog
  },
  {
    path: '/post/:id',
    name: 'BlogPostDetail',
    component: BlogPostDetail,
    props: true
  },
  {
    path: '/github',
    name: 'GitHub',
    component: GitHub
  },
  // 捕获所有未匹配的路由，重定向到首页
  {
    path: '/:catchAll(.*)',
    redirect: '/'
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),  // 使用HTML5历史模式
  routes                        // 路由配置
})

export default router 
