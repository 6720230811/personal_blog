<template>
    <section>
        <div class="title">Technical Skills</div>
        <div v-if="!loading && skills.length > 0" class="skills-grid">
            <div class="skill-item" v-for="skill in limitedSkills" :key="skill.id">
                <div class="skill-header">
                    <div class="stitle">{{ skill.name }}</div>
                    <div class="skill-value">{{ skill.proficiency * 10 }}%</div>
                </div>
                <div class="mar">{{ skill.category }}</div>
                <div class="skill-bar">
                    <div class="skill-progress" :style="{ width: (skill.proficiency * 10) + '%' }"></div>
                </div>
            </div>
        </div>
        <div v-else-if="loading" class="loading">
            Loading skills...
        </div>
        <div v-else-if="error" class="error">
            {{ error }}
        </div>
    </section>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            skills: [],
            loading: true,
            error: null,
            maxSkills: 6 // 限制显示的技能数量
        };
    },
    computed: {
        limitedSkills() {
            // 只返回指定数量的技能
            return this.skills.slice(0, this.maxSkills);
        }
    },
    mounted() {
        this.fetchSkills();
    },
    methods: {
        async fetchSkills() {
            try {
                this.loading = true;
                const response = await axios.get('http://localhost:8000/api/skills/');
                console.log('技能API响应:', response);
                
                if (response.data && response.data.results && response.data.results.length > 0) {
                    this.skills = response.data.results;
                    console.log('成功获取技能:', this.skills);
                } else {
                    console.log('API返回空数据，使用默认技能');
                    // 如果没有数据，设置默认技能
                    this.skills = [
                        { 
                            id: 1, 
                            name: 'Python', 
                            category: 'Software Engineering', 
                            proficiency: 90 
                        },
                        { 
                            id: 2, 
                            name: 'JavaScript', 
                            category: 'Frontend Development', 
                            proficiency: 85 
                        },
                        { 
                            id: 3, 
                            name: 'Vue.js', 
                            category: 'Frontend Framework', 
                            proficiency: 80 
                        }
                    ];
                }
            } catch (error) {
                console.error('获取技能数据失败:', error);
                this.error = '无法连接到API服务器';
                // 出错时设置默认技能
                this.skills = [
                    { 
                        id: 1, 
                        name: 'Python', 
                        category: 'Software Engineering', 
                        proficiency: 90 
                    },
                    { 
                        id: 2, 
                        name: 'JavaScript', 
                        category: 'Frontend Development', 
                        proficiency: 85 
                    },
                    { 
                        id: 3, 
                        name: 'Vue.js', 
                        category: 'Frontend Framework', 
                        proficiency: 80 
                    }
                ];
            } finally {
                this.loading = false;
            }
        }
    }
}
</script>

<style scoped>
.title{
    font-size: 48px;
    color: #ffffff;
    margin-bottom: 20px;
    font-weight: bold;
}

.skills-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.skill-item {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    padding: 15px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.skill-item:hover {
    transform: translateY(-5px);
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(61, 214, 208, 0.2);
}

.skill-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.skill-value {
    font-size: 16px;
    color: #3dd6d0;
    font-weight: bold;
}

.stitle{
    font-size: 22px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 5px;
    transition: all 0.3s ease;
}

.skill-item:hover .stitle {
    color: #3dd6d0;
    text-shadow: 0 0 5px rgba(61, 214, 208, 0.3);
}

.mar{
    font-size: 16px;
    color: #949494;
    margin-bottom: 10px;
}

.skill-bar {
    width: 100%;
    height: 8px;
    background-color: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 5px;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);
    position: relative;
}

.skill-progress {
    height: 100%;
    background: linear-gradient(to right, #3dd6d0, #2b8e89);
    border-radius: 4px;
    position: relative;
    transition: width 1s cubic-bezier(0.65, 0, 0.35, 1);
    box-shadow: 0 0 10px rgba(61, 214, 208, 0.5);
    animation: pulse 2s infinite;
}

.skill-progress::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(90deg, 
        rgba(255, 255, 255, 0) 0%, 
        rgba(255, 255, 255, 0.2) 50%, 
        rgba(255, 255, 255, 0) 100%);
    animation: shine 2s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 5px rgba(61, 214, 208, 0.5);
    }
    50% {
        box-shadow: 0 0 15px rgba(61, 214, 208, 0.8);
    }
    100% {
        box-shadow: 0 0 5px rgba(61, 214, 208, 0.5);
    }
}

@keyframes shine {
    0% {
        transform: translateX(-100%);
    }
    100% {
        transform: translateX(100%);
    }
}

.loading {
    font-size: 1rem;
    color: #ccc;
    margin-top: 1rem;
}

.error {
    font-size: 1rem;
    color: #ff6b6b;
    margin-top: 1rem;
    text-align: center;
    padding: 1.5rem;
    background: rgba(255, 107, 107, 0.1);
    border-radius: 6px;
    border: 1px solid rgba(255, 107, 107, 0.2);
}

/* 响应式样式 */
@media (max-width: 768px) {
    .skills-grid {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
    
    .stitle {
        font-size: 20px;
    }
    
    .mar {
        font-size: 14px;
    }
}

@media (max-width: 576px) {
    .skills-grid {
        grid-template-columns: 1fr;
    }
}
</style>