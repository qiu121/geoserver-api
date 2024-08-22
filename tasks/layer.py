import json

import requests

from auth import get_auth_headers
from config import GEO_URL, USERNAME, PASSWORD, WORKSPACE, COVERAGE_STORE, LAYER


def create_layer() -> int:
    """
    创建图层.

    Returns:
        int: HTTP 响应状态码
    """
    url = f'{GEO_URL}/workspaces/{WORKSPACE}/coveragestores/{COVERAGE_STORE}/coverages'
    headers = get_auth_headers(USERNAME, PASSWORD)
    body = {
        "coverage": {
            "name": LAYER,
            "title": "a title",
            "keywords": ["GEO TIFF"],
            "abstract": "Description",
            "enabled": True,
            "metadata": {
                "title": "Metadata Title",
                "nativeName": "metadata_native_name"
            }
        }
    }
    json_data = json.dumps(body)
    response = requests.post(url, data=json_data, headers=headers)
    print(response.status_code)
    print(response.text)

    return response.status_code

if __name__ == '__main__':
    create_layer()
