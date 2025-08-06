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
export async function apiRequest(path, options = {}, timeout = 1200000) {
  const url = buildApiUrl(path);
  
  // 创建一个超时Promise
  const timeoutPromise = new Promise((_, reject) => {
    setTimeout(() => reject(new Error('请求超时')), timeout);
  });
  
  // 使用Promise.race实现超时控制
  const response = await Promise.race([
    fetch(url, options),
    timeoutPromise
  ]);
  
  // 克隆响应以供后续使用
  const clonedResponse = response.clone();
  
  try {
    // 尝试解析JSON响应
    const data = await response.json();
    
    // 检查响应是否成功
    if (data.code === 200) {
      // 直接返回data字段，而不是创建新的Response对象
      return data.data;
    } else {
      // 如果code不为200，则抛出错误
      throw new Error(data.message || '请求失败');
    }
  } catch (error) {
    // 如果解析JSON失败，则返回原始响应
    if (error instanceof SyntaxError) {
      return clonedResponse;
    }
    // 如果是其他错误，则重新抛出
    throw error;
  }
}