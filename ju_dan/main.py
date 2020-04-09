#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


import logging
import time

import itchat
import pymysql


# 注册对文本消息进行监听，对群聊进行监听
@itchat.msg_register(itchat.content.INCOME_MSG, isGroupChat=True)
def handle_content(msg):
    try:
        msg_type = msg['MsgType']
        if msg_type == 1:
            content = msg['Text']
        else:
            content = '非文本内容'
        time_stamp = msg['CreateTime']
        create_time = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time_stamp))
        current_talk_group_id = msg['User']['UserName']
        current_talk_group_name = msg['User']['NickName']
        from_user_name = msg['ActualNickName']
        from_user_id = msg['ActualUserName']
        sql = "INSERT INTO wx_group_chat(msg_type, content, sender_id, sender_name,\
                 group_id, group_name, time_stamp, create_time) \
                  VALUE ('%d','%s','%s','%s','%s','%s','%d','%s');"\
              % (int(msg_type), content, from_user_id, from_user_name,\
                 current_talk_group_id, current_talk_group_name, int(time_stamp), create_time)
        exe_db(db, sql, logger)
    except Exception as e:
        logger.debug(e)
        return


def build_logs():
    # 获取当前时间
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    # 设置log名称
    log_name = "wx.log"
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


def connect_mysql(logger):
    try:
        db = pymysql.connect(host='47.93.206.227', port=3306, user='root', passwd='root', db='spring_clould', charset='utf8mb4')
        # db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='spring_clould', charset='utf8mb4')
        return db
    except Exception as e:
        logger.debug('MySQL数据库连接失败')
        logger.debug(e)


def exe_db(db, sql, logger):
    try:
        cursor = db.cursor()
        db.ping(reconnect=True)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        logger.debug('SQL执行失败,请至日志查看该SQL记录')
        logger.debug(sql)
        logger.debug(e)


def select_db(db, sql, logger):
    try:
        cursor = db.cursor()
        db.ping(reconnect=True)
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        logger.debug('SQL执行失败,请至日志查看该SQL记录')
        logger.debug(sql)
        logger.debug(e)


def main():
    # 手机扫码登录
    newInstance = itchat.new_instance()
    newInstance.auto_login(hotReload=True, enableCmdQR=2)
    global logger
    logger = build_logs()
    global db
    db = connect_mysql(logger)
    # 持续运行
    itchat.run()


if __name__ == '__main__':
    main()
