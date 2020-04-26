#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
import ssl
import unicodedata
import sys
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pandas as pd
import requests

# 屏蔽HTTPS证书校验, 忽略安全警告
requests.packages.urllib3.disable_warnings()
context = ssl._create_unverified_context()
joiner = ' '
cmd = "http"
no_ca = "--verify=no"
httpie_allow_view = {"-v": "显示请求详细信息", "-h": "显示请求头", "-b": "显示请求Body", "-d": "响应结果保存至TXT", "": "默认"}
httpie_view = None
# 最大并发数
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


def httpie(url, method, request_headers, request_body):
    param_list = [cmd, no_ca]
    if httpie_view is not None:
        param_list.append(httpie_view)
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


def is_number(s):
    try:
        # 如果能运行float(s)语句，返回True（字符串s是浮点数）
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


def replace_id(json, id):
    """
    将json的值都变为字符串处理
    :param json:
    :return:
    """
    for (k, v) in json.items():
        if v == "NONE":
            json[k] = str(id)
        else:
            json[k] = str(v)
    return json


def main():
    # 全局变量cookie, 初始化为空
    global init_cookie
    # 首先登陆一次
    init_cookie = auto_login()
    # 读取ID数据列表
    ids = load_data()
    for result in executor.map(httpie_cmd, ids):
        print(result)


if __name__ == '__main__':
    main()
