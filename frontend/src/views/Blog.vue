<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

interface BlogPost {
  id: number;
  title: string;
  published_at: string;
  cover_image: string | null;
  category: string;
  summary: string;
}

const blogPosts = ref<BlogPost[]>([]);
const loading = ref(true);

async function fetchBlogPosts() {
  try {
    const response = await axios.get('/api/blogs/');
    if (response.data && response.data.results) {
      // 使用DRF分页时的数据结构
      blogPosts.value = response.data.results;
    } else if (Array.isArray(response.data)) {
      // 直接返回数组的情况
      blogPosts.value = response.data;
    }
    loading.value = false;
  } catch (error) {
    console.error('Failed to fetch blog posts:', error);
    // 出错时设置默认博客文章数据
    blogPosts.value = [
      {
        id: 1,
        title: 'Arriving to a new milestone in my career',
        published_at: '2024-04-08T00:00:00Z',
        cover_image: '/images/pt3.jpg',
        category: 'Journal',
        summary: 'Reflections on my career journey and reaching new heights.'
      },
      {
        id: 2,
        title: 'The 99% that remains in the drawer',
        published_at: '2024-03-05T00:00:00Z',
        cover_image: null,
        category: 'Journal',
        summary: 'On design work that never sees the light of day.'
      },
      {
        id: 3,
        title: 'The rise of design engineering',
        published_at: '2024-03-05T00:00:00Z',
        cover_image: null,
        category: 'Technology',
        summary: 'How design engineering is changing the tech landscape.'
      }
    ];
    loading.value = false;
  }
}

function formatDate(dateString: string) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
}

onMounted(() => {
  fetchBlogPosts();
});
</script>
<template>
  <div class="blog-page">
    <div class="container">
      <h1 class="page-title">Writing about design and tech...</h1>
      
      <div v-if="loading" class="loading">
        Loading blog posts...
      </div>
      
      <div v-else class="blog-posts-container">
        <router-link 
          v-for="post in blogPosts" 
          :key="post.id" 
          :to="`/post/${post.id}`" 
          :class="['blog-post', !post.cover_image && 'no-image']"
        >
          <div class="post-image-container" v-if="post.cover_image">
            <img :src="post.cover_image" :alt="post.title" class="post-image" />
          </div>
          <div class="post-details">
            <h2 class="post-title">{{ post.title }}</h2>
            <p class="post-date">{{ formatDate(post.published_at) }}</p>
            <span class="post-tag">{{ post.category }}</span>
          </div>
        </router-link>
        
        <div v-if="blogPosts.length === 0" class="no-posts">
          No blog posts available.
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.blog-page {
  padding: var(--spacing-lg) 0;
}

.page-title {
  font-size: 3.5rem;
  color: #fff;
  margin-bottom: 60px;
  text-align: center;
}

.blog-posts-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.blog-post {
  display: flex;
  padding: var(--spacing-md);
  text-decoration: none;
  cursor: pointer;
  color: inherit;
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.blog-post:hover {
  transform: translate3d(0,-5px,10px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.blog-post.no-image {
  margin-left: 0;
}

.post-image-container {
  width: 40%;
  margin-right: var(--spacing-lg);
  flex-shrink: 0;
}

.post-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  object-fit: cover;
}

.post-details {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.post-title {
  font-size: 1.8rem;
  margin: 0;
  color: #fff;
  margin-bottom: var(--spacing-sm);
}

.post-date {
  color: var(--color-text-muted);
  margin: 0 0 var(--spacing-md) 0;
  font-size: 0.9rem;
  text-align: right;
}

.post-tag {
  background-color: rgba(0, 0, 0, 0.3);
  color: var(--color-text);
  padding: 6px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  width: fit-content;
}

.loading, .no-posts {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--spacing-xl);
  font-size: 1.2rem;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-lg);
  }
  
  .blog-post {
    flex-direction: column;
  }
  
  .post-image-container {
    width: 100%;
    margin-right: 0;
    margin-bottom: var(--spacing-md);
  }
}

@media (max-width: 576px) {
  .page-title {
    font-size: 2rem;
    margin-bottom: var(--spacing-md);
  }
  
  .post-title {
    font-size: 1.5rem;
  }
}
</style>
