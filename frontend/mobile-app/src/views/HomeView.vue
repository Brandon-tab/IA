<template>
  <main class="home">
    <div class="header">
      <h1>拍摄上传</h1>
      <p class="subtitle">请拍摄正面和反面照片</p>
    </div>

    <div class="camera-section">
      <h2>正面照片</h2>
      <input type="file" accept="image/*" capture="environment" @change="handleFrontImage" ref="frontInput" />
      <button class="camera-button" @click="triggerFrontCamera" @touchstart="handleTouchStart" @touchend="handleTouchEnd">📷 拍摄正面照片</button>
      <div class="image-preview" v-if="frontImage">
        <img :src="frontImage" alt="正面照片" />
        <button @click="clearFrontImage" class="clear-button">🗑️ 清除</button>
      </div>
    </div>

    <div class="camera-section">
      <h2>反面照片</h2>
      <input type="file" accept="image/*" capture="environment" @change="handleBackImage" ref="backInput" />
      <button class="camera-button" @click="triggerBackCamera" @touchstart="handleTouchStart" @touchend="handleTouchEnd">📷 拍摄反面照片</button>
      <div class="image-preview" v-if="backImage">
        <img :src="backImage" alt="反面照片" />
        <button @click="clearBackImage" class="clear-button">🗑️ 清除</button>
      </div>
    </div>

    <div class="status-message" v-if="uploadStatus">
      <p>{{ uploadStatus }}</p>
    </div>

    <button class="save-button" @click="saveImages" :disabled="!frontImage || !backImage">
      保存照片
    </button>

    <!-- 调试面板 -->
    <div class="debug-panel" v-if="debugState.show">
      <div class="debug-header">
        <h3>调试信息</h3>
        <button class="close-debug" @click="debugState.show = false">×</button>
      </div>
      <div class="debug-content">
        <div class="debug-item">
          <strong>状态:</strong> {{ debugState.status }}
        </div>
        <div class="debug-item">
          <strong>消息:</strong> {{ debugState.message }}
        </div>
        <div class="debug-item" v-if="debugState.error">
          <strong>错误:</strong> {{ debugState.error }}
        </div>
      </div>
    </div>

  </main>
</template>

<script setup>
import { ref } from 'vue'

// 图片数据
const frontImage = ref('')
const backImage = ref('')

// 上传状态
const uploadStatus = ref('')

// 调试状态
const debugState = ref({
  show: false,
  status: '',
  message: '',
  error: ''
})

// 切换调试面板
function toggleDebugPanel() {
  debugState.value.show = !debugState.value.show
  // 在移动设备上，如果打开调试面板，滚动到顶部
  if (debugState.value.show) {
    setTimeout(() => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }, 100);
  }
}

// 前端输入引用
const frontInput = ref(null)
const backInput = ref(null)

// 触发正面摄像头
function triggerFrontCamera() {
  if (frontInput.value) {
    frontInput.value.click()
  }
}

// 触发反面摄像头
function triggerBackCamera() {
  if (backInput.value) {
    backInput.value.click()
  }
}

// 处理触摸开始事件
function handleTouchStart(event) {
  event.target.classList.add('touch-active')
}

// 处理触摸结束事件
function handleTouchEnd(event) {
  event.target.classList.remove('touch-active')
}

// 处理正面图片
function handleFrontImage(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      frontImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 处理反面图片
function handleBackImage(event) {
  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      backImage.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

// 清除正面图片
function clearFrontImage() {
  frontImage.value = ''
  if (frontInput.value) {
    frontInput.value.value = ''
  }
}

// 清除反面图片
function clearBackImage() {
  backImage.value = ''
  if (backInput.value) {
    backInput.value.value = ''
  }
}

// 保存图片
async function saveImages() {
  if (!frontImage.value || !backImage.value) {
    uploadStatus.value = '请先拍摄正面和反面照片'
    return
  }

  try {
    // 更新调试状态
    debugState.value.status = '上传中'
    debugState.value.message = '正在准备上传...'
    debugState.value.error = ''

    // 创建FormData对象
    const formData = new FormData()
    const frontBlob = await fetch(frontImage.value).then(res => res.blob())
    const backBlob = await fetch(backImage.value).then(res => res.blob())
    
    formData.append('front_image', frontBlob, 'front.jpg')
    formData.append('back_image', backBlob, 'back.jpg')

    // 发送请求
    const response = await fetch('/api/upload-images/', {
      method: 'POST',
      body: formData,
      // 移动端优化：设置超时
      signal: AbortSignal.timeout(30000) // 30秒超时
    })

    const result = await response.json()
    
    if (response.ok) {
      uploadStatus.value = '上传成功!'
      debugState.value.status = '成功'
      debugState.value.message = `图片已保存，ID: ${result.id}`
      
      // 清除图片
      clearFrontImage()
      clearBackImage()
    } else {
      throw new Error(result.error || '上传失败')
    }
  } catch (error) {
    uploadStatus.value = '上传失败，请重试'
    debugState.value.status = '错误'
    debugState.value.message = '上传过程中发生错误'
    debugState.value.error = error.message
    console.error('上传错误:', error)
  }
}
</script>

<style scoped>
.home {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

/* 移动端优化 */
@media (max-width: 768px) {
  .home {
    padding: 15px;
  }
  
  .header h1 {
    font-size: 24px;
  }
  
  .subtitle {
    font-size: 14px;
  }
  
  .camera-section {
    padding: 15px;
  }
  
  .camera-section h2 {
    font-size: 18px;
  }
  
  .camera-button {
    padding: 18px;
    font-size: 18px;
  }
  
  .save-button {
    padding: 18px;
    font-size: 20px;
  }
  
  .debug-panel {
    width: 90%;
    right: 5%;
  }
  
  .debug-toggle {
    padding: 12px 20px;
    font-size: 16px;
  }
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 28px;
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  font-size: 16px;
  color: #666;
}

.camera-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.camera-section h2 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #444;
}

.camera-section input {
  display: none; /* 隐藏默认文件输入 */
}

.camera-button {
  display: block;
  width: 100%;
  padding: 15px;
  background-color: #4285f4;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin: 10px 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.camera-button:hover,
.camera-button.touch-active {
  background-color: #3367d6;
  transform: scale(0.98);
  transition: all 0.1s ease;
}

.image-preview {
  margin-top: 15px;
  text-align: center;
}

.image-preview img {
  max-width: 100%;
  height: auto;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.clear-button {
  margin-top: 10px;
  padding: 10px 20px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
}

.clear-button:hover {
  background-color: #ff2e43;
}

.status-message {
  margin: 20px 0;
  padding: 15px;
  border-radius: 4px;
  text-align: center;
}

.status-message p {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.save-button {
  display: block;
  width: 100%;
  padding: 16px;
  background-color: #42b983;
  color: white;
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover:not(:disabled) {
  background-color: #359c6d;
}

.save-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* 调试面板样式 */
.debug-panel {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 300px;
  background-color: #fff;
  border: 2px solid #42b983;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 1000;
}

.debug-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #42b983;
  color: white;
  border-top-left-radius: 6px;
  border-top-right-radius: 6px;
}

.debug-header h3 {
  margin: 0;
  font-size: 18px;
}

.close-debug {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.debug-content {
  padding: 15px;
}

.debug-item {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.debug-item:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.debug-item strong {
  display: inline-block;
  width: 60px;
  color: #333;
}

/* 调试模式开关按钮 */
.debug-toggle {
  position: fixed;
  bottom: 20px;
  right: 20px;
  padding: 10px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
  cursor: pointer;
  z-index: 999;
}

.debug-toggle:hover {
  background-color: #359c6d;
}
</style>