#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random
import time

import requests


def main():
    parser = argparse.ArgumentParser(description="帝八嫂的小秘密")
    parser.add_argument("-l", "--loop", type=int, default=20, help="下载次数默认20")
    parser.add_argument("-d", "--delay", type=int, default=5, help="延时默认5秒")
    args = parser.parse_args()
    loop = args.loop
    if loop < 0:
        loop = 20
    delay = args.delay
    if delay < 0:
        delay = 5
    print("参数设置结果: 下载次数=[{}], 延时=[{}]s".format(loop, delay))
    tasks = list(range(1, loop + 1))
    download_url = "https://plugins.jetbrains.com/plugin/download?rel=true&updateId=92649"
    # 添加头部，伪装浏览器，字典格式
    headers_0 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'}
    headers_1 = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    headers_2 = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'}
    for i in tasks:
        print("执行第[{}]次下载任务".format(i))
        # 随机获取浏览器代理
        seed = random.randint(0, 10000)
        mod = seed % 3
        headers = headers_0
        if mod == 1:
            headers = headers_1
        if mod == 2:
            headers = headers_2

        jet = requests.get(download_url, headers=headers)

        file_name = "D8{}.zip".format(i)

        # 下载文件
        with open(file_name, "wb") as d8ger_writer:
            d8ger_writer.write(jet.content)

        # 延时5秒执行
        time.sleep(delay)


if __name__ == '__main__':
    main()
