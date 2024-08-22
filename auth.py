import base64
from typing import Dict


def get_auth_headers(username: str, password: str) -> Dict[str, str]:
    """
    返回一个包含认证头信息的字典.

    Args:
        username: 用户名
        password: 密码

    Returns:
        dict: 包含 'Content-Type' 和 'Authorization' 头的字典
    """
    # 将字符串类型转为 bytes二进制类型
    data = f'{username}:{password}'.encode()
    # 将字节编码序列解码为字符串
    decoded_data = base64.b64encode(data).decode()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {decoded_data}'
    }
    return headers
