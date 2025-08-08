import axios from 'axios'

// 创建axios实例
const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8001', // API基础URL
  timeout: 120000, // 请求超时时间
  method: 'post', // 默认请求方式为POST
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
http.interceptors.request.use(
  config => {
    // 可以在这里添加认证token等
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
http.interceptors.response.use(
  response => {
    // 可以在这里统一处理响应数据
    return response.data
  },
  error => {
    // 可以在这里统一处理错误
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

export default http