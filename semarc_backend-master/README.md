# 配置指南：大模型设置

本项目支持多种大模型的接入和配置，以下是详细的配置说明。

---

## 1. 基础配置

### 1.API Key 配置
在 [`config.py`](config.py ) 文件中，填写对应大模型的 API Key：
```python
API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # OpenAI API Key
DEEPSEEK_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # DeepSeek API Key
```

## 2. 代理配置
如果需要通过访问OpenAI大模型，请启用代理：
```python
USE_PROXY = True
proxies = {
    "http": "http://127.0.0.1:10809",  # 代理地址
    "https": "http://127.0.0.1:10809"
}
```
- 将 USE_PROXY 设置为 True。
- 根据代理软件的设置填写 proxies 的协议、地址和端口。

## 3. 模型选择
在 config.py 中设置默认使用的大模型：
```python
LLM_MODEL = "ollama-deepseek-v2:16b"
```
- 默认模型必须包含在 AVAIL_LLM_MODELS 列表中。
- 根据需求向AVAIL_LLM_MODELS添加支持的模型，并将其设置为 LLM_MODEL。

## 4. 高级配置
### 4.1 设置多线程请求数
设置多线程请求的并发数：
```python
DEFAULT_WORKER_NUM = 32
```
- 在线大模型理论上无并发上限。
- 本地大模型并发上限取决于本地资源。
### 4.2 超时与重试
配置请求超时时间和重试次数：
```python
TIMEOUT_SECONDS = 300  # 超时时间（秒）
MAX_RETRY = 2          # 最大重试次数
```
### 4.3 URL 重定向
如果需要自定义 API URL，可以通过以下方式重定向：
```python
API_URL_REDIRECT = {
    "https://api.openai.com/v1/chat/completions": "https://your-proxy-url/v1/chat/completions"
}
```