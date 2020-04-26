#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import ssl
import sys
from concurrent.futures.thread import ThreadPoolExecutor

import requests

# 屏蔽HTTPS证书校验, 忽略安全警告
requests.packages.urllib3.disable_warnings()
context = ssl._create_unverified_context()


def init_param():
    joiner = ' '
    # 并发数
    max_concurrent = 64
    concurrent = 1
    execute_num = 1
    if len(sys.argv) > 1:
        try:
            input_concurrent = int(sys.argv[1])
            if input_concurrent > 1:
                concurrent = min(input_concurrent, max_concurrent)
        except Exception as e:
            print("并发数设置范围[1, {}], 默认1".format(max_concurrent))
            print(e)
    if len(sys.argv) > 2:
        try:
            if int(sys.argv[2]) > 1:
                execute_num = int(sys.argv[2])
        except Exception as e:
            print(e)
    init_cookie = auto_login()
    executor = ThreadPoolExecutor(max_workers=concurrent)
    return [joiner, execute_num, init_cookie, executor]


def execute_http(i):
    """
    执行excuteUrl.json接口
    :param i 仅用于计数虚拟参数
    :return:
    """
    with open("./excuteUrl.json", 'r') as request_data:
        request_json = json.load(request_data)
    url = request_json['url']
    method = request_json['method']
    request_headers = handle_json_str_value(request_json['headers'])
    executeStartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    request_headers['Cookie'] = init_cookie
    request_body = handle_json_str_value(request_json['body'])
    response_body = {
        "status": -1,
        "msg": "接口执行失败",
        "data": "请检查接口是否返回JSON格式的相应数据, 以及抛出未经处理的特殊异常"
    }
    try:
        response = requests.request(method, url, headers=request_headers, json=request_body, timeout=3, verify=False)
        # JSON标准格式
        response_body = json.dumps(response.json(), ensure_ascii=False, indent=4)
    except Exception as e:
        print(e)
    executeEndTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return "executeStartTime=[{}], executeEndTime=[{}]\n响应结果:\n{}".format(executeStartTime, executeEndTime, response_body)


def auto_login():
    """
    自动登录, 获取登录Cookie
    """
    with open("./ssoLogin.json", 'r') as sso_login_request_data:
        request_json = json.load(sso_login_request_data)
    url = request_json['url']
    method = request_json['method']
    request_headers = handle_json_str_value(request_json['headers'])
    request_body = handle_json_str_value(request_json['body'])
    # request_headers = {"Content-Type": "application/json", "HT-app": "6"}
    response = requests.request(method, url, headers=request_headers, json=request_body, timeout=3, verify=False)
    response_headers = response.headers
    # 处理Cookie, 多个Cookie之间使用';'分隔, 否则校验cookie时出现"domain."在高版本中tomcat中报错
    # https://blog.csdn.net/w57685321/article/details/84943176
    cookie = response_headers.get("set-Cookie").replace(", _r", "; _r").replace(", _a", "; _a")
    # JSON标准格式
    response_body = json.dumps(response.json(), ensure_ascii=False, indent=4)
    print("登录响应Cookie结果: \n{}\n登录响应BODY结果: {}".format(cookie, response_body))
    return cookie


def handle_json_str_value(json):
    """
    将json的值都变为字符串处理
    :param json:
    :return:
    """
    for (k, v) in json.items():
        json[k] = str(v)
    return json


def main():
    # 初始化参数
    initial_param_list = init_param()
    # 全局变量
    global joiner
    global execute_num
    global init_cookie
    global executor
    joiner = initial_param_list[0]
    execute_num = initial_param_list[1]
    init_cookie = initial_param_list[2]
    executor = initial_param_list[3]
    nums = list(range(0, execute_num))
    for result in executor.map(execute_http, nums):
        print(result)


if __name__ == '__main__':
    main()
