<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import SideMenu from '@/components/SideMenu.vue'

</script>

<template>
  <div class="container">
    <header>
        <Header />
    </header>
    <div class="main-content">
        <nav class="menu" id="sideMenu">
          <SideMenu />
        </nav>
        <main class="content">
          <router-view />
        </main>
    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #ffffff;
  min-width:1024px;
}

/* 顶部header样式 */
header {
  width: 100%;
  color: white;
  padding: 0.5rem 0 0 0;
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
nav {
  width: 220px;
  background-color: transparent;
  color: #333333;
  padding: 1rem 0;
  overflow-y: auto;
  transition: all 0.3s ease;
  font-size: 0.8rem;
  border-right: 2px solid #eeeeee;
}

/* 右侧内容区域 */
.content {
  width: 100%;
  flex: 1;
  padding: 1rem;
  overflow-y: auto;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
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

</style>
