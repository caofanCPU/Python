#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import ssl
import subprocess
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd
import requests

# 屏蔽HTTPS证书校验, 忽略安全警告
requests.packages.urllib3.disable_warnings()
context = ssl._create_unverified_context()
joiner = ' '
id_key = 'NONE'
# 登陆一次后是否服复用cookie
hot_reload = True
cmd = "http"
no_ca = "--verify=no"
httpie_allow_view = {"-v": "显示请求详细信息", "-h": "显示请求头", "-b": "显示请求Body", "-d": "响应结果保存至TXT", "": "默认"}
httpie_view = None
# 并发数
max_concurrent = 64
concurrent = 1
try:
    if len(sys.argv) > 1:
        if httpie_allow_view.get(sys.argv[1]) is not None:
            httpie_view = sys.argv[1]
        else:
            print("输入参数有误, 仅支持如下参数: -v显示请求详细信息|-h显示请求头|-b显示请求Body|-d响应结果保存至TXT")
    if len(sys.argv) > 2:
        try:
            input_concurrent = int(sys.argv[2])
            if input_concurrent > 1:
                concurrent = min(input_concurrent, max_concurrent)
        except Exception as e:
            print("并发数设置范围[1, {}], 默认1".format(max_concurrent))
            print(e)
except Exception as e:
    print(e)
executor = ThreadPoolExecutor(max_workers=concurrent)


def httpie_cmd(id):
    """
    执行excuteUrl.json接口
    :param id
    :return:
    """
    with open("./excuteUrl.json", 'r') as request_data:
        request_json = json.load(request_data)
    url = request_json['url']
    method = request_json['method']
    request_headers = load_request_headers(request_json['headers'], hot_reload)
    headers = joiner.join(request_headers)
    body = joiner.join(request_json['body'])
    body = body.replace(id_key, str(id))
    httpie_params = [cmd, no_ca]
    if httpie_view is not None:
        httpie_params.append(httpie_view)
    httpie_params.extend([method, url, headers, body])
    httpie = joiner.join(httpie_params)
    # print(httpie)
    executeStartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # 延时执行
    # time.sleep(0.05)
    subprocess.call(httpie, shell=True)
    executeEndTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return "当前[ID={}, [executeStartTime={}], [executeEndTime={}]".format(id, executeStartTime, executeEndTime)


def load_request_headers(headers, hot_reload):
    """
    加载请求header
    :param headers:
    :param hot_reload: 是否热加载, 复用已有Cookie
    :return:
    """
    if hot_reload:
        with open("./cookie.txt", "r") as f:
            cookie = ''.join(f.readlines())
    else:
        cookie = auto_login()
    headers.append(cookie)
    return headers


def load_data():
    """
    读取数据文件, 每行为一条数据
    :return:
    """
    data = pd.read_csv("./ID.csv", header=-1)
    data.columns = ['id']
    return data['id']


def auto_login():
    """
    自动登录, 获取登录Cookie, 写入文件, 在控制台打印
    """
    with open("./ssoLogin.json", 'r') as sso_login_request_data:
        request_json = json.load(sso_login_request_data)
    url = request_json['url']
    method = request_json['method']
    request_headers = {}
    for item in request_json['headers']:
        split = item.replace('=', '').split(':')
        request_headers[split[0]] = split[1]
    request_body = {}
    for item in request_json['body']:
        split = item.replace(':', '').split('=')
        request_body[split[0]] = split[1]

    request_headers = {"Content-Type": "application/json", "HT-app": "6"}
    response = requests.request(method, url, headers=request_headers, json=request_body, timeout=3, verify=False)
    response_headers = response.headers
    cookie = "'Cookie:" + response_headers.get("set-Cookie") + "'"
    with open("./cookie.txt", "w") as f:
        f.write(cookie)
    # JSON标准格式
    response_body = json.dumps(response.json(), ensure_ascii=False, indent=4)
    print("\n执行登录响应BODY结果: \n" + response_body)
    return cookie


def main():
    # 首先登陆一次
    auto_login()
    ids = load_data()
    for result in executor.map(httpie_cmd, ids):
        print(result)


if __name__ == '__main__':
    main()
