<template>
        <section>
            <div class="title">Work Experience</div>
            <div v-if="!loading && workExperiences.length > 0">
                <div v-for="work in workExperiences" :key="work.id" class="work-item">
                    <div class="posdate">
                        <div class="pos">
                            <div class="wtitle">{{ work.project_name }}</div>
                            <div class="wpos">{{ work.position }}</div>
                        </div>
                        <div class="date">{{ formatDate(work.start_date) }} - {{ work.end_date ? formatDate(work.end_date) : 'Present' }}</div>
                    </div>
                    <div class="description" v-if="work.description" v-html="formatDescription(work.description)"></div>
                </div>
            </div>
            <div v-else-if="loading" class="loading">
                Loading work experience...
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
            workExperiences: [],
            loading: true,
            error: null
        };
    },
    mounted() {
        this.fetchWorkExperience();
    },
    methods: {
        async fetchWorkExperience() {
            try {
                this.loading = true;
                const response = await axios.get('http://localhost:8000/api/work-experience/');
                console.log('工作经验API响应:', response);
                
                if (response.data && response.data.results && response.data.results.length > 0) {
                    this.workExperiences = response.data.results;
                    console.log('成功获取工作经验:', this.workExperiences);
                } else {
                    console.log('API返回空数据，使用默认工作经历');
                    // 如果没有数据，设置默认工作经历
                    this.workExperiences = [
                        { 
                            id: 1, 
                            project_name: 'FLY', 
                            position: 'Senior Design Engineer',
                            start_date: '2022-01-01',
                            end_date: null,
                            description: '- Redesigned the UX/UI for the FLY platform, resulting in a 20% increase in user engagement and 30% faster load times.\n- Spearheaded the integration of AI tools into design workflows, enabling designers to iterate 50% faster.'
                        },
                        {
                            id: 2,
                            project_name: 'TechCorp',
                            position: 'UX/UI Designer',
                            start_date: '2019-06-01',
                            end_date: '2021-12-31',
                            description: '- Led design for multiple key projects with high-profile clients.\n- Collaborated with engineering teams to implement responsive designs.'
                        }
                    ];
                }
            } catch (error) {
                console.error('获取工作经验数据失败:', error);
                this.error = '无法连接到API服务器';
                // 出错时设置默认工作经历
                this.workExperiences = [
                    { 
                        id: 1, 
                        project_name: 'FLY', 
                        position: 'Senior Design Engineer',
                        start_date: '2022-01-01',
                        end_date: null,
                        description: '- Redesigned the UX/UI for the FLY platform, resulting in a 20% increase in user engagement and 30% faster load times.\n- Spearheaded the integration of AI tools into design workflows, enabling designers to iterate 50% faster.'
                    },
                    {
                        id: 2,
                        project_name: 'TechCorp',
                        position: 'UX/UI Designer',
                        start_date: '2019-06-01',
                        end_date: '2021-12-31',
                        description: '- Led design for multiple key projects with high-profile clients.\n- Collaborated with engineering teams to implement responsive designs.'
                    }
                ];
            } finally {
                this.loading = false;
            }
        },
        formatDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.getFullYear();
        },
        formatDescription(description) {
            if (!description) return '';
            // 将纯文本描述转换为带HTML的列表
            const items = description.split('\n').filter(item => item.trim());
            if (items.length === 0) return '';
            
            return '<ul>' + 
                items.map(item => `<li>${item.startsWith('-') ? item.substring(1).trim() : item}</li>`).join('') +
                '</ul>';
        }
    }
}
</script>

<style scoped>
.title{
    font-weight: bold;
    font-size: 48px;
    color: #ffffff;
    margin-bottom: 2rem;
    position: relative;
    display: inline-block;
}

.title::after {
    content: '';
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 60px;
    height: 4px;
    background: linear-gradient(to right, #3dd6d0, #2b8e89);
    border-radius: 2px;
}

.work-item {
    margin-bottom: 40px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.work-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(61, 214, 208, 0.2);
    background: rgba(0, 0, 0, 0.3);
}

.posdate{
    display: flex;
    padding-top: 10px;
    margin-bottom: 1rem;
    align-items: center;
}

.pos{
    width: 60%;
    padding-right: 10%;
    text-align: left;
}

.wtitle{
    color: #ffffff;
    margin-bottom: 10px;
    font-weight: bold;
    font-size: 28px;
    transition: all 0.3s ease;
}

.work-item:hover .wtitle {
    color: #3dd6d0;
    text-shadow: 0 0 5px rgba(61, 214, 208, 0.3);
}

.wpos{
    font-size: 18px;
    color: #089f75;
    display: inline-block;
    padding: 4px 12px;
    background: rgba(8, 159, 117, 0.1);
    border-radius: 20px;
    border: 1px solid rgba(8, 159, 117, 0.2);
    transition: all 0.3s ease;
}

.work-item:hover .wpos {
    background: rgba(8, 159, 117, 0.2);
    transform: translateX(5px);
}

.date{
    width: 40%;
    font-size: 18px;
    text-align: right;
    color: #8a8c8b;
    font-style: italic;
    transition: all 0.3s ease;
}

.work-item:hover .date {
    color: #a8aaa9;
}

li {
    color: #ffffff;
    font-size: 18px;
    line-height: 1.6;
    margin-top: 10px;
    text-align: justify;
    transition: all 0.3s ease;
}

.work-item:hover li {
    transform: translateX(3px);
}

li::marker {
    color: #089f75;
}

.loading {
    font-size: 18px;
    color: #ccc;
    margin-top: 1rem;
    text-align: center;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

/* 支持v-html渲染的列表样式 */
:deep(ul) {
    padding-left: 20px;
    margin-top: 10px;
    list-style-type: none;
}

:deep(li) {
    color: #ffffff;
    font-size: 18px;
    line-height: 1.6;
    margin-top: 15px;
    text-align: justify;
    position: relative;
    padding-left: 25px;
    transition: all 0.3s ease;
}

:deep(li)::before {
    content: '';
    position: absolute;
    left: 0;
    top: 10px;
    width: 8px;
    height: 8px;
    background-color: #089f75;
    border-radius: 50%;
    transition: all 0.3s ease;
}

.work-item:hover :deep(li)::before {
    background-color: #3dd6d0;
    transform: scale(1.2);
    box-shadow: 0 0 8px rgba(61, 214, 208, 0.5);
}

.error {
    font-size: 18px;
    color: #ff6b6b;
    margin-top: 1rem;
    text-align: center;
    padding: 2rem;
    background: rgba(255, 107, 107, 0.1);
    border-radius: 16px;
    border: 1px solid rgba(255, 107, 107, 0.2);
}
</style>