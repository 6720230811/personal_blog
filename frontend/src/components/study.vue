<template>
    <section>
        <div class="title">Education</div>
        <div v-if="!loading && educations.length > 0">
            <div class="posdate" v-for="education in educations" :key="education.id">
                <div>
                    <div class="stitle">{{ education.school_name }}</div>
                    <div class="mar">{{ education.major }} - {{ education.degree }}</div>
                    <div class="date">{{ formatDate(education.start_date) }} - {{ education.end_date ? formatDate(education.end_date) : 'Present' }}</div>
                </div>
            </div>
        </div>
        <div v-else-if="loading" class="loading">
            Loading education history...
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
            educations: [],
            loading: true,
            error: null
        };
    },
    mounted() {
        this.fetchEducation();
    },
    methods: {
        async fetchEducation() {
            try {
                this.loading = true;
                const response = await axios.get('http://localhost:8000/api/education/');
                console.log('教育经历API响应:', response);
                
                if (response.data && response.data.results && response.data.results.length > 0) {
                    this.educations = response.data.results;
                    console.log('成功获取教育经历:', this.educations);
                } else {
                    console.log('API返回空数据，使用默认教育信息');
                    // 如果没有数据，设置默认教育信息
                    this.educations = [
                        { 
                            id: 1, 
                            school_name: 'University of Jakarta', 
                            major: 'Software Engineering',
                            degree: 'Bachelor of Science',
                            start_date: '2018-09-01',
                            end_date: '2022-06-30' 
                        },
                        { 
                            id: 2, 
                            school_name: 'Tech Institute of Design', 
                            major: 'UI/UX Design',
                            degree: 'Certificate',
                            start_date: '2022-08-01',
                            end_date: null 
                        }
                    ];
                }
            } catch (error) {
                console.error('获取教育经历数据失败:', error);
                this.error = '无法连接到API服务器';
                // 出错时设置默认教育信息
                this.educations = [
                    { 
                        id: 1, 
                        school_name: 'University of Jakarta', 
                        major: 'Software Engineering',
                        degree: 'Bachelor of Science',
                        start_date: '2018-09-01',
                        end_date: '2022-06-30' 
                    },
                    { 
                        id: 2, 
                        school_name: 'Tech Institute of Design', 
                        major: 'UI/UX Design',
                        degree: 'Certificate',
                        start_date: '2022-08-01',
                        end_date: null 
                    }
                ];
            } finally {
                this.loading = false;
            }
        },
        formatDate(dateString) {
            if (!dateString) return '';
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
        }
    }
}
</script>

<style scoped>
.title{
    font-size: 48px;
    color: #ffffff;
    margin-bottom: 2rem;
    font-weight: bold;
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

.posdate{
    padding: 1.5rem 2rem;
    margin-bottom: 25px;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    position: relative;
    overflow: hidden;
}

.posdate::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(to bottom, #3dd6d0, #2b8e89);
    opacity: 0.5;
    transition: all 0.3s ease;
}

.posdate:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(61, 214, 208, 0.2);
    background: rgba(0, 0, 0, 0.3);
}

.posdate:hover::before {
    width: 6px;
    opacity: 1;
}

.stitle{
    font-size: 30px;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 12px;
    transition: all 0.3s ease;
}

.posdate:hover .stitle {
    color: #3dd6d0;
    text-shadow: 0 0 5px rgba(61, 214, 208, 0.3);
    transform: translateX(5px);
}

.mar{
    font-size: 20px;
    color: #949494;
    margin-bottom: 10px;
    display: inline-block;
    padding: 4px 12px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    transition: all 0.3s ease;
}

.posdate:hover .mar {
    background: rgba(61, 214, 208, 0.1);
    color: #b9b9b9;
    transform: translateX(5px);
}

.date {
    font-size: 16px;
    color: #747474;
    font-style: italic;
    margin-top: 10px;
    display: flex;
    align-items: center;
    transition: all 0.3s ease;
}

.date::before {
    content: '';
    display: inline-block;
    width: 16px;
    height: 16px;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23747474' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='18' rx='2' ry='2'%3E%3C/rect%3E%3Cline x1='16' y1='2' x2='16' y2='6'%3E%3C/line%3E%3Cline x1='8' y1='2' x2='8' y2='6'%3E%3C/line%3E%3Cline x1='3' y1='10' x2='21' y2='10'%3E%3C/line%3E%3C/svg%3E");
    background-size: contain;
    background-repeat: no-repeat;
    margin-right: 8px;
    transition: all 0.3s ease;
}

.posdate:hover .date {
    color: #a8aaa9;
}

.posdate:hover .date::before {
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%233dd6d0' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Crect x='3' y='4' width='18' height='18' rx='2' ry='2'%3E%3C/rect%3E%3Cline x1='16' y1='2' x2='16' y2='6'%3E%3C/line%3E%3Cline x1='8' y1='2' x2='8' y2='6'%3E%3C/line%3E%3Cline x1='3' y1='10' x2='21' y2='10'%3E%3C/line%3E%3C/svg%3E");
    transform: translateX(2px);
}

.loading {
    font-size: 1rem;
    color: #ccc;
    margin-top: 1rem;
    text-align: center;
    padding: 2rem;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.error {
    font-size: 1rem;
    color: #ff6b6b;
    margin-top: 1rem;
    text-align: center;
    padding: 2rem;
    background: rgba(255, 107, 107, 0.1);
    border-radius: 16px;
    border: 1px solid rgba(255, 107, 107, 0.2);
}
</style>