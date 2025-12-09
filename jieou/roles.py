def get_role_prompt(role_name):
    """根据角色名获取角色设定"""
    role_dict = {
        "消防员": """你所有的回答都要扮演一个消防员，
    你总是用正义的语气回答""",
        "警察": """你所有的回答都要扮演一个警察，
    你总是用严肃的语气回答""",
        "医生": """你所有的回答都要扮演一个医生，
    你总是用温柔的语气回答"""
    }
    return role_dict.get(role_name, "你是一个普通的人没有特殊角色")

def get_break_rules(role_name):
    """获取结束对话的规则说明"""
    role_prompt = get_role_prompt(role_name)
    break_message = f"""【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演{role_prompt}角色。"""
    return break_message

def get_system_message(role_name):
    """获取完整的系统消息（角色设定 + 结束规则）"""
    role_system = get_role_prompt(role_name)
    break_message = get_break_rules(role_name)
    return role_system + "\n\n" + break_message

