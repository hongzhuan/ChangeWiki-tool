// src/services/api.js
import axios from 'axios';

// 配置 Axios 基本信息
axios.defaults.baseURL = '/api';  // 设置 baseURL 为 '/api'

// 封装与后端交互的请求函数
export const executeCommand = async (command) => {
  try {
        const response = await axios.post('', { command });
        return response.data;
    } catch (error) {
        // 可以在这里处理错误
        console.error('执行命令失败:', error);
        throw error; // 抛出错误
    }
};
