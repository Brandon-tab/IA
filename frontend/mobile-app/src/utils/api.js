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
 * @returns {Promise} fetch Promise
 */
export async function apiRequest(path, options = {}) {
  const url = buildApiUrl(path);
  return await fetch(url, options);
}