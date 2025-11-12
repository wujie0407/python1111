import requests
import json

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "f411addcc1ec4b4587dee19edd59e2f5.qVfd7OBYmRQmUjQz",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 1.0
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 使用示例
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]

result = call_zhipu_api(messages)
print(result['choices'][0]['message']['content'])
