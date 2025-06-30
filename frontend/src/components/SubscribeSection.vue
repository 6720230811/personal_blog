<template>
    <div class="subscribe-section">
      <div class="inner-div">
        <h1>订阅我的通讯</h1>
        <div class="text-container">
          <p>我会不定期分享关于技术和创意工程的思考与见解，让我们一起探索数字世界的无限可能。</p>
        </div>
        <form @submit.prevent="submitSubscription" class="subscription-form">
          <div class="form-row">
            <input v-model="email" type="email" name="EMAIL" placeholder="您的邮箱地址" required />
            <button type="submit" :disabled="loading">
              {{ loading ? '提交中...' : '订阅' }}
            </button>
          </div>
          <p v-if="message" :class="{ 'success-message': isSuccess, 'error-message': !isSuccess }">
            {{ message }}
          </p>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        email: '',
        loading: false,
        message: '',
        isSuccess: false
      }
    },
    methods: {
      async submitSubscription() {
        if (!this.email) {
          this.message = '请输入邮箱地址';
          this.isSuccess = false;
          return;
        }
        
        try {
          this.loading = true;
          this.message = '';
          
          const response = await axios.post('http://localhost:8000/api/subscribe/', {
            email: this.email,
          });
          
          // 处理成功响应
          this.isSuccess = true;
          if (response.status === 201) {
            this.message = '感谢订阅！请查收确认邮件。';
            this.email = ''; // 清空输入
          } else if (response.status === 200) {
            this.message = response.data.message || '操作成功';
          }
        } catch (error) {
          // 处理错误
          this.isSuccess = false;
          if (error.response && error.response.data) {
            this.message = error.response.data.error || '订阅失败，请稍后再试';
          } else {
            this.message = '网络错误，请检查您的连接';
          }
          console.error('订阅请求失败:', error);
        } finally {
          this.loading = false;
        }
      }
    }
  }
  </script>
  
  <style scoped>
  .subscribe-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
    padding: 6rem 2rem;
    margin-top: 4rem;
    color: #fff;
  }

  .inner-div {
    width: 90%;
    max-width: 1000px;
    display: flex;
    flex-direction: column;
    align-items: center;
    background: linear-gradient(to right, rgba(61, 214, 208, 0.1), rgba(0, 0, 0, 0.3));
    border: 1px solid rgba(61, 214, 208, 0.2);
    border-radius: 2rem;
    padding: 4rem 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  }

  .text-container {
    width: 70%;
    margin-bottom: 2rem;
  }
  
  .subscribe-section h1 {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    background: linear-gradient(to right, #ffffff, #3dd6d0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .subscribe-section p {
    font-size: 1.2rem;
    line-height: 1.6;
    margin-bottom: 1rem;
    color: rgba(255, 255, 255, 0.8);
  }
  
  .subscription-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    max-width: 500px;
  }

  .form-row {
    display: flex;
    width: 100%;
    gap: 1rem;
  }
  
  .subscribe-section input {
    width: 70%;
    padding: 1rem 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background-color: rgba(255, 255, 255, 0.1);
    color: #fff;
    border-radius: 2rem;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .subscribe-section input:focus {
    outline: none;
    border-color: #3dd6d0;
    background-color: rgba(255, 255, 255, 0.15);
    box-shadow: 0 0 10px rgba(61, 214, 208, 0.3);
  }
  
  .subscribe-section button {
    text-align: center;
    width: 30%;
    padding: 1rem 1.5rem;
    background-color: #3dd6d0;
    color: #000;
    border: none;
    border-radius: 2rem;
    cursor: pointer;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
  }
  
  .subscribe-section button:hover {
    background-color: #2bc4be;
    transform: translateY(-3px);
    box-shadow: 0 5px 15px rgba(61, 214, 208, 0.4);
  }
  
  .subscribe-section button:disabled {
    background-color: #75adaa;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
  
  .success-message {
    color: #3dd6d0;
    margin-top: 1rem;
    font-size: 1rem;
  }
  
  .error-message {
    color: #ff6b6b;
    margin-top: 1rem;
    font-size: 1rem;
  }
  
  @media (max-width: 992px) {
    .text-container {
      width: 90%;
    }
  }
  
  @media (max-width: 768px) {
    .subscribe-section {
      padding: 4rem 1rem;
      margin-top: 3rem;
    }
    
    .inner-div {
      width: 100%;
      padding: 3rem 1.5rem;
    }
    
    .subscribe-section h1 {
      font-size: 2rem;
    }
    
    .subscribe-section p {
      font-size: 1.1rem;
    }
  }
  
  @media (max-width: 576px) {
    .form-row {
      flex-direction: column;
      gap: 1rem;
    }
    
    .subscribe-section input,
    .subscribe-section button {
      width: 100%;
    }
    
    .subscribe-section h1 {
      font-size: 1.8rem;
    }
  }
  </style>