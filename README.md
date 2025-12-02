# Python 基础知识总结

本文档总结了今天学习的两个Python文件（`101.py` 和 `glm.py`）中包含的Python基础知识。

## 文件1: 101.py

### 涉及的知识点

#### 1. **变量赋值**
```python
x = "1"
y = "2"
name = "wujie"
```
- Python使用 `=` 进行变量赋值
- 变量名可以包含字母、数字和下划线
- 变量名区分大小写

#### 2. **字符串类型（String）**
- 字符串用单引号 `'` 或双引号 `"` 包裹
- `"1"` 和 `"2"` 是字符串，不是数字
- 字符串类型在Python中用 `str` 表示

#### 3. **字符串拼接**
```python
print(x + y)  # 输出: "12"
```
- 使用 `+` 运算符可以连接两个字符串
- 注意：字符串拼接和数字相加的区别
  - `"1" + "2"` → `"12"` (字符串拼接)
  - `1 + 2` → `3` (数字相加)

#### 4. **print() 函数**
- `print()` 用于将内容输出到控制台
- 可以输出字符串、数字、变量等多种类型

#### 5. **f-string 格式化字符串**
```python
print(f"Hello{name}")  # 输出: "Hellowujie"
```
- f-string 是Python 3.6+引入的字符串格式化方法
- 在字符串前加 `f` 或 `F` 前缀
- 使用 `{}` 包裹变量或表达式
- 更推荐使用空格：`f"Hello {name}"` → `"Hello wujie"`

---

## 文件2: glm.py

### 涉及的知识点

#### 1. **模块导入（import）**
```python
import requests
import json
```
- `import` 用于导入Python模块或库
- `requests` 是用于发送HTTP请求的第三方库
- `json` 是Python标准库，用于处理JSON数据

#### 2. **函数定义（def）**
```python
def call_zhipu_api(messages, model="glm-4-flash"):
```
- 使用 `def` 关键字定义函数
- 函数名遵循变量命名规范
- **默认参数**：`model="glm-4-flash"` 是默认参数，调用时可以不提供该参数

#### 3. **字典（Dictionary）**
```python
headers = {
    "Authorization": "f411addcc1ec4b4587dee19edd59e2f5.qVfd7OBYmRQmUjQz",
    "Content-Type": "application/json"
}

data = {
    "model": model,
    "messages": messages,
    "temperature": 1.0
}
```
- 字典用花括号 `{}` 定义
- 格式：`{key: value}`
- 键值对之间用逗号分隔
- 字典可以存储不同类型的数据

#### 4. **列表（List）**
```python
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]
```
- 列表用方括号 `[]` 定义
- 列表中可以包含字典、字符串、数字等多种类型
- 列表元素之间用逗号分隔

#### 5. **HTTP请求（requests.post）**
```python
response = requests.post(url, headers=headers, json=data)
```
- `requests.post()` 用于发送POST请求
- 参数说明：
  - `url`: 请求的URL地址
  - `headers`: 请求头（字典格式）
  - `json`: JSON格式的请求体（字典格式）

#### 6. **条件判断（if-else）**
```python
if response.status_code == 200:
    return response.json()
else:
    raise Exception(f"API调用失败: {response.status_code}, {response.text}")
```
- `if` 用于条件判断
- `==` 是比较运算符，判断是否相等
- `else` 处理不满足条件的情况
- `return` 返回函数结果

#### 7. **异常处理（raise Exception）**
```python
raise Exception(f"错误信息")
```
- `raise` 用于抛出异常
- `Exception` 是Python的基础异常类
- 当API调用失败时，抛出异常并显示错误信息

#### 8. **字典访问**
```python
result['choices'][0]['message']['content']
```
- 使用方括号 `[]` 和键名访问字典的值
- 可以嵌套访问多层字典
- `[0]` 表示访问列表的第一个元素（索引从0开始）

#### 9. **方法调用**
- `response.json()`: 将响应内容解析为JSON格式（字典）
- `response.status_code`: 获取HTTP状态码
- `response.text`: 获取响应的文本内容

---

## 📊 glm.py 代码对比分析：昨天 vs 今天

### 版本对比

#### 昨天的版本
```python
data = {
    "model": model,
    "messages": messages,
    "temperature": 1.0  # ← 昨天是 1.0
}

# 使用示例
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}  # ← 硬编码字符串
]
```

#### 今天的版本
```python
data = {
    "model": model,
    "messages": messages,
    "temperature": 0.5  # ← 今天改为 0.5
}

role_system = "你是醉酒大汉,你刚刚喝醉了"  # ← 新增变量

# 使用示例
messages = [
    {"role": "user", "content": f"请介绍一下自己,{role_system}"}  # ← 使用f-string和变量
]
```

### 主要差异分析

#### 差异1：temperature 参数值的变化
- **昨天**：`temperature: 1.0`
- **今天**：`temperature: 0.5`
- **说明**：降低了输出随机性，使AI回答更确定、更保守

#### 差异2：新增 role_system 变量
- **昨天**：无此变量
- **今天**：`role_system = "你是醉酒大汉,你刚刚喝醉了"`
- **说明**：将角色描述提取为独立变量，提高代码可维护性

#### 差异3：messages 中 content 的构建方式
- **昨天**：硬编码字符串 `"你好，请介绍一下自己"`
- **今天**：使用 f-string 动态构建 `f"请介绍一下自己,{role_system}"`
- **说明**：使用 f-string 实现动态字符串拼接

### 这些差异所蕴含的 Python 基础知识

#### 1. **变量提取和代码重构**

**知识点：变量的作用**
```python
# 昨天的写法（硬编码）
content = "你好，请介绍一下自己"

# 今天的写法（使用变量）
role_system = "你是醉酒大汉,你刚刚喝醉了"
content = f"请介绍一下自己,{role_system}"
```

**Python 基础知识：**
- ✅ **代码可维护性**：将重复或可能变化的值提取为变量，便于修改
- ✅ **变量命名**：使用有意义的变量名（`role_system`）提高代码可读性
- ✅ **单一职责**：将系统角色描述单独提取，使代码结构更清晰

#### 2. **f-string 中变量的使用**

**知识点：f-string 变量插值**
```python
# 昨天的写法
{"role": "user", "content": "你好，请介绍一下自己"}

# 今天的写法
role_system = "你是醉酒大汉,你刚刚喝醉了"
{"role": "user", "content": f"请介绍一下自己,{role_system}"}
```

**Python 基础知识：**

##### 2.1 f-string 的基本语法
- f-string 是 Python 3.6+ 引入的字符串格式化方法
- 在字符串前加 `f` 或 `F` 前缀
- 使用 `{}` 包裹变量或表达式

##### 2.2 变量在 f-string 中的使用
```python
name = "Python"
age = 30
message = f"我是{name}，今年{age}岁"  # "我是Python，今年30岁"
```

##### 2.3 在字典中使用 f-string
```python
# 变量可以在字典定义时使用
role_system = "你是醉酒大汉"
content = f"请介绍一下自己,{role_system}"

messages = [
    {"role": "user", "content": content}
]

# 或者直接在字典中写 f-string
messages = [
    {"role": "user", "content": f"请介绍一下自己,{role_system}"}
]
```

#### 3. **参数值的修改**

**知识点：理解参数的作用**
```python
# 昨天
"temperature": 1.0

# 今天
"temperature": 0.5
```

**Python 基础知识：**
- `temperature` 是控制 AI 模型输出随机性的参数
- 值范围通常在 0.0 到 2.0 之间
- **较低的值（如 0.5）**：输出更确定、更保守
- **较高的值（如 1.0）**：输出更随机、更有创造性
- `1.0` 和 `0.5` 都是浮点数（float）类型

#### 4. **代码组织方式的改进**

**昨天的代码结构：**
```python
# 所有内容都写在一起
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]
```

**今天的代码结构：**
```python
# 先定义变量
role_system = "你是醉酒大汉,你刚刚喝醉了"

# 再使用变量构建内容
messages = [
    {"role": "user", "content": f"请介绍一下自己,{role_system}"}
]
```

**Python 基础知识：**
- ✅ **变量先定义后使用**：遵循 Python 的执行顺序
- ✅ **代码分层**：将配置、变量定义、逻辑执行分开
- ✅ **可扩展性**：如果需要修改角色描述，只需修改 `role_system` 变量

### 核心知识点总结

| 知识点 | 说明 | 代码示例 |
|--------|------|----------|
| **变量提取** | 将硬编码值提取为变量，提高可维护性 | `role_system = "..."` |
| **f-string 变量插值** | 在 f-string 中使用 `{}` 插入变量 | `f"文本{变量}"` |
| **字典中的 f-string** | 在字典定义时使用 f-string | `{"key": f"value{var}"}` |
| **参数调优** | 根据需求调整参数值 | `temperature: 0.5` |
| **代码组织** | 先定义变量，再使用变量 | 变量定义 → 使用变量 |

### 代码演进示例

#### 阶段1：硬编码（昨天）
```python
messages = [
    {"role": "user", "content": "你好，请介绍一下自己"}
]
```

#### 阶段2：使用变量（今天）
```python
role_system = "你是醉酒大汉,你刚刚喝醉了"
messages = [
    {"role": "user", "content": f"请介绍一下自己,{role_system}"}
]
```

#### 阶段3：进一步优化（未来可能）
```python
# 可以定义更多变量
greeting = "请介绍一下自己"
role_system = "你是醉酒大汉,你刚刚喝醉了"
content = f"{greeting},{role_system}"

messages = [
    {"role": "user", "content": content}
]
```

---

## 知识点汇总表

| 知识点 | 文件 | 说明 |
|--------|------|------|
| 变量赋值 | 101.py | 使用 `=` 赋值 |
| 字符串类型 | 101.py | 用引号包裹的文本 |
| 字符串拼接 | 101.py | 使用 `+` 连接字符串 |
| print()函数 | 101.py | 输出内容到控制台 |
| f-string | 101.py | 格式化字符串的方法 |
| 模块导入 | glm.py | 使用 `import` 导入库 |
| 函数定义 | glm.py | 使用 `def` 定义函数 |
| 默认参数 | glm.py | 函数参数可以设置默认值 |
| 字典 | glm.py | 键值对数据结构 |
| 列表 | glm.py | 有序的元素集合 |
| HTTP请求 | glm.py | 使用requests库发送请求 |
| 条件判断 | glm.py | 使用if-else进行逻辑判断 |
| 异常处理 | glm.py | 使用raise抛出异常 |
| 字典访问 | glm.py | 使用方括号访问字典值 |

---

## 学习建议

1. **基础语法**：从变量、数据类型、运算符开始
2. **控制流**：掌握if-else、for、while等控制结构
3. **数据结构**：重点学习列表和字典的使用
4. **函数**：理解函数定义、参数传递、返回值
5. **模块**：学会使用标准库和第三方库
6. **实践**：多写代码，通过实际项目巩固知识

---

## 🔄 GitHub 版本管理

本项目使用Git和GitHub进行版本控制，记录学习进度和代码变更。

### Git 基本操作

#### 1. 初始化Git仓库（如果尚未初始化）
```bash
git init
```

#### 2. 配置Git用户信息（首次使用需要）
```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

#### 3. 查看文件状态
```bash
git status
```

#### 4. 添加文件到暂存区
```bash
# 添加所有文件
git add .

# 或添加特定文件
git add README.md
git add 101.py
git add glm.py
```

#### 5. 提交更改
```bash
git commit -m "今日学习内容：Python基础语法和API调用"
```

#### 6. 查看提交历史
```bash
git log
```

### GitHub 远程仓库操作

#### 1. 在GitHub上创建新仓库
- 访问 https://github.com
- 点击右上角 "+" → "New repository"
- 填写仓库名称（如：python-learning）
- 选择Public或Private
- **不要**勾选"Initialize this repository with a README"（因为本地已有文件）
- 点击"Create repository"

#### 2. 连接本地仓库到GitHub
```bash
# 添加远程仓库（将YOUR_USERNAME和REPO_NAME替换为你的信息）
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# 查看远程仓库
git remote -v
```

#### 3. 推送到GitHub
```bash
# 首次推送
git push -u origin main

# 或如果默认分支是master
git push -u origin master

# 之后的推送
git push
```

#### 4. 从GitHub拉取更新
```bash
git pull origin main
```

### 日常工作流程

1. **修改代码** → 编辑文件
2. **查看状态** → `git status`
3. **添加文件** → `git add .`
4. **提交更改** → `git commit -m "描述性信息"`
5. **推送到GitHub** → `git push`

### 提交信息规范

建议使用清晰的提交信息：
- `"添加：今日学习内容总结"`
- `"更新：完善README文档"`
- `"修复：修正字符串拼接示例"`
- `"新增：API调用功能"`

### 版本管理的好处

✅ **备份代码**：代码保存在云端，不会丢失  
✅ **记录历史**：可以查看每次修改的内容  
✅ **协作学习**：可以与同学分享代码  
✅ **学习轨迹**：记录学习进度和成长过程  

---

*最后更新：今天*

glm.py更新日志
变更概览
温度参数调整：data 里的 temperature 由 0.5 提升到 0.8，使模型回复更加发散。见 glm.py 的配置段落。
调用方式由单次请求改成循环对话：原文件只构造一次 messages 并调用 call_zhipu_api，现在改成 while True 输入循环，每次根据用户输入动态重建 messages 并发送请求，实现持续对话。
退出逻辑与角色设定：循环中把 role_system 设为“你是一个江湖剑客”，若用户输入“再见”则触发 if 条件打印“对话结束”并 break。
输出语句改写：旧版本直接 print(result['choices'][0]['message']['content'])，当前版本尝试 print(result)['choices'][0]['message']['content']，这会先打印整个响应对象并返回 None，随后再访问 ['choices'] 会报错，建议恢复旧写法。
安全提示：代码仍然把真实的 API Key 写死在 headers 中，建议改成环境变量或配置文件，避免泄露。

## glm.py vs glm2.py 差异与知识点

### 核心差异
- **角色设定方式**：`glm.py` 在 `messages` 中先写系统设定、再写用户内容；`glm2.py` 增加了更详细的 `role_system` 提示，让模型在对话中遵守“结束对话只回‘江湖再见’”的规则。
- **退出机制**：`glm.py` 通过 `if user_input in ['再见']` 判断用户输入来 `break`；`glm2.py` 则在拿到模型回复后判断 `reply == "江湖再见"` 来退出，实现“由模型决定何时终止”。
- **输出流程**：`glm.py` 的 `print(result)['choices'][0]...` 写法会因为 `print()` 返回 `None` 而报错；`glm2.py` 先把 `reply = result['choices'][0]['message']['content']`，再 `print(reply)`，流程更清晰。
- **循环体验**：两个文件都使用 `while True` 持续对话，但 `glm2.py` 将“终止触发”移到模型回复之后，用户体验更自然。

### Python 基础与新功能的对应关系
| 主题 | glm.py 表现 | glm2.py 改进 | 关联的基础知识 |
| --- | --- | --- | --- |
| 条件判断 | 只判断用户输入 | 先判断用户输入（隐藏意图），再判断模型输出 | `if`/`break`、比较运算符 |
| 字符串处理 | `user_input in ['再见']` | `reply == "江湖再见"`，并用更长的系统提示 | 字符串常量、`==` 比较 |
| 函数重用 | `call_zhipu_api()` | 相同函数，但强调“同一函数服务于多种对话策略” | 函数参数、默认值 |
| 数据结构 | `messages` 是列表 + 字典 | 结构相同，但内容由变量驱动 | 列表、字典、变量插值 |
| 输出流程 | 错误写法导致 `NoneType` 访问 | 先保存再输出，清晰可靠 | 变量赋值、函数返回值 |

### glm3.py vs glm2.py：随机角色选择

#### 代码对比
```python
# glm3.py
import random
current_role = random.choice(list(role_system.keys()))

# glm2.py
role_system = "你是一个江湖剑客..."
```

- glm3.py 通过 `random.choice()` 在启动时从 `role_system` 的键列表中随机抽取身份，确保每轮游戏体验不同。
- glm2.py 将角色设定写成固定字符串，因此每次运行都是同一个身份，方便调试但缺少变化。

#### Python 基础知识总结
- **模块导入**：`import random` 引入标准库 `random`，提供随机数与随机抽取函数。
- **字典视图转列表**：`role_system.keys()` 返回 `dict_keys` 视图，配合 `list(...)` 转成真正的列表后才能作为序列传入 `random.choice`。
- **序列随机抽取**：`random.choice(sequence)` 会从非空序列中等概率返回一个元素，常用于抽签、随机匹配等场景。
- **可扩展性设计**：在 glm3.py 中新增或删除角色只需修改 `role_system` 字典；随机逻辑自动适配，体现“数据驱动行为”的思路。glm2.py 若要换身份必须直接改字符串。
- **确定性 vs 随机性**：glm2.py 的固定角色有利于测试，glm3.py 的随机角色提供更真实的猜身份体验，展示了如何用标准库快速引入“非确定性”行为。

### 学习启示
- **条件分层**：可以先基于输入做一次判断，再用模型输出进行二次判断，体现 if-else 的组合思维。
- **退出控制**：`while True` 必须配合可靠的 `break` 条件；换不同判断点就能得到不同的用户体验。
- **变量中转**：任何要重复使用的内容（如 `reply`）都应先存入变量，避免链式访问导致可读性和调试困难。
- **系统提示工程**：把角色设定写成变量，可以随时替换，练习字符串与变量的组合方式。

Python 基础知识点概括
while 循环：while True 会形成无限循环，只有在循环体内命中 break 才会结束。常用于持续读取输入或轮询。若没有合适的退出条件，程序可能永远不结束。
if 条件判断：if user_input in ['再见'] 用来检查变量是否等于某列表里的任一值；当条件为真执行缩进块，否则跳过。可配合 elif/else 形成多分支。
break 语句：只能在循环中使用；触发后直接跳出最近一层循环。与 while True 搭配是实现“直到满足条件才退出”的常见模式。
输入输出：input() 从标准输入读取字符串；print() 将结果写到控制台。当前代码应把 print(result)['choices'...] 改成先提取内容再打印，例如：
  reply = result['choices'][0]['message']['content']  print(reply)



记忆体聊天记录数据清洗
1处理俚语和非正式表达
2处理缩写和代指，进行匿名化处理
3敏感信息和实体匿名化
4错别字和语病修正
5俚语和敏感词处理：

将具有攻击性的俗语如

将“操”替换为“靠”。

将“nb”替换为“厉害”。

将“der”替换为“傻”



人格提示词：
人格特征：介绍人物现在身份
分析人物性格（对外物分析会讲出来的）
兴趣爱好
语言特征：用ai提取聊天记录习惯话术
在此基础之上进行补充

