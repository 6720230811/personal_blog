<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { marked } from 'marked';
import '../assets/markdown.css';

// 声明博客文章的数据结构
interface BlogPost {
  id: number;
  title: string;
  content: string;
  published_at: string;
  cover_image: string | null;
  category: string;
  views_count: number;
  tags?: any[];
}

const route = useRoute();
const postId = computed(() => route.params.id);
const post = ref<BlogPost | null>(null);
const loading = ref(true);
const error = ref('');

// 格式化日期的函数
function formatDate(dateString: string) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
}

// 将Markdown转换为HTML的函数
function renderMarkdown(text: string) {
  if (!text) return '';
  return marked(text);
}

// 获取博客文章详情
async function fetchBlogPost() {
  if (!postId.value) {
    error.value = 'Invalid post ID';
    loading.value = false;
    return;
  }

  try {
    const response = await axios.get(`/api/blogs/${postId.value}/`);
    post.value = response.data;
    loading.value = false;
  } catch (err) {
    console.error('Error fetching blog post:', err);
    error.value = 'Failed to load the blog post. Please try again later.';
    loading.value = false;
  }
}

onMounted(() => {
  fetchBlogPost();
});
</script>

<template>
  <div class="blog-post-page">
    <div class="container-narrow">
      <div v-if="loading" class="loading">
        Loading article...
      </div>
      
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      
      <article v-else-if="post" class="post-container">
        <header class="post-header">
          <h1 class="post-title">{{ post.title }}</h1>
          <div class="post-meta">
            <span class="post-date">{{ formatDate(post.published_at) }}</span>
            <span class="post-category">{{ post.category }}</span>
          </div>
          
          <div v-if="post.cover_image" class="post-cover">
            <img :src="post.cover_image" :alt="post.title" />
          </div>
        </header>
        
        <div class="post-content markdown-content" v-html="renderMarkdown(post.content)"></div>
        
        <footer class="post-footer">
          <div v-if="post.tags && post.tags.length > 0" class="post-tags">
            <span class="tag-label">Tags:</span>
            <span v-for="tag in post.tags" :key="tag.id" class="tag">
              {{ tag.name }}
            </span>
          </div>
          
          <div class="post-views">
            <span>Views: {{ post.views_count }}</span>
          </div>
        </footer>
      </article>
      
      <div v-else class="not-found">
        Blog post not found.
      </div>
    </div>
  </div>
</template>

<style scoped>
.blog-post-page {
  padding: var(--spacing-lg) 0;
}

.loading, .error, .not-found {
  text-align: center;
  padding: var(--spacing-xl);
  font-size: 1.2rem;
  color: var(--color-text-muted);
}

.error {
  color: #ff6b6b;
}

.post-container {
  animation: fadeIn 0.5s ease-out;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: var(--spacing-lg);
}

.post-header {
  margin-bottom: var(--spacing-lg);
}

.post-title {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
  line-height: 1.2;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  color: var(--color-text-muted);
  font-size: 1rem;
  margin-bottom: var(--spacing-lg);
}

.post-category {
  background-color: rgba(0, 0, 0, 0.3);
  color: var(--color-text);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.post-cover {
  margin: var(--spacing-lg) 0;
  border-radius: 8px;
  overflow: hidden;
}

.post-cover img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.post-content {
  font-size: 1.1rem;
  line-height: 1.8;
}

.post-footer {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.post-tags {
  margin-bottom: var(--spacing-md);
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  align-items: center;
}

.tag-label {
  color: var(--color-text-muted);
}

.tag {
  background-color: rgba(0, 0, 0, 0.3);
  color: var(--color-text);
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
}

.post-views {
  margin-top: var(--spacing-md);
  color: var(--color-text-muted);
  font-size: 0.9rem;
  text-align: right;
}

@media (max-width: 768px) {
  .post-title {
    font-size: 2.2rem;
  }
  
  .post-content {
    font-size: 1rem;
  }
}

@media (max-width: 576px) {
  .post-container {
    padding: var(--spacing-md);
  }
  
  .post-title {
    font-size: 1.8rem;
  }
}

/* 使详情页整体左对齐，覆盖 #app 默认的 text-align:center */
.post-container,
.post-header,
.post-title,
.post-content {
  text-align: left;
}
</style> 