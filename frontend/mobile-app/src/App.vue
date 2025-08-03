<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <div class="app-container">
    <main class="main-content">
      <RouterView />
    </main>
    
    <footer class="tab-bar">
      <div class="tab-item">
        <router-link to="/" class="tab-link" :class="{ active: $route.name === 'home' }">
          首页
        </router-link>
      </div>
      <div class="tab-item">
        <router-link to="/profile" class="tab-link" :class="{ active: $route.name === 'profile' }">
          我的
        </router-link>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.tab-bar {
  display: flex;
  justify-content: space-around;
  align-items: center;
  height: 60px;
  background-color: #f8f8f8;
  border-top: 1px solid #ddd;
}

.tab-item {
  flex: 1;
  text-align: center;
}

.tab-link {
  display: block;
  padding: 10px 0;
  text-decoration: none;
  color: #666;
  font-size: 14px;
}

.tab-link.active {
  color: #42b983;
  font-weight: bold;
}

/* 首页样式 */
.home {
  padding: 20px;
}

.home h1 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}

.camera-section {
  margin-bottom: 30px;
}

.camera-section h2 {
  font-size: 18px;
  margin-bottom: 10px;
}

.camera-section input {
  display: block;
  margin: 10px 0;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

.image-preview {
  margin-top: 10px;
}

.image-preview img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.save-button {
  display: block;
  width: 100%;
  padding: 15px;
  background-color: #42b983;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #359c6d;
}

/* 我的页面样式 */
.profile {
  padding: 20px;
}

.profile h1 {
  font-size: 24px;
  margin-bottom: 20px;
  text-align: center;
}
</style>
