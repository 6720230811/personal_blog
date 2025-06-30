<script setup lang="ts">
import CurrentTime from './time.vue';
import Navigate from './navigate.vue';
import Address from './address.vue';
</script>
<template>
    <header class="header">
        <div class="header-container">
            <Address/>
            <Navigate/>
            <CurrentTime />
        </div>
    </header>
</template>
<style scoped>
.header {
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    background-color: rgba(0, 0, 0, 0.2);
    position: sticky;
    top: 0;
    z-index: 1000;
    width: 100%;
    box-sizing: border-box;
    border-bottom: 1px solid rgba(61, 214, 208, 0.1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.header:hover {
    border-bottom-color: rgba(61, 214, 208, 0.2);
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.3);
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.8rem 2rem;
    max-width: 1800px;
    margin: 0 auto;
    color: var(--color-text);
    font-size: 15px;
}

@media (max-width: 992px) {
    .header-container {
        padding: 0.8rem 1.5rem;
    }
}

@media (max-width: 768px) {
    .header-container {
        flex-direction: column;
        padding: 0.8rem 1rem;
        gap: 0.8rem;
    }
}

@media (max-width: 576px) {
    .header-container {
        padding: 0.6rem 0.8rem;
    }
}
</style>