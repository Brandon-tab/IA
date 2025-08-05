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
            <input v-model="operationType" type="radio" value="in" /> 入库
          </label>
          <label>
            <input v-model="operationType" type="radio" value="out" /> 出库
          </label>
        </div>
      </div>
      
      <button @click="saveProduct" class="save-button">保存</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 产品数据
const product = ref({
  brand: '',
  name: '',
  quantity: 0,
  price: 0.00,
  barcode: '1234567890123' // 示例条形码
})

// 操作类型 (入库/出库)
const operationType = ref('in') // 默认为入库

// 保存产品信息
function saveProduct() {
  console.log('保存产品信息:', product.value)
  console.log('操作类型:', operationType.value)
  // 这里可以添加保存到服务器的逻辑
  alert(`产品信息已保存!\n操作类型: ${operationType.value === 'in' ? '入库' : '出库'}\n产品: ${product.value.name}`)
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