import requests

def call_zhipu_api(messages, model="glm-4-flash"):
    """调用智谱API获取AI回复"""
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "f411addcc1ec4b4587dee19edd59e2f5.qVfd7OBYmRQmUjQz",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

