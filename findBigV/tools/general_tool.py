import re

def is_chinese(text):
    """判断字符串是否包含中文"""
    if not text:
        return False
    return bool(re.search(r'[\u4e00-\u9fa5]', text))

def remove_non_chinese_fields(data):
    """
    移除字典中值不是中文的键值对，并递归处理嵌套字典和列表。

    Args:
        data: 要处理的字典或列表。

    Returns:
        处理后的字典或列表。
    """
    if isinstance(data, dict):
        new_dict = {}
        for key, value in data.items():
            if isinstance(value, str):
                if is_chinese(value):
                    new_dict[key] = value
            elif isinstance(value, dict) or isinstance(value, list):
                new_dict[key] = remove_non_chinese_fields(value)
            
        return new_dict
    elif isinstance(data, list):
        new_list = []
        for item in data:
            new_item = remove_non_chinese_fields(item)
            if new_item:
                new_list.append(new_item)
        return new_list
    else:
        return data