#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import ssl
from concurrent.futures.thread import ThreadPoolExecutor

import requests

import numpy as np
import argparse

# 屏蔽HTTPS证书校验, 忽略安全警告
requests.packages.urllib3.disable_warnings()
context = ssl._create_unverified_context()


def init_param() -> list:
    """
    初始化参数, 读取shell命令参数, 自动登录
    依次返回httpie_view方式, 线程池, 登录cookie
    :rtype: list
    """
    parser = argparse.ArgumentParser(description="并发执行接口")
    parser.add_argument("-w", "--workers", type=int, choices=choice_nums(1, 65, 1), default=1, help="并发执行线程数, 取值范围[1, 64]")
    parser.add_argument("-l", "--loops", type=int, default=1, help="循环执行次数")
    args = parser.parse_args()
    loops = args.loops
    if loops < 1:
        loops = 1
    print("参数设置结果: 执行次数=[{}], 并发线程数=[{}]".format(loops, args.workers))
    init_executor = ThreadPoolExecutor(max_workers=args.workers)
    cookie = auto_login()
    return [loops, init_executor, cookie]


def choice_nums(start: int, end: int, delta: int) -> list:
    """
    返回指定的数组序列
    :rtype: list
    """
    return np.arange(start, end, delta).tolist()


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
    request_headers['Cookie'] = init_cookie
    request_body = handle_json_str_value(request_json['body'])
    response_body = {
        "status": -1,
        "msg": "接口执行失败",
        "data": "请检查接口是否返回JSON格式的相应数据, 以及抛出未经处理的特殊异常"
    }
    executeStartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
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
    # 全局变量
    global execute_num
    global init_cookie
    global executor
    # 初始化参数
    initial_param_list = init_param()
    execute_num = initial_param_list[0]
    executor = initial_param_list[1]
    init_cookie = initial_param_list[2]
    nums = list(range(0, execute_num))
    # for result in executor.map(execute_http, nums):
    #     print(result)


if __name__ == '__main__':
    main()
