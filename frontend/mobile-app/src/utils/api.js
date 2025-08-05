// utils/api.js

/**
 * 根据环境构建API URL
 * @param {string} path - API路径
 * @returns {string} 完整的API URL
 */
export function buildApiUrl(path) {
  const basePath = process.env.NODE_ENV === 'development' ? '/api' : '';
  // 确保路径以 '/' 开头
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  return `${basePath}${normalizedPath}`;
}

/**
 * 发送API请求
 * @param {string} path - API路径
 * @param {Object} options - fetch选项
 * @param {number} timeout - 超时时间（毫秒）
 * @returns {Promise} fetch Promise
 */
export async function apiRequest(path, options = {}, timeout = 30000) {
  const url = buildApiUrl(path);
  
  // 创建一个超时Promise
  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('请求超时')), timeout);
  });
  
  // 使用Promise.race实现超时控制
  return await Promise.race([
    fetch(url, options),
    timeoutPromise
  ]);
}