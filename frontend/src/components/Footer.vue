<template>
  <footer >
    <!-- <div class="footer-content">
      <span>© 2025 / <strong>Selene Yu</strong> / Build your portfolio with <a href="https://onceui.com">Once UI</a></span>
    </div>
    <div class="footer-icons">
      <a href="https://github.com" target="_blank" rel="noopener noreferrer">
        <img src="/icon/github.ico" alt="GitHub" />
      </a>
      <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">
        <img src="/icon/wechat.ico" alt="LinkedIn" />
      </a>
      <a href="mailto:selene@example.com">
        <img src="/icon/email.ico" alt="Email" />
      </a>
    </div> -->
  </footer>
</template>

<style scoped>
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #0b201b;
  color: #fff;
  width: 50vw;
}

.footer-content {
  display: flex;
  align-items: center;
}

.footer-content span {
  font-size: 0.875rem;
}

.footer-content a {
  color: #00ffcc;
  text-decoration: none;
}

.footer-content a:hover {
  text-decoration: underline;
}

.footer-icons {
  display: flex;
  gap: 1rem;
}

.footer-icons img {
  width: 24px;
  height: 24px;
}
</style>
