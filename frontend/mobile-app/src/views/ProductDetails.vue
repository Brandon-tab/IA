<template>
  <div class="product-details">
    <h1>产品详情</h1>
    
    <div class="product-info">
      <div class="form-group">
        <label for="brand">品牌:</label>
        <input id="brand" v-model="product.brand" type="text" />
      </div>
      
      <div class="form-group">
        <label for="name">名称:</label>
        <input id="name" v-model="product.name" type="text" />
      </div>
      
      <div class="form-group">
        <label for="quantity">数量:</label>
        <input id="quantity" v-model="product.quantity" type="number" />
      </div>
      
      <div class="form-group">
        <label for="price">价格:</label>
        <input id="price" v-model="product.price" type="number" step="0.01" />
      </div>
      
      <div class="form-group">
        <label for="barcode">条形码:</label>
        <input id="barcode" disabled v-model="product.barcode" type="text" readonly />
      </div>
      
      <div class="form-group">
        <label>操作类型:</label>
        <div class="radio-group">
          <label>
            <input v-model="operationType" type="radio" value="1" /> 入库
          </label>
          <label>
            <input v-model="operationType" type="radio" value="0" /> 出库
          </label>
        </div>
      </div>
      
      <button @click="saveProduct" class="save-button">保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { showSuccessToast, showFailToast } from 'vant'
import { apiRequest } from '../utils/api'

// 获取路由实例
const route = useRoute()

// 产品数据
const product = ref({
  id: null,
  front_image_path: '',
  back_image_path: '',
  brand: '',
  name: '',
  quantity: 1,
  price: 0.00,
  barcode: ''
})

// 在组件挂载时从查询参数中获取值
onMounted(() => {
  if (route.query.id) product.value.id = route.query.id
  if (route.query.front_image_path) product.value.front_image_path = route.query.front_image_path
  if (route.query.back_image_path) product.value.back_image_path = route.query.back_image_path
  if (route.query.brand) product.value.brand = route.query.brand
  if (route.query.name) product.value.name = route.query.name
  if (route.query.price) product.value.price = route.query.price
  if (route.query.barcode) product.value.barcode = route.query.barcode
})

// 操作类型 (入库/出库)
const operationType = ref('1') // 默认为入库

// 保存产品信息
async function saveProduct() {
  console.log('保存产品信息:', product.value)
  console.log('操作类型:', operationType.value)
  
  // 构造请求参数
  const requestData = {
    front_image_path: product.value.front_image_path,
    back_image_path: product.value.back_image_path,
    brand: product.value.brand,
    name: product.value.name,
    price: product.value.price,
    barcode: product.value.barcode,
    quantity: product.value.quantity,
    operationType: operationType.value
  };
  
  // 发送请求到后端
  try {
    const result = await apiRequest('/update-image', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestData)
    });
    
    console.log('Success:', result);
    showSuccessToast(`产品信息已保存!\n操作类型: ${operationType.value === '1' ? '入库' : '出库'}\n产品: ${product.value.name}`);
  } catch (error) {
    console.error('Error:', error);
    showFailToast('保存失败，请查看控制台错误信息');
  }
}
</script>

<style scoped>
.product-details {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

.product-info {
  background: #f5f5f5;
  padding: 20px;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input[type="text"],
input[type="number"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.radio-group {
  display: flex;
  gap: 15px;
}

.radio-group label {
  font-weight: normal;
  display: flex;
  align-items: center;
  gap: 5px;
}

.save-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 12px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin-top: 10px;
  cursor: pointer;
  border-radius: 4px;
  width: 100%;
}

.save-button:hover {
  background-color: #359c6d;
}
</style>