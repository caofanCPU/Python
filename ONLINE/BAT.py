#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import ssl
import unicodedata
from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd
import numpy as np
import requests
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
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--view", action="store_true", help="显示请求详细信息")
    group.add_argument("-hd", "--header", action="store_true", help="显示请求头")
    group.add_argument("-b", "--body", action="store_true", help="显示请求Body")
    group.add_argument("-d", "--download", action="store_true", help="显示请求头, 但响应结果保存至TXT")
    args = parser.parse_args()
    view_param = "-v"
    if args.header:
        view_param = "-h"
    if args.body:
        view_param = "-b"
    if args.download:
        view_param = "-d"
    print("参数设置结果: httpie命令方式=[{}], 并发线程数=[{}]".format(view_param, args.workers))
    init_executor = ThreadPoolExecutor(max_workers=args.workers)
    cookie = auto_login()
    return [view_param, init_executor, cookie]


def execute_http(id: int) -> str:
    """
    执行excuteUrl.json接口, 返回结果数据
    :param id: 接口请求标识性ID数据
    :rtype: str
    """
    with open("./excuteUrl.json", 'r') as request_data:
        request_json = json.load(request_data)
    url = request_json['url']
    method = request_json['method']
    request_headers = handle_json_str_value(request_json['headers'])
    request_headers['Cookie'] = init_cookie
    request_body = replace_id(request_json['body'], id)
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
    httpie_cmd_str = httpie(url, method, request_headers, request_body)
    return "执行命令httpie:\n{}\n当前ID=[{}], executeStartTime=[{}], executeEndTime=[{}]\n响应结果:\n{}".format(httpie_cmd_str, id, executeStartTime, executeEndTime, response_body)


def httpie(url: str, method: str, request_headers: json, request_body: json) -> str:
    """
    拼接httpie完整命令
    :param url: 接口访问路径
    :param method: 请求方式
    :param request_headers: 请求头JSON
    :param request_body: 请求Body体JSON
    :rtype: str
    """
    joiner = ' '
    cmd = "http"
    no_ca = "--verify=no"
    param_list = [cmd, no_ca, httpie_view]
    param_list.extend([method, url])
    for (k, v) in request_headers.items():
        if k == "Cookie":
            param_list.append("'" + k + ":" + v + "'")
        else:
            param_list.append(k + ":" + v)
    for (k, v) in request_body.items():
        if is_number(v):
            param_list.append(k + ":=" + v)
        else:
            param_list.append(k + "=" + v)
    return joiner.join(param_list)


def is_number(s: str) -> bool:
    """
    :param s: 输入字符串
    :rtype: bool
    """
    try:
        float(s)
        return True
    except ValueError:
        # ValueError为Python的一种标准异常，表示"传入无效的参数"
        # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
        pass
    try:
        # 把一个表示数字的字符串转换为浮点数返回的函数
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def load_data() -> list:
    """
    读取数据文件, 每行为一条数据
    :rtype: list
    """
    data = pd.read_csv("./ID.csv", header=-1)
    data.columns = ['id']
    return data['id']


def auto_login() -> str:
    """
    自动登录, 获取登录Cookie
    :rtype: str
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


def handle_json_str_value(json: json) -> json:
    """
    将json的值都变为字符串处理
    :param json:
    :rtype: json
    """
    for (k, v) in json.items():
        json[k] = str(v)
    return json


def replace_id(json: json, id: int) -> json:
    """
    将json的值都变为字符串处理
    :param json:
    :param id: 目标ID
    :rtype: json
    """
    for (k, v) in json.items():
        if v == "NONE":
            json[k] = str(id)
        else:
            json[k] = str(v)
    return json


def choice_nums(start: int, end: int, delta: int) -> list:
    """
    返回指定的数组序列
    :rtype: list
    """
    return np.arange(start, end, delta).tolist()


def main():
    # 全局变量
    global httpie_view
    global executor
    global init_cookie
    # 首先初始化数据
    init = init_param()
    httpie_view = init[0]
    executor = init[1]
    init_cookie = init[2]
    # 读取ID数据列表
    ids = load_data()
    for result in executor.map(execute_http, ids):
        print(result)


if __name__ == '__main__':
    main()
