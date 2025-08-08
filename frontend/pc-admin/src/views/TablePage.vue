<template>
  <div class="table-page">
    <div class="header">
      <h1>图像数据表</h1>
      <el-button type="primary" @click="exportToExcel" class="export-button">导出Excel</el-button>
    </div>
    <el-table :data="paginatedData" style="width: 100%" stripe>
      <el-table-column prop="id" label="ID" width="80" />
      <el-table-column prop="brand" label="品牌" width="120" />
      <el-table-column prop="name" label="名称" width="150" />
      <el-table-column prop="price" label="价格" width="100" />
      <el-table-column prop="barcode" label="条形码" width="150" />
      <el-table-column prop="number" label="数量" width="100" />
      <el-table-column prop="front_image_path" label="正面图像" width="200" />
      <el-table-column prop="back_image_path" label="背面图像" width="200" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
      <el-table-column prop="updated_at" label="更新时间" width="180" />
    </el-table>
    <el-pagination
  v-model:current-page="currentPage"
  v-model:page-size="pageSize"
  :page-sizes="[10, 20, 50, 100]"
  :small="false"
  :disabled="false"
  :background="true"
  layout="total, sizes, prev, pager, next, jumper"
  :total="totalItems"
  @size-change="handleSizeChange"
  @current-change="handleCurrentChange"
  class="pagination"
/>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import http from '@/utils/http'
import { ElMessage } from 'element-plus'

// 表格数据
const tableData = ref([])

// 分页相关数据
const currentPage = ref(1)
const pageSize = ref(10)
const totalItems = ref(0)
const totalPages = ref(0)

// 获取图像数据
const fetchImageData = async (page = currentPage.value, size = pageSize.value) => {
  try {
    const response = await http('/images/', {
      method: 'POST',
      data: {
        page: page,
        page_size: size
      }
    })
    // 根据后端返回的数据格式处理响应
    if (response.code === 200) {
      // 确保响应数据存在
      const responseData = response.data || {};
      const imageData = responseData.data || [];
      
      // 处理日期字段，确保能正确显示
      const processedData = imageData.map(item => ({
        ...item,
        created_at: item.created_at ? new Date(item.created_at).toLocaleString() : '',
        updated_at: item.updated_at ? new Date(item.updated_at).toLocaleString() : ''
      }));
      tableData.value = processedData;
      
      // 更新分页信息
      if (responseData.pagination) {
        currentPage.value = responseData.pagination.current_page;
        pageSize.value = responseData.pagination.page_size;
        totalItems.value = responseData.pagination.total_items;
        totalPages.value = responseData.pagination.total_pages;
      }
    } else {
      console.error('获取数据失败:', response.message)
    }
  } catch (error) {
    console.error('获取数据时发生错误:', error)
  }
}

// 在组件挂载时获取数据
onMounted(() => {
  fetchImageData()
})

// 计算当前页数据（现在使用后端分页，直接返回所有数据）
const paginatedData = computed(() => {
  return tableData.value
})

// 分页大小改变时的处理函数
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1 // 重置到第一页
  fetchImageData(1, val) // 重新获取数据
}

// 当前页改变时的处理函数
const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchImageData(val, pageSize.value) // 重新获取数据
}

// 导出Excel函数
const exportToExcel = async () => {
  try {
    // 发起导出请求
    const response = await fetch('http://localhost:8001/export-images/', {
      method: 'GET'
    });
    
    if (response.ok) {
      // 获取文件名
      const contentDisposition = response.headers.get('content-disposition');
      let filename = 'images.xlsx';
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename="(.+)"/);
        if (filenameMatch.length === 2) {
          filename = filenameMatch[1];
        }
      }
      
      // 创建下载链接
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
      window.URL.revokeObjectURL(url);
      
      ElMessage.success('导出成功');
    } else {
      ElMessage.error('导出失败');
    }
  } catch (error) {
    console.error('导出时发生错误:', error);
    ElMessage.error('导出时发生错误');
  }
};
</script>

<style scoped>
.table-page {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
}

.export-button {
  margin-left: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}
</style>