<template>
    <div class="gallery-section">
        <div class="title"><h2>Capture the colorful<br>moments of life</h2></div>
      <div class="gallery">
        <div class="gallery-carousel" @click="nextImage">
          <img v-for="(image, index) in images" :key="index" :src="image" alt="Gallery Image" v-show="currentImageIndex === index" />
        </div>
        <div class="carousel-indicators">
          <div v-for="(image, index) in images" :key="index" :class="{ active: currentImageIndex === index }"></div>
        </div>
        <!-- <div class="project-details">
          <div class="left">
            <h2>Building Once UI, a Customizable Design System</h2>
          </div>
          <div class="right">
            <p>Development of a flexible and highly customizable design system using Next.js for front-end and Figma for design collaboration.</p>
            <a href="work/building-once-ui-a-customizable-design-system">Read case study</a>
          </div>
        </div> -->
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        images: [
          '/public/images/pt4.jpg',
          '/public/images/pt5.jpg',
          '/public/images/pt6.jpg',
        ],
        currentImageIndex: 0
      };
    },
    methods: {
      nextImage() {
        this.currentImageIndex = (this.currentImageIndex + 1) % this.images.length;
      }
    }
  };
  </script>
  
  <style scoped>
  .gallery-section {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-top: 6rem;
    padding: 2rem 0;
    color: #fff;
  }
  .title {
    display: flex;
    justify-content: flex-end; /* 将内容靠右对齐 */
    width: 100%;
  }
 h2 {
    text-align: right;
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 2rem;
    word-wrap: break-word; /* 强制换行 */
    white-space: pre-wrap; /* 保留空白符并换行 */
}
  .gallery {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
  
  .gallery-carousel {
    width: 100%;
    max-width: 1000px;
    height: 500px; /* 固定高度 */
    border-radius: 1rem;
    margin-bottom: 0.5rem;
    position: relative;
    overflow: hidden; /* 确保图片不会超出容器 */
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.3);
  }
  
  .gallery-carousel img {
    width: 100%;
    height: 100%;
    object-fit: cover; /* 确保图片自适应容器大小 */
    border-radius: 1rem;
    position: relative;
    transition: all 0.5s ease;
  }
  
  .gallery-carousel:hover img {
    transform: scale(1.05);
  }
  
  .carousel-indicators {
    display: flex;
    justify-content: center;
    width: 100%;
    max-width: 1000px;
    margin-top: 1rem;
  }
  
  .carousel-indicators div {
    width: 50px;
    height: 5px;
    margin: 0 6px;
    background-color: rgba(255, 255, 255, 0.2);
    cursor: pointer;
    transition: all 0.3s ease;
    border-radius: 3px;
  }
  
  .carousel-indicators div:hover {
    background-color: rgba(255, 255, 255, 0.5);
  }
  
  .carousel-indicators div.active {
    background-color: #3dd6d0;
    width: 60px;
  }
  
  @media (max-width: 1200px) {
    .gallery-carousel {
      height: 450px;
    }
    
    h2 {
      font-size: 2.5rem;
    }
  }
  
  @media (max-width: 992px) {
    .gallery-carousel {
      height: 400px;
    }
  }
  
  @media (max-width: 768px) {
    .gallery-section {
      margin-top: 4rem;
      padding: 1rem 0;
    }
    
    h2 {
      font-size: 2rem;
    }
    
    .gallery-carousel {
      height: 350px;
    }
    
    .carousel-indicators div {
      width: 40px;
    }
  }
  
  @media (max-width: 576px) {
    .gallery-section {
      margin-top: 3rem;
    }
    
    h2 {
      font-size: 1.8rem;
    }
    
    .gallery-carousel {
      height: 250px;
    }
    
    .carousel-indicators div {
      width: 30px;
      height: 4px;
    }
  }
  </style>