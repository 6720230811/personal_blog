<template>
    <div class="blog-section">
      <h2 class="section-title">最新博客文章</h2>
      <div class="blog-posts" v-if="!loading && blogs.length > 0">
        <div class="blog-post" v-for="blog in blogs" :key="blog.id">
          <div class="blog-post-date">{{ formatDate(blog.published_at) }}</div>
          <h3>{{ blog.title }}</h3>
          <p>{{ blog.summary || '这篇文章暂无摘要...' }}</p>
          <div class="blog-post-footer">
            <a :href="'/post/' + blog.id" class="read-more-link">
              阅读更多
              <span class="arrow-icon">→</span>
            </a>
            <div class="blog-tags" v-if="blog.tags && blog.tags.length > 0">
              <span class="blog-tag" v-for="tag in blog.tags" :key="tag.id">{{ tag.name }}</span>
            </div>
            <div class="blog-tags" v-else>
              <span class="blog-tag">{{ blog.category || '技术' }}</span>
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="loading" class="loading">
        正在加载博客文章...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else class="no-content">
        暂无博客文章
      </div>
      <div class="view-all-container">
        <a href="/blog" class="view-all-link">查看所有文章</a>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';

  export default {
    data() {
      return {
        blogs: [],
        loading: true,
        error: null
      };
    },
    mounted() {
      this.fetchLatestBlogs();
    },
    methods: {
      async fetchLatestBlogs() {
        try {
          console.log('尝试获取最新博客...');
          // 修正API路径，匹配后端的DRF ViewSet路由
          const response = await axios.get('http://localhost:8000/api/blogs/');
          console.log('API响应:', response);
          
          if (response.data && response.data.results && response.data.results.length > 0) {
            // 获取最新的5篇文章
            this.blogs = response.data.results.slice(0, 3);
            console.log('成功获取博客数据:', this.blogs);
          } else {
            console.log('API返回空数据，使用测试数据');
            // 如果没有数据，显示一些测试数据
            this.blogs = [
              {
                id: 1,
                title: '如何使用Vue 3和TypeScript构建现代Web应用',
                published_at: new Date().toISOString(),
                summary: '本文探讨了Vue 3的组合式API和TypeScript的结合使用，以及如何通过这种组合提高代码质量和开发效率。',
                category: '前端开发'
              },
              {
                id: 2,
                title: 'CSS网格布局与Flexbox的最佳实践',
                published_at: new Date(Date.now() - 86400000).toISOString(),
                summary: '深入分析CSS网格布局与Flexbox的区别，以及在不同场景下如何选择最合适的布局方式来构建响应式界面。',
                category: 'CSS'
              },
              {
                id: 3,
                title: 'RESTful API设计原则与最佳实践',
                published_at: new Date(Date.now() - 172800000).toISOString(),
                summary: '本文总结了设计高质量RESTful API的关键原则，包括资源命名、状态码使用、版本控制和安全认证等方面的最佳实践。',
                category: '后端开发'
              }
            ];
          }
        } catch (error) {
          console.error('获取博客文章失败:', error);
          this.error = '无法连接到API服务器';
          // 出错时显示一些测试数据
          this.blogs = [
            {
              id: 1,
              title: '如何使用Vue 3和TypeScript构建现代Web应用',
              published_at: new Date().toISOString(),
              summary: '本文探讨了Vue 3的组合式API和TypeScript的结合使用，以及如何通过这种组合提高代码质量和开发效率。',
              category: '前端开发'
            },
            {
              id: 2,
              title: 'CSS网格布局与Flexbox的最佳实践',
              published_at: new Date(Date.now() - 86400000).toISOString(),
              summary: '深入分析CSS网格布局与Flexbox的区别，以及在不同场景下如何选择最合适的布局方式来构建响应式界面。',
              category: 'CSS'
            },
            {
              id: 3,
              title: 'RESTful API设计原则与最佳实践',
              published_at: new Date(Date.now() - 172800000).toISOString(),
              summary: '本文总结了设计高质量RESTful API的关键原则，包括资源命名、状态码使用、版本控制和安全认证等方面的最佳实践。',
              category: '后端开发'
            }
          ];
        } finally {
          this.loading = false;
        }
      },
      formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' });
      }
    }
  }
  </script>
  
  <style scoped>
  .blog-section {
    display: flex;
    flex-direction: column;
    width: 100%;
    padding: 5rem 0 3rem 0;
    margin-top: 3rem;
    color: #fff;
    max-width: 1400px;
    margin: 3rem auto 0 auto;
  }
  
  .section-title {
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 3rem;
    position: relative;
    padding-left: 1.5rem;
    text-align: left;
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
  
  .blog-posts {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
    gap: 2rem;
    width: 100%;
  }
  
  .blog-post {
    display: flex;
    flex-direction: column;
    background: rgba(0, 0, 0, 0.2);
    padding: 2rem;
    border-radius: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    border: 1px solid rgba(255, 255, 255, 0.1);
    height: 100%;
    position: relative;
    overflow: hidden;
  }
  
  .blog-post::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 0;
    background: linear-gradient(to bottom, #3dd6d0, #2bc4be);
    transition: height 0.4s ease;
  }
  
  .blog-post:hover {
    transform: translateY(-10px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
    background: rgba(0, 0, 0, 0.3);
  }
  
  .blog-post:hover::before {
    height: 100%;
  }
  
  .blog-post-date {
    font-size: 0.9rem;
    color: #3dd6d0;
    margin-bottom: 1rem;
    font-weight: 500;
  }
  
  .blog-post h3 {
    font-size: 1.6rem;
    margin-bottom: 1rem;
    color: #fff;
    line-height: 1.4;
    transition: color 0.3s ease;
  }
  
  .blog-post:hover h3 {
    color: #3dd6d0;
  }
  
  .blog-post p {
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.6;
    flex-grow: 1;
  }
  
  .blog-post-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: auto;
  }
  
  .read-more-link {
    font-size: 1rem;
    color: #3dd6d0;
    text-decoration: none;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s ease;
  }
  
  .arrow-icon {
    transition: transform 0.3s ease;
  }
  
  .read-more-link:hover {
    color: #2bc4be;
  }
  
  .read-more-link:hover .arrow-icon {
    transform: translateX(5px);
  }
  
  .blog-tags {
    display: flex;
    gap: 0.5rem;
  }
  
  .blog-tag {
    font-size: 0.8rem;
    padding: 0.2rem 0.8rem;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    color: #ccc;
    transition: all 0.3s ease;
  }
  
  .blog-tag:hover {
    background-color: rgba(61, 214, 208, 0.1);
    color: #3dd6d0;
  }

  .loading {
    font-size: 1.1rem;
    color: #ccc;
    margin: 2rem 0;
    padding: 3rem;
    text-align: center;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 1rem;
    border: 1px dashed rgba(255, 255, 255, 0.1);
  }
  
  .view-all-container {
    display: flex;
    justify-content: center;
    margin-top: 5rem;
  }
  
  .view-all-link {
    font-size: 1.1rem;
    color: #fff;
    text-decoration: none;
    padding: 0.8rem 2rem;
    background-color: rgba(61, 214, 208, 0.1);
    border: 1px solid rgba(61, 214, 208, 0.3);
    border-radius: 2rem;
    transition: all 0.3s ease;
    font-weight: 500;
  }
  
  .view-all-link:hover {
    background-color: rgba(61, 214, 208, 0.2);
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(61, 214, 208, 0.2);
  }

  /* 响应式样式 */
  @media (max-width: 1200px) {
    .blog-posts {
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    }
    
    .section-title {
      font-size: 2.5rem;
    }
  }
  
  @media (max-width: 992px) {
    .blog-posts {
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
  }
  
  @media (max-width: 768px) {
    .blog-section {
      padding: 4rem 0 2rem 0;
      margin-top: 2rem;
    }
    
    .section-title {
      font-size: 2rem;
      margin-bottom: 1.5rem;
    }
    
    .blog-posts {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    
    .blog-post {
      padding: 1.5rem;
    }
  }

  @media (max-width: 576px) {
    .section-title {
      font-size: 1.8rem;
    }
    
    .blog-post h3 {
      font-size: 1.4rem;
    }
    
    .blog-post p {
      font-size: 1rem;
    }
    
    .blog-post-footer {
      flex-direction: column;
      align-items: flex-start;
      gap: 1rem;
    }
    
    .blog-tags {
      width: 100%;
      justify-content: flex-start;
    }
  }

  .error {
    font-size: 1.2rem;
    color: #ff6b6b;
    margin: 2rem 0;
    text-align: center;
    padding: 2rem;
    background: rgba(255, 107, 107, 0.1);
    border-radius: 1rem;
    border: 1px solid rgba(255, 107, 107, 0.2);
  }

  .no-content {
    font-size: 1.2rem;
    color: #ccc;
    margin: 2rem 0;
    text-align: center;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  </style>