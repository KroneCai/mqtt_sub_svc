<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import Header from './components/Header.vue'
import SideMenu from './components/SideMenu.vue'
</script>

<template>
  <div class="container">
    <header>
        <Header />
    </header>
    <div class="main-content">
        <nav class="menu" id="mainMenu">
          <SideMenu />
        </nav>
        
        <main class="content">
            <RouterView />
        </main>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* 顶部header样式 */
header {
  width: 100%;
  color: white;
  padding: 0.5rem 0;
  text-align: center;
}

/* 主要内容区域 */
.main-content {
  width: 100%;
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧菜单区域 */
.menu {
  width: 220px;
  background-color: #ecf0f1;
  color: #333333;
  padding: 0 0.5rem;
  overflow-y: auto;
  transition: all 0.3s ease;
}

/* 右侧内容区域 */
.content {
  width: 100%;
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 0.8rem;
  text-align: center;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  .container {
    min-width: 1024px;
  }
}
</style>
