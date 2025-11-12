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

