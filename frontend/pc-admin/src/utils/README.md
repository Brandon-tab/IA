# HTTP Client 封装说明

## 简介
本项目对axios进行了封装，默认使用POST请求方式，统一处理请求和响应拦截器。

## 使用方法

```javascript
import http from './http'

// 发送POST请求
http('/api/users', { name: 'John' })
  .then(response => {
    console.log(response)
  })
  .catch(error => {
    console.error(error)
  })

// 发送GET请求（需要手动指定method）
http({
  url: '/api/users',
  method: 'get'
})
  .then(response => {
    console.log(response)
  })
  .catch(error => {
    console.error(error)
  })
```

## 配置

- baseURL: 默认为 `http://localhost:8000`，可通过环境变量 `VITE_API_BASE_URL` 进行配置
- timeout: 默认为 `10000ms`
- method: 默认为 `post`
- headers: 默认包含 `'Content-Type': 'application/json'`

## 拦截器

### 请求拦截器
- 可用于添加认证token等统一处理

### 响应拦截器
- 统一处理响应数据，直接返回response.data
- 统一处理错误信息