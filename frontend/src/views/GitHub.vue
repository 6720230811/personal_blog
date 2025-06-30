<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 定义数据类型
interface Project {
  name: string;
  url: string;
  stars: number;
  description?: string;
}

interface ChatMessage {
  role: 'user' | 'agent';
  content: string;
  id: number;
}

// 响应式数据
const summary = ref('');
const projects = ref<Project[]>([]);
const question = ref('');
const chatHistory = ref<ChatMessage[]>([]);
const weekRange = ref(getLastWeekRange());
const loading = ref(true);
const error = ref('');

// 获取上周日期范围
function getLastWeekRange(): string {
  // 以中国时区为准
  const now = new Date();
  const day = now.getDay() === 0 ? 7 : now.getDay(); // 周日为7
  // 本周一
  const thisMonday = new Date(now.getFullYear(), now.getMonth(), now.getDate() - day + 1);
  // 上周一
  const lastMonday = new Date(thisMonday.getFullYear(), thisMonday.getMonth(), thisMonday.getDate() - 7);
  // 上周日
  const lastSunday = new Date(thisMonday.getFullYear(), thisMonday.getMonth(), thisMonday.getDate() - 1);
  // 格式化
  const fmt = (d: Date): string => `${d.getFullYear()}.${(d.getMonth()+1).toString().padStart(2,'0')}.${d.getDate().toString().padStart(2,'0')}`;
  return `${fmt(lastMonday)} - ${fmt(lastSunday)}`;
}

// 发送问题
function sendQuestion() {
  if (!question.value.trim()) return;
  
  chatHistory.value.push({ 
    role: 'user', 
    content: question.value, 
    id: Date.now() 
  });
  
  axios.post('http://localhost:8000/api/chat/', { 
    question: question.value 
  }).then(res => {
    chatHistory.value.push({ 
      role: 'agent', 
      content: res.data.answer, 
      id: Date.now() + 1 
    });
  }).catch(error => {
    console.error('发送问题失败:', error);
    chatHistory.value.push({ 
      role: 'agent', 
      content: '抱歉，服务器出现错误，请稍后重试。', 
      id: Date.now() + 1 
    });
  });
  
  question.value = '';
}

// 加载数据
onMounted(() => {
  loading.value = true;
    console.log("发起API请求获取项目信息");
    
    // 获取欢迎消息
  axios.get('http://localhost:8000/api/welcome/')
    .then(res => {
      // 添加欢迎消息到聊天历史
      chatHistory.value.push({ 
        role: 'agent', 
        content: res.data.message || '欢迎使用GitHub项目监控系统！有什么可以帮助您的吗？', 
        id: Date.now() 
      });
    })
    .catch(error => {
      console.error('获取欢迎消息失败:', error);
      // 添加默认欢迎消息
      chatHistory.value.push({ 
        role: 'agent', 
        content: '欢迎使用GitHub项目监控系统！有什么可以帮助您的吗？', 
        id: Date.now() 
      });
    });
    
    // 获取项目列表
  axios.get('http://localhost:8000/api/top10/')
    .then(res => {
      console.log("API请求成功，数据:", res.data);
      projects.value = res.data.projects || [];
      console.log("设置projects完成，长度:", projects.value.length);
      
      // 如果没有项目数据，使用测试数据
      if (projects.value.length === 0) {
        projects.value = getTestData();
      }
    })
    .catch(error => {
      console.error('获取项目信息失败:', error);
      error.value = `错误: ${error.message || '未知错误'}`;
      // 使用测试数据
      projects.value = getTestData();
    })
    .finally(() => {
      loading.value = false;
    });
});

// 测试数据
function getTestData(): Project[] {
  return [
    {
      name: "microsoft/semantic-kernel",
      url: "https://github.com/microsoft/semantic-kernel",
      stars: 15200,
      description: "微软的语义内核框架，用于集成LLM到应用程序中"
    },
  ];
}
</script>

<template>
  <div class="github-container">
    <!-- 左侧：项目详情 -->
    <div class="left-panel">
      <h2>上周GitHub热门新项目</h2>
      <div class="summary-card">
        {{weekRange}} GitHub热门新项目Top10
      </div>
      
      <!-- 项目列表 -->
      <div class="main-content">
        <h3>详细项目列表</h3>
        
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          <p>正在加载项目数据...</p>
        </div>
        
        <div class="project-list" v-else-if="projects.length > 0">
   <div class="project-card" v-for="(repo, idx) in projects" :key="repo.url">
            <div class="project-header">
      <span class="project-index">{{ idx + 1 }}.</span>
      <a :href="repo.url" class="project-name" target="_blank">{{ repo.name }}</a>
      <span class="project-stars">⭐{{ repo.stars }}</span>
    </div>
    <div class="project-desc">
      简介: {{ repo.description || '暂无简介' }}
    </div>
  </div>
</div>

        <div v-else class="no-data">
        暂无项目数据
      </div>
    </div>
    </div>
    
    <!-- 右侧：与Agent对话 -->
    <div class="right-panel">
      <h3>与Agent对话</h3>
      <div class="chat-history">
        <div v-for="msg in chatHistory" :key="msg.id" :class="['chat-bubble', msg.role === 'user' ? 'right' : 'left']">
          <div class="bubble-content">
            <b v-if="msg.role==='user'">你：</b>
            <b v-else>机器人：</b>
            <span>{{ msg.content }}</span>
          </div>
        </div>
      </div>
      <div class="chat-input-row">
        <input 
          v-model="question" 
          @keyup.enter="sendQuestion" 
          placeholder="请输入你的问题..." 
        />
        <button @click="sendQuestion">
          <span class="send-btn-text">发送</span>
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.github-container {
  display: flex;
  flex-direction: row;
  gap: 32px;
  max-width: 1600px;
  margin: 0 auto;
  padding: 30px 10px 40px 10px;
}

.main-content {
  width: 100%;
  margin: 0 auto;
  visibility: visible;
}

.left-panel {
  flex: 2.6;
  min-width: 0;
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  color: #fff;
  position: relative;
}

.right-panel {
  flex: 1.2;
  min-width: 0;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 24px 18px 18px 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
  height: fit-content;
  color: #fff;
}

h2, h3 {
  color: #fff;
  margin-bottom: 20px;
  text-align: center;
}

.summary-card {
  background-color: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  white-space: pre-wrap;
  word-wrap: break-word;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 30px;
  font-size: 1.08em;
  color: #fff;
  text-align: center;
  padding: 25px 15px;
}

.project-list {
  margin: 30px auto;
  max-width: 800px;
}

.project-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  margin-bottom: 18px;
  padding: 18px 22px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.03);
  transition: all 0.3s ease;
  color: #fff;
  position: relative;
}

.project-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
  transform: translateX(10px);
  background: rgba(255, 255, 255, 0.1);
}

.project-header {
  display: flex;
  align-items: center;
  font-size: 1.1em;
  margin-bottom: 8px;
}

.project-index {
  font-weight: bold;
  color: #fff;
  margin-right: 8px;
}

.project-name {
  font-weight: bold;
  color: #3dd6d0;
  text-decoration: none;
  margin-right: 12px;
  transition: color 0.2s ease;
}

.project-name:hover {
  text-decoration: underline;
  color: #2bc4be;
}

.project-stars {
  color: #fff;
  font-weight: bold;
  margin-left: auto;
}

.project-desc {
  color: #ccc;
  font-size: 0.98em;
  margin-left: 24px;
}

/* 聊天气泡左右分布 */
.chat-history {
  margin: 30px 0 10px 0;
  min-height: 120px;
  max-height: 600px;
  overflow-y: auto;
  padding-right: 6px;
  color: #fff;
}

.chat-bubble {
  display: flex;
  margin: 10px 0;
}

.chat-bubble.left {
  justify-content: flex-start;
}

.chat-bubble.right {
  justify-content: flex-end;
}

.bubble-content {
  max-width: 80%;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 12px 18px;
  font-size: 1em;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  word-break: break-word;
  color: #fff;
}

.chat-bubble.right .bubble-content {
  background: rgba(61, 214, 208, 0.1);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.chat-bubble.left .bubble-content {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  border-bottom-left-radius: 4px;
}

.chat-input-row {
  display: flex;
  align-items: stretch;
  margin-top: 30px;
}

input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  margin-right: 10px;
  font-size: 1em;
  height: 48px;
  box-sizing: border-box;
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
}

input:focus {
  outline: none;
  border-color: #3dd6d0;
  box-shadow: 0 0 0 2px rgba(61, 214, 208, 0.2);
}

button {
  padding: 0 20px;
  background: linear-gradient(90deg, #3dd6d0 0%, #2bc4be 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  font-weight: bold;
  box-shadow: 0 2px 8px rgba(61, 214, 208, 0.2);
  transition: all 0.2s ease;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

button:hover {
  background: linear-gradient(90deg, #2bc4be 0%, #3dd6d0 100%);
  box-shadow: 0 4px 16px rgba(61, 214, 208, 0.3);
  transform: translateY(-2px);
}

.send-btn-text {
  display: inline-block;
  text-align: center;
  font-size: 1em;
  font-weight: bold;
}

.loading-state {
  display: flex;
    flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  }

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #3dd6d0;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.no-data {
  text-align: center;
  padding: 30px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px dashed rgba(255, 255, 255, 0.2);
  color: #ccc;
  border-radius: 8px;
}

@media (max-width: 1200px) {
  .github-container {
    padding: 20px 10px;
  }
}

@media (max-width: 900px) {
  .github-container {
    flex-direction: column;
    gap: 20px;
  }
  
  .left-panel, .right-panel {
    width: 100%;
  }
  
  .right-panel {
    margin-top: 20px;
  }
  
  .project-card {
    padding: 15px;
  }
  
  .bubble-content {
    max-width: 90%;
  }
}

@media (max-width: 576px) {
  .github-container {
    padding: 10px;
  }
  
  .left-panel, .right-panel {
    padding: 15px;
  }
  
  h2 {
    font-size: 1.5rem;
  }
  
  h3 {
    font-size: 1.3rem;
  }
  
  .project-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .project-stars {
    margin-left: 0;
    margin-top: 5px;
  }
  
  .project-desc {
    margin-left: 0;
  }
  
  .chat-input-row {
    flex-direction: column;
    gap: 10px;
  }
  
  input, button {
    width: 100%;
    margin: 0;
  }
}
</style>