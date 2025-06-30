# personal_blog

这是个人博客的综合平台，提供开源项目追踪和技术内容分享。
|![1](https://github.com/user-attachments/assets/c8c5c838-4fa0-4aed-a9ab-8820704ebfdc)|
![2](https://github.com/user-attachments/assets/c480d499-9eac-4dff-b4d4-b54b6e646dc8)|
![3](https://github.com/user-attachments/assets/f021caee-9f07-4331-b497-177ca3cd7da0)|
![4](https://github.com/user-attachments/assets/670cd472-36f0-405d-b415-10656e22b279)|
![5](https://github.com/user-attachments/assets/0c2bec20-9de9-4b03-b751-1d7ea16277bc)|
<details>
<div style="display: flex; overflow-x: auto; gap: 15px; padding: 15px 0; background: #f5f5f5; border-radius: 8px;">

  <img src="https://github.com/6720230811/personal_blog/blob/main/images/1.png" style="height: 180px; border: 1px solid #ddd;">
  <img src="https://github.com/6720230811/personal_blog/blob/main/images/2.png" style="height: 180px; border: 1px solid #ddd;">
  <img src="https://github.com/6720230811/personal_blog/blob/main/images/3.png" style="height: 180px; border: 1px solid #ddd;">
  <img src="https://github.com/6720230811/personal_blog/blob/main/images/4.png" style="height: 180px; border: 1px solid #ddd;">
  <img src="https://github.com/6720230811/personal_blog/blob/main/images/5.png" style="height: 180px; border: 1px solid #ddd;">
</div>
</details>



## 功能特点

### 博客系统功能

- 📝 技术博客文章发布

- 🎨 个人作品展示平台

- 👤 关于页面介绍

  

### GitHub 功能

- 🔍 获取GitHub上周热门项目
- 📅 每周一早上8点自动推送上周热门项目
- 📧 邮件通知
- 🤖 基于AI的项目分析与问答

## 安装使用

1. 克隆本仓库
2. 安装依赖：

```
npm install
pip install -r requirements.txt
```

3. 创建`.env`文件并配置邮箱信息:

```
EMAIL_USER=your-email@example.com
EMAIL_PASS=your-email-password
TO_EMAIL=recipient@example.com
EMAIL_PROVIDER=gmail
```

## 运行方式

### 前端启动

```
npm run dev
```

### 后端启动

```
python manage.py runserver
```

## 系统架构

- **前端**: Vue.js 3 + Vue Router + Vite
- **后端**: Python + Django + LangChain
- **API**: GitHub API、OpenAI API

## 环境要求

- Node.js 16+
- Python 3.8+
