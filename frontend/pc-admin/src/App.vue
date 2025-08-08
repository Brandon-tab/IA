<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header class="header">
        <h1>智能管理后台管理系统</h1>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <Sidebar />
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  height: 100vh;
}

.header {
  background-color: #409EFF;
  color: white;
  text-align: left;
  line-height: 60px;
  font-size: 24px;
  font-weight: bold;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.el-aside {
  background-color: #f5f5f5;
  border-right: 1px solid #e6e6e6;
}

.el-main {
  background-color: #ffffff;
  padding: 20px;
}
</style>
