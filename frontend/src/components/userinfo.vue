<template>
   <section>
        <div v-if="owner">
            <div class="name">{{ owner.username }}</div>
            <div class="pos">{{ owner.identity }}</div>
            <p>{{ owner.bio }}</p>
        </div>
        <div v-else class="loading">
            Loading user information...
        </div>
   </section>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            owner: {
                username: '',
                identity: '',
                bio: '',
      },
            loading: true,
            error: null
            };
    },
    mounted() {
        this.fetchOwnerInfo();
    },
    methods: {
        async fetchOwnerInfo() {
            try {
                const response = await axios.get('http://localhost:8000/api/owner/');
                if (response.data && response.data.results && response.data.results.length > 0) {
                    this.owner = response.data.results[0]; // 获取第一个结果
                } else {
                    // 如果没有数据，设置默认值
                    this.owner = {
                        username: 'adgo',
                        identity: 'Design Engineer',
                        bio: 'adgo is a Jakarta-based design engineer with a passion for transforming complex challenges into simple, elegant design solutions. His work spans digital interfaces, interactive experiences, and the convergence of design and technology.'
                    };
                }
            } catch (error) {
                console.error('Failed to fetch owner information:', error);
                // 出错时设置默认值
                this.owner = {
                    username: 'adgo',
                    identity: 'Design Engineer',
                    bio: 'adgo is a Jakarta-based design engineer with a passion for transforming complex challenges into simple, elegant design solutions. His work spans digital interfaces, interactive experiences, and the convergence of design and technology.'
                };
            }
        }
    }
}
</script>

<style scoped>
.name{
    font-weight: bold;
    font-size: 64px;
    color: #ffffff;
    margin-bottom: 0.5rem;
    background: linear-gradient(to right, #ffffff, #3dd6d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 10px rgba(61, 214, 208, 0.3);
    position: relative;
    display: inline-block;
    transition: all 0.3s ease;
}

.name:hover {
    transform: translateY(-3px);
    text-shadow: 0 4px 15px rgba(61, 214, 208, 0.5);
}

.pos{
    font-size: 30px;
    color: #949494;
    margin-bottom: 2rem;
    position: relative;
    display: inline-block;
    padding: 5px 15px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 30px;
    transition: all 0.3s ease;
}

.pos:hover {
    background: rgba(61, 214, 208, 0.1);
    color: #b9b9b9;
    transform: translateX(5px);
}

p {
    text-align: justify;
    font-size: 18px;
    line-height: 1.8;
    color: rgba(255, 255, 255, 0.85);
    background: rgba(0, 0, 0, 0.2);
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

p::before {
    content: '"';
    position: absolute;
    top: 10px;
    left: 15px;
    font-size: 80px;
    color: rgba(61, 214, 208, 0.1);
    font-family: Georgia, serif;
    line-height: 1;
}

p:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
    border-color: rgba(61, 214, 208, 0.2);
    background: rgba(0, 0, 0, 0.3);
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
</style>