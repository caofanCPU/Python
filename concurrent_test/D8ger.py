#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import random
import time

import requests
import logging


def user_agent() -> list:
    opera_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50'}
    opera_2 = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50'}
    opera_3 = {'User-Agent': 'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'}
    firefox_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'}
    firefox_2 = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10'}
    safari = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2'}
    chrome_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'}
    chrome_2 = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
    chrome_3 = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'}
    taobao = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11'}
    liebao_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'}
    liebao_2 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)'}
    qq_1 = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)'}
    qq_2 = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)'}
    qq_3 = {'User-Agent': 'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
    sougou_1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'}
    sougou_2 = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)'}
    maxthon = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36'}
    uc = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'}
    iphone = {'User-Agent': 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
    ipod = {'User-Agent': 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
    ipad_1 = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'}
    ipad_2 = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'}
    android_1 = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
    android_2 = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'}
    pad_moto_xoom = {'User-Agent': 'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13'}
    black_berry = {'User-Agent': 'Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+'}
    hp_touch_pad = {'User-Agent': 'Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0'}
    nokia_n97 = {'User-Agent': 'Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124'}
    windows_phone_mango = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)'}
    first_list = [opera_1, opera_2, opera_3, firefox_1, firefox_2, safari]
    second_list = [chrome_1, chrome_2, chrome_3, taobao, liebao_1, liebao_2]
    third_list = [qq_1, qq_2, qq_3, sougou_1, sougou_2, maxthon, uc, iphone]
    fourth_list = [ipod, ipad_1, ipad_2, android_1, android_2, pad_moto_xoom]
    fifth_list = [black_berry, hp_touch_pad, nokia_n97, windows_phone_mango]
    first_list.extend(second_list)
    first_list.extend(third_list)
    first_list.extend(fourth_list)
    first_list.extend(fifth_list)
    return first_list


def build_logs():
    # 设置log名称
    log_name = "v5.log"
    # 定义logger
    logger = logging.getLogger()
    # 设置级别为debug
    logger.setLevel(level=logging.DEBUG)
    # 设置 logging文件名称
    handler = logging.FileHandler(log_name)
    # 设置级别为debug
    handler.setLevel(logging.DEBUG)
    # 设置log的格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    # 将格式压进logger
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # 写入logger
    logger.addHandler(handler)
    logger.addHandler(console)
    # 将logger返回
    return logger


def execute_download():
    parser = argparse.ArgumentParser(description="帝八嫂的小秘密")
    parser.add_argument("-l", "--loop", type=int, default=200, help="下载次数默认200")
    parser.add_argument("-d", "--delay", type=int, default=0, help="延时默认0秒")
    args = parser.parse_args()
    loop = args.loop
    if loop < 0:
        loop = 200
    delay = args.delay
    if delay < 0:
        delay = 0
    # 日志
    logger = build_logs()
    logger.debug("参数设置结果: 下载次数=[{}], 延时=[{}]s".format(loop, delay))
    tasks = list(range(1, loop + 1))
    download_url = "https://plugins.jetbrains.com/plugin/download?rel=true&updateId=92649"
    # 添加头部，伪装浏览器，字典格式
    agent_list = user_agent()
    gama = len(agent_list)
    failed = 0
    for i in tasks:
        logger.debug("执行第[{}]次下载任务".format(i))
        # 随机获取浏览器代理
        seed = random.randint(0, 1000)
        index = seed % gama
        headers = agent_list[index]
        file_name = "D8{}.zip".format(i)
        try:
            logger.debug("第[{}]次下载任务: [随机数={}], [索引={}],\n[浏览器代理={}]".format(i, seed, index, headers))
            jet = requests.get(download_url, headers=headers, timeout=600)
            # 下载文件
            with open(file_name, "wb") as d8ger_writer:
                d8ger_writer.write(jet.content)
        except Exception as e:
            # 服务端关闭连接, 防火墙超时关闭连接, 或其他异常
            logger.error("第[{}]次下载任务出现异常, 原因: {}".format(i, e))
            failed += 1
            # 继续下一次
            continue
        # 延时5秒执行
        logger.debug("文件[{}]下载完成".format(file_name))
        if delay > 0:
            time.sleep(delay)
    logger.debug("失败[{}]次, 成功下载[{}]次".format(failed, loop - failed))


def main():
    execute_download()


if __name__ == '__main__':
    main()
