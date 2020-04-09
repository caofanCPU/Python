# -*- coding: utf-8 -*-
import os

import pandas as pd
import numpy as np


def load_data():
    """
    读取数据文件，推荐CSV格式
    :return:
    """
    work_main_dir = os.path.dirname(__file__) + os.path.sep
    file_path = work_main_dir + "激活学生列表.xlsx"
    return pd.read_excel(file_path)


def main():
    data = load_data()
    account_id_list = np.array(data['account_id']).tolist()
    print(', \n'.join([str(i) for i in account_id_list]))


if __name__ == '__main__':
    main()


