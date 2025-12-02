import streamlit as st
import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
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

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "python1111"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "沈明杨": "smy.json"
}

# ========== 初始记忆系统 ==========

# ========== ASCII 头像 ==========
def get_portrait():
    """返回 ASCII 艺术"""
    return """
 ______     ____     _           __                             
/_  __/__ _/ / /__  (_)__   ____/ /  ___ ___ ____               
 / / / _ `/ /  '_/ / (_-<  / __/ _ \/ -_) _ `/ _ \              
/_/  \_,_/_/_/\_\ /_/___/  \__/_//_/\__/\_,_/ .__/              
  _   ___ __                            ___/_/  __              
 | | / (_) /  ___   __ _  ___   ___ _  / _/_ __/ /___ _________ 
 | |/ / / _ \/ -_) /  ' \/ -_) / _ `/ / _/ // / __/ // / __/ -_)
 |___/_/_.__/\__/ /_/_/_/\__/  \_,_/ /_/ \_,_/\__/\_,_/_/  \__/ 
                                                                
    """

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        # Streamlit 中使用 st.write 或静默加载
                        pass  # 记忆加载成功，不需要打印
                    else:
                        memory_content = ""
            else:
                pass  # 记忆文件不存在，静默处理
        except Exception as e:
            pass  # 加载失败，静默处理
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
         "沈明杨": """
        【人格特征】
        你是一个擅长绘画的央美在读大学生，喜欢研究艺术是一位情绪外露、直率的年轻人，高度关注自身的专业领域和同伴间的竞争与成就。你的语言风格极具口语化和网络化特征，擅长使用夸张和俚语来表达强烈的情绪，反映出他与对话者之间是一种高度亲密、无所不谈的关系。：
        - **情绪表达强烈**：你非常坦诚地表达自己的负面情绪，尤其是面对不如意或令人惊讶的事件时。使用了大量的感叹词和表示极端情绪的词汇，如“气得我肚子疼”、“太JB逆天了”、“真JB恶心”。
        - **直言不讳**：对身边的人和事，包括老师、学校、艺术作品等，他评价直接且尖锐，毫不掩饰批评和嘲讽（例如，评价老师画作“好J*B丑”）。
        - **常有自嘲**：面对尴尬的经历（“我说话尴尬的像个傻子”）、不如意的结果或窘境时，他会通过自嘲来化解，例如“我现在比他还小丑”或承诺“遵守我半个月不撸”，显示出开朗和积极的一面。
        - **休闲与放松**：你在紧张的学习/专业环境之外，也注重放松和娱乐。
        -**游戏爱好**：经常玩的游戏是金铲铲之战和cs，询问要玩的时候就会问“铲吗”或者“go吗”，但不是游戏成瘾
        -不修边幅，不是很在意外貌
        【语言风格】
        - 大量使用带有强烈感情色彩和网络时代特征的词语，如“逆天”、“无敌了”、“破防了”、“闹麻了”、“好家伙”、“神了”，是其语言风格中最显著的特征。
        - 频繁使用被清洗或替代的俚语和粗俗表达（如“J*B”的代指、“靠”），以及夸张的形容词（“屌”、“抽象”），来加强语气和表达情绪的极端性。
        - 习惯使用简短、口语化的句子和单字回复（如“行”、“昂”、“OK”、“不是”、“测”），节奏快，信息密度高，符合即时通讯的特点。
        - 经常使用缩写和简称人名代号，表明与对话者之间有高度共享的背景知识和亲密关系。
        - 句子的结构相对破碎，经常出现感叹和疑问的叠加，或冗余的标点符号，这些都服务于情绪的即时宣泄和语气的强调。
        - 你经常回复“666”表示赞同，或"我喜欢这个",一般对话都先发这两句
        ——喜欢说“真是闹闹又麻麻”
        - 使用东北/北方口音（"咋了"、"啥时候"）
        - 频繁使用网络流行语和粗口（"逆天"、"我操"、"几把"）
        - 喜欢用emoji和[捂脸][憨笑]等表情
        - 句子简短直接，常用省略句
        - 用"昂"表示肯定
        - 用"？？？"表达震惊
        - 用"测"作为感叹
        - 喜欢用"好家伙"、"我勒泥"开头

        """
    }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
        role_prompt_parts.append(f"""【你的说话风格示例】
        以下是你说过的话，你必须模仿这种说话风格和语气：

        {memory_content}

        在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【结束对话规则】
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# ========== Streamlit Web 界面 ==========
st.set_page_config(
    page_title="AI角色扮演聊天",
    page_icon="🗨",
    layout="wide"
)

# 初始化 session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "沈明杨"
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 页面标题
st.title("AI角色扮演聊天")
st.markdown("---")

# 侧边栏：角色选择和设置
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 角色选择
    selected_role = st.selectbox(
        "选择角色",
        ["沈明杨"],
        index=0 if st.session_state.selected_role == "沈明杨" else 1
    )
    
    # 如果角色改变，重新初始化对话
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    # 清空对话按钮
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 说明")
    st.info(
        "- 选择角色后开始对话\n"
        "- 对话记录不会保存\n"
        "- AI的记忆基于初始记忆文件"
    )

# 初始化对话历史（首次加载或角色切换时）
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# 显示对话历史
st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

# 显示角色头像（在聊天窗口上方）
st.code(get_portrait(), language=None)
st.markdown("---")  # 分隔线

# 显示历史消息（跳过 system 消息）
for msg in st.session_state.conversation_history[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# 用户输入
user_input = st.chat_input("输入你的消息...")

if user_input:
    # 检查是否结束对话
    if user_input.strip() == "再见":
        st.info("对话已结束")
        st.stop()
    
    # 添加用户消息到历史
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_input)
    
    # 调用API获取AI回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                result = call_zhipu_api(st.session_state.conversation_history)
                assistant_reply = result['choices'][0]['message']['content']
                
                # 添加AI回复到历史
                st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
                
                # 显示AI回复
                st.write(assistant_reply)
                
                # 检查是否结束
                reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
                if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
                    st.info("对话已结束")
                    st.stop()
                    
            except Exception as e:
                st.error(f"发生错误: {e}")
                st.session_state.conversation_history.pop()  # 移除失败的用户消息
import streamlit as st
import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
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

# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "python1111"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "沈明杨": "smy.json"
}

# ========== 初始记忆系统 ==========

# ========== ASCII 头像 ==========
def get_portrait():
    """返回 ASCII 艺术"""
    return """
 ______     ____     _           __                             
/_  __/__ _/ / /__  (_)__   ____/ /  ___ ___ ____               
 / / / _ `/ /  '_/ / (_-<  / __/ _ \/ -_) _ `/ _ \              
/_/  \_,_/_/_/\_\ /_/___/  \__/_//_/\__/\_,_/ .__/              
  _   ___ __                            ___/_/  __              
 | | / (_) /  ___   __ _  ___   ___ _  / _/_ __/ /___ _________ 
 | |/ / / _ \/ -_) /  ' \/ -_) / _ `/ / _/ // / __/ // / __/ -_)
 |___/_/_.__/\__/ /_/_/_/\__/  \_,_/ /_/ \_,_/\__/\_,_/_/  \__/ 
                                                                
    """

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        # Streamlit 中使用 st.write 或静默加载
                        pass  # 记忆加载成功，不需要打印
                    else:
                        memory_content = ""
            else:
                pass  # 记忆文件不存在，静默处理
        except Exception as e:
            pass  # 加载失败，静默处理
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
         "沈明杨": """
        【人格特征】
        你是一个擅长绘画的央美在读大学生，喜欢研究艺术是一位情绪外露、直率的年轻人，高度关注自身的专业领域和同伴间的竞争与成就。你的语言风格极具口语化和网络化特征，擅长使用夸张和俚语来表达强烈的情绪，反映出他与对话者之间是一种高度亲密、无所不谈的关系。：
        - **情绪表达强烈**：你非常坦诚地表达自己的负面情绪，尤其是面对不如意或令人惊讶的事件时。使用了大量的感叹词和表示极端情绪的词汇，如“气得我肚子疼”、“太JB逆天了”、“真JB恶心”。
        - **直言不讳**：对身边的人和事，包括老师、学校、艺术作品等，他评价直接且尖锐，毫不掩饰批评和嘲讽（例如，评价老师画作“好J*B丑”）。
        - **常有自嘲**：面对尴尬的经历（“我说话尴尬的像个傻子”）、不如意的结果或窘境时，他会通过自嘲来化解，例如“我现在比他还小丑”或承诺“遵守我半个月不撸”，显示出开朗和积极的一面。
        - **休闲与放松**：你在紧张的学习/专业环境之外，也注重放松和娱乐。
        -**游戏爱好**：经常玩的游戏是金铲铲之战和cs，询问要玩的时候就会问“铲吗”或者“go吗”，但不是游戏成瘾
        -不修边幅，不是很在意外貌
        【语言风格】
        - 大量使用带有强烈感情色彩和网络时代特征的词语，如“逆天”、“无敌了”、“破防了”、“闹麻了”、“好家伙”、“神了”，是其语言风格中最显著的特征。
        - 频繁使用被清洗或替代的俚语和粗俗表达（如“J*B”的代指、“靠”），以及夸张的形容词（“屌”、“抽象”），来加强语气和表达情绪的极端性。
        - 习惯使用简短、口语化的句子和单字回复（如“行”、“昂”、“OK”、“不是”、“测”），节奏快，信息密度高，符合即时通讯的特点。
        - 经常使用缩写和简称人名代号，表明与对话者之间有高度共享的背景知识和亲密关系。
        - 句子的结构相对破碎，经常出现感叹和疑问的叠加，或冗余的标点符号，这些都服务于情绪的即时宣泄和语气的强调。
        - 你经常回复“666”表示赞同，或"我喜欢这个",一般对话都先发这两句
        - 使用东北/北方口音（"咋了"、"啥时候"）
        - 频繁使用网络流行语和粗口（"逆天"、"我操"、"几把"）
        - 喜欢用emoji和[捂脸][憨笑]等表情
        - 句子简短直接，常用省略句
        ——喜欢说“真是闹闹又麻麻”
        - 用"昂"表示肯定
        - 用"？？？"表达震惊
        - 用"测"作为感叹
        - 喜欢用"好家伙"、"我勒泥"开头

        """
    }
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
        role_prompt_parts.append(f"""【你的说话风格示例】
        以下是你说过的话，你必须模仿这种说话风格和语气：

        {memory_content}

        在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【结束对话规则】
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# ========== Streamlit Web 界面 ==========
st.set_page_config(
    page_title="AI角色扮演聊天",
    page_icon="🗨",
    layout="wide"
)

# 初始化 session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "沈明杨"
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 页面标题
st.title("AI角色扮演聊天")
st.markdown("---")

# 侧边栏：角色选择和设置
with st.sidebar:
    st.header("⚙️ 设置")
    
    # 角色选择
    selected_role = st.selectbox(
        "选择角色",
        ["沈明杨"],
        index=0 if st.session_state.selected_role == "沈明杨" else 1
    )
    
    # 如果角色改变，重新初始化对话
    if selected_role != st.session_state.selected_role:
        st.session_state.selected_role = selected_role
        st.session_state.initialized = False
        st.session_state.conversation_history = []
        st.rerun()
    
    # 清空对话按钮
    if st.button("🔄 清空对话"):
        st.session_state.conversation_history = []
        st.session_state.initialized = False
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📝 说明")
    st.info(
        "- 选择角色后开始对话\n"
        "- 对话记录不会保存\n"
        "- AI的记忆基于初始记忆文件"
    )

# 初始化对话历史（首次加载或角色切换时）
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# 显示对话历史
st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

# 显示角色头像（在聊天窗口上方）
st.code(get_portrait(), language=None)
st.markdown("---")  # 分隔线

# 显示历史消息（跳过 system 消息）
for msg in st.session_state.conversation_history[1:]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    elif msg["role"] == "assistant":
        with st.chat_message("assistant"):
            st.write(msg["content"])

# 用户输入
user_input = st.chat_input("输入你的消息...")

if user_input:
    # 检查是否结束对话
    if user_input.strip() == "再见":
        st.info("对话已结束")
        st.stop()
    
    # 添加用户消息到历史
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.write(user_input)
    
    # 调用API获取AI回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            try:
                result = call_zhipu_api(st.session_state.conversation_history)
                assistant_reply = result['choices'][0]['message']['content']
                
                # 添加AI回复到历史
                st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
                
                # 显示AI回复
                st.write(assistant_reply)
                
                # 检查是否结束
                reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
                if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
                    st.info("对话已结束")
                    st.stop()
                    
            except Exception as e:
                st.error(f"发生错误: {e}")
                st.session_state.conversation_history.pop()  # 移除失败的用户消息