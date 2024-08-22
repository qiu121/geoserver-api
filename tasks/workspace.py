import json
import requests
from auth import get_auth_headers
from config import GEO_URL, USERNAME, PASSWORD, WORKSPACE


def create_workspace() -> int:
    """
    创建工作空间.

    Returns:
        int: HTTP 响应状态码.
    """

    url = f'{GEO_URL}/workspaces'
    headers = get_auth_headers(USERNAME, PASSWORD)
    body = {
        'workspace': {
            'name': WORKSPACE
        }
    }
    # 序列化为 JSON格式
    json_data = json.dumps(body)
    params = {'default': 'false'}

    response = requests.post(url, data=json_data, params=params, headers=headers)
    print(response.status_code)
    print(response.text)

    return response.status_code


if __name__ == "__main__":
    create_workspace()
