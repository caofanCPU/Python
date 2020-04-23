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
# 是否开启并发测试
enable_concurrent_test = True
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
    request_headers = request_json['headers']
    cookie = load_cookie(hot_reload)
    request_headers.append('Cookie:' + cookie)
    headers = joiner.join(request_headers)
    body = joiner.join(request_json['body'])
    body = body.replace(id_key, str(id))
    httpie_params = [cmd, no_ca]
    if httpie_view is not None:
        httpie_params.append(httpie_view)
    httpie_params.extend([method, url, headers, body])
    httpie = joiner.join(httpie_params)
    executeStartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    # 延时执行
    # time.sleep(0.05)
    # 使用httpie执行shell, 线程套线程, 效率低下
    # subprocess.call(httpie, shell=True)
    response_body = execute(request_json, cookie, id)
    executeEndTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return "执行命令\n{}\n当前[ID=[{}], executeStartTime=[{}], executeEndTime=[{}]\n响应结果:\n{}".format(httpie, id, executeStartTime, executeEndTime, response_body)


def execute(request_json, cookie, id):
    url = request_json['url']
    method = request_json['method']
    request_headers = {}
    for item in request_json['headers']:
        if item.find('Cookie') != -1:
            continue
        split = item.replace('=', '').split(':')
        request_headers[split[0]] = split[1]
    request_headers['Cookie'] = cookie
    request_body = {}
    for item in request_json['body']:
        split = item.replace(':', '').replace('NONE', str(id)).split('=')
        request_body[split[0]] = split[1]
    try:
        response = requests.request(method, url, headers=request_headers, json=request_body, timeout=3, verify=False)
        # JSON标准格式
        response_body = json.dumps(response.json(), ensure_ascii=False, indent=4)
    except Exception as e:
        response_body = "服务方接口执行失败\n"
        print(response)
        print(e)
    return response_body


def load_cookie(reuse_cookie):
    """
    加载cookie
    :param reuse_cookie: 是否热加载, 复用已有Cookie
    :return:
    """
    if reuse_cookie:
        with open("./cookie.txt", "r") as f:
            cookie = ''.join(f.readlines())
    else:
        cookie = auto_login()
    return cookie


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
    cookie = response_headers.get("set-Cookie")
    with open("./cookie.txt", "w") as f:
        f.write(cookie)
    # JSON标准格式
    response_body = json.dumps(response.json(), ensure_ascii=False, indent=4)
    print("\n执行登录响应BODY结果: \n" + response_body)
    return cookie


def normal():
    ids = load_data()
    for result in executor.map(httpie_cmd, ids):
        print(result)


def concurrent_infinite_loop_test():
    # datas = list(range(1, 20))
    datas = [10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, \
             10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, 10009984, \
            ]

    while True:
        for result in executor.map(httpie_cmd, datas):
            print(result)


def main():
    # 首先登陆一次
    auto_login()
    if enable_concurrent_test:
        concurrent_infinite_loop_test()
    else:
        normal()


if __name__ == '__main__':
    main()
