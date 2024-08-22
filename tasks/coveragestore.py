import json

import requests

from auth import get_auth_headers
from config import GEO_URL, USERNAME, PASSWORD, WORKSPACE, COVERAGE_STORE, TIF_PATH


def create_coverage_store() -> int:
    """
    创建数据存储仓库

    Returns:
        int: HTTP 响应状态码
    """
    url = f'{GEO_URL}/workspaces/{WORKSPACE}/coveragestores'
    headers = get_auth_headers(USERNAME, PASSWORD)
    body = {
        "coverageStore": {
            "name": COVERAGE_STORE,
            "type": "GeoTIFF",
            "enabled": True,
            "url": TIF_PATH,
            "workspace": {
                "name": WORKSPACE
            }
        }
    }
    json_data = json.dumps(body)
    response = requests.post(url, data=json_data, headers=headers)
    print(response.status_code)
    print(response.text)

    return response.status_code


def update_coverage_store(old_coverage_store: str, new_coverage_store) -> int:
    """
    修改原数据存储仓库信息
    Args:
        old_coverage_store: 原数据存储名称
        new_coverage_store: 新的数据存储名称

    Returns: HTTP响应码
    """
    url = f'{GEO_URL}/workspaces/{WORKSPACE}/coveragestores/{old_coverage_store}'
    headers = get_auth_headers(USERNAME, PASSWORD)
    body = {
        "coverageStore": {
            "name": new_coverage_store,
            "type": "GeoTIFF",
            "enabled": True,
            "url": TIF_PATH,
            "workspace": {
                "name": WORKSPACE
            }
        }
    }
    json_data = json.dumps(body)
    response = requests.put(url, data=json_data, headers=headers)
    print(response.status_code)
    print(response.text)

    return response.status_code
