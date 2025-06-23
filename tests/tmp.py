import requests
import time
import os
import hashlib
import json
import uuid
from dotenv import load_dotenv
load_dotenv(verbose=True)

from src.proxy import HTTP_CLIENT

# 调用代理，请使用过内部vpn【zjk】或者找 韩广 开放白名单

# gpt-4 api最长支持 8k
# gpt-4t，gpt-4o API最长支持 128k，输出为 4k
# gpt-3.5-turbo 最长支持 16k

host = 'https://gpt-hk.singularity-ai.com'
# host = 'https://gpt-us.singularity-ai.com'  # host 可以选择us的

# 【注】o1目前不支持任何可选参数，temperature，top_p，stream等参数都不能填写，不支持system【role】
# url = host + '/gpt-proxy/azure/gpt-o1/preview'    # o1-preview
# url = host + '/gpt-proxy/azure/gpt-o1/mini'       # o1-mini
# url = host + '/gpt-proxy/azure/gpt4'              # gpt-4
# url = host + '/gpt-proxy/azure/gpt4t'             # gpt-4-turbo
# url = host + '/gpt-proxy/azure/gpt4o'             # gpt-4o (默认版本 2024-08-06）
# url = host + '/gpt-proxy/azure/gpt4o/20240513'    # gpt-4o-2024-05-13
# url = host + '/gpt-proxy/azure/gpt35'             # gpt-3.5
# url = host + '/gpt-proxy/azure/gpt4o/mini'        # gpt-4o-mini
url = host + '/gpt-proxy/azure/chat/completions'    # 指定这个url，必须在body里面填写model参数

proxy_url = os.environ.get('LOCAL_PROXY_BASE', '')

proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

app_key = os.environ.get('SKYWORK_API_KEY', '')
if app_key == '':
    print("not set env var GPTAppKey")
    exit(1)

headers = {
    "app_key": app_key,
    "Content-Type": "application/json"
}

data = {
    "model": "o3",
    "messages": [
        {
            "role": "user",
            "content": "写一个请假申请"
        }
    ],
}

try:
    with HTTP_CLIENT as client:
        response = client.post(url,
                         json=data,
                         headers=headers
                               )
        print(response.json())
except Exception as e:
    print(e)