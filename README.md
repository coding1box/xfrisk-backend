# AI流式输出后端服务

这是一个支持AI流式输出的Flask后端服务，用于处理与DeepSeek API的通信。

## 功能特性

- ✅ 支持普通聊天接口 (`/api/chat`)
- ✅ 支持流式输出接口 (`/api/chat/stream`)
- ✅ 完整的错误处理和日志记录
- ✅ CORS跨域支持
- ✅ 环境变量配置

## 文件结构

```
xf_risk/
├── deepseek_api.py    # 主要的API实现
├── main.py           # 应用入口
├── test_stream.py    # 测试脚本
├── requirements.txt  # 依赖包
└── README.md        # 说明文档
```

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置环境变量

确保设置了 `DEEPSEEK_API_KEY` 环境变量：

```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

### 3. 启动服务

```bash
python main.py
```

服务将在 `http://localhost:8080` 启动。

## API接口

### 1. 普通聊天接口

**URL:** `POST /api/chat`

**请求体:**
```json
{
  "message": "用户消息",
  "history": [
    {"role": "user", "content": "历史消息1"},
    {"role": "assistant", "content": "历史回复1"}
  ]
}
```

**响应:**
```json
{
  "reply": "AI回复内容"
}
```

### 2. 流式输出接口

**URL:** `POST /api/chat/stream`

**请求体:** 与普通接口相同

**响应:** Server-Sent Events (SSE) 格式

```
data: {"content": "部分内容"}
data: {"content": "更多内容"}
data: [DONE]
```

## 测试

运行测试脚本：

```bash
python test_stream.py
```

这将测试普通API和流式API的功能。

## 部署到Render

1. 将代码推送到Git仓库
2. 在Render中创建新的Web Service
3. 连接你的Git仓库
4. 设置环境变量 `DEEPSEEK_API_KEY`
5. 部署

## 前端集成

### 流式输出示例

```javascript
const response = await fetch('https://your-backend.onrender.com/api/chat/stream', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: '用户消息',
    history: []
  })
});

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  
  const chunk = decoder.decode(value);
  const lines = chunk.split('\n');
  
  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const dataStr = line.slice(6);
      if (dataStr.trim() === '[DONE]') break;
      
      try {
        const data = JSON.parse(dataStr);
        if (data.content) {
          // 处理流式内容
          console.log(data.content);
        }
      } catch (e) {
        console.error('解析错误:', e);
      }
    }
  }
}
```

## 错误处理

服务包含完整的错误处理：

- 网络超时
- API密钥错误
- 请求格式错误
- 服务器异常

所有错误都会返回适当的错误消息给前端。

## 注意事项

1. 确保 `DEEPSEEK_API_KEY` 环境变量已正确设置
2. 流式输出需要前端支持 SSE 或 ReadableStream
3. 建议在生产环境中使用 HTTPS
4. 注意API调用频率限制 