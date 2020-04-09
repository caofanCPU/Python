# -*- coding: utf-8 -*-
import os
import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt


def load_data():
    """
    读取数据文件，推荐CSV格式
    :return:
    """
    work_main_dir = os.path.dirname(__file__) + os.path.sep
    file_path = work_main_dir + "PDF.csv"
    return pd.read_csv(file_path)


def calculate_statistical_indicators(data, delta):
    """
    对数据序列计算：最大值/最小值/平均值/标准差，以及根据组距计算分组坐标
    :param data: 原始数据列
    :param delta: 分组区间长度
    :return: [最大值, 最小值, 平均值, 标准差, 分组间距, 分组数, 分组序号, 分组坐标点, 分组区间, 分组频次]
    :           0      1      2      3       4       5      6         7        8        9
    """
    def dataframe_tolist(dataframe_data):
        return sum(np.array(dataframe_data).tolist(), [])

    # 统计指标数据
    statistical_indicators = [float(data.max()), float(data.min()), float(data.mean()), float(data.std())]
    # 数据转换
    datavalue = dataframe_tolist(data)
    # 分组数
    split_group = math.ceil((statistical_indicators[0] - statistical_indicators[1]) / delta) + 1
    # 分组自然编号序列
    group_nos = list(np.arange(1, split_group + 1, 1))
    # 分组坐标节点序列
    group_coordinates = list(statistical_indicators[1] + (np.array(group_nos) - 1) * delta)
    # 分组坐标区间序列
    group_sections = []
    # 统计分组坐标区间频次, 统计标准左开右闭：(,]
    group_frequencies = {}
    for i in group_nos:
        i -= 1
        if i == 0:
            group_sections.append([0, group_coordinates[i]])
        else:
            group_sections.append([group_coordinates[i - 1], group_coordinates[i]])

        start = group_sections[i][0]
        end = group_sections[i][1]
        count = 0
        for value in datavalue:
            if start < value <= end:
                count += 1
        group_frequencies.update({i: count})
    statistical_indicators.append(delta)
    statistical_indicators.append(split_group)
    statistical_indicators.append(group_nos)
    statistical_indicators.append(group_coordinates)
    statistical_indicators.append(group_sections)
    statistical_indicators.append(group_frequencies)
    statistical_indicators.append(datavalue)

    return statistical_indicators


def normal_distribution_pdf(x, mu, sigma):
    """
    正态分布概率密度函数
    Normal distribution probability density function
    :return: 
    """
    if sigma == 0:
        return 0
    return np.exp(-((x-mu)**2 / (2 * sigma**2))) / (sigma * np.sqrt(2*np.pi))


def calculate_points(mu, sigma):
    point = []
    i = mu - 2 * sigma
    while mu - 2 * sigma <= i <= mu + 2 * sigma:
        point.append(i)
        i += sigma
    x = np.array(point)
    y = normal_distribution_pdf(x, mu, sigma)
    for i in range(0, len(x)):
        print(x[i], y[i])
    return [x, y]


def plot_pdf(statistical_indicators):
    plt.figure("NormalDistribution-PDF")
    # plt.grid()
    plt.xlabel("Student-Score")
    plt.ylabel("Probability-Value")
    plt.title("Figure-1.1")
    plt.xlim(0.00, 140.00)
    plt.ylim(0.00, 0.055)

    data = statistical_indicators[len(statistical_indicators) - 1]
    plt.hist(data, bins=23, rwidth=5, density=True, color='yellow')

    mu, sigma = statistical_indicators[2], statistical_indicators[3]
    coordinates = statistical_indicators[7]
    # 增加0值起始点
    coordinates.insert(0, 0)
    x = np.array(coordinates)
    y = normal_distribution_pdf(x, mu, sigma)
    plt.plot(x, y, color='red', linewidth=2)

    points = calculate_points(mu, sigma)
    plt.scatter(points[0], points[1], marker='<', s=30, c='green')

    # 绘制垂线plt.vlines
    for x_i in points[0]:
        plt.vlines(x_i, plt.ylim()[0], plt.ylim()[1], linestyles=':', linewidth=1)

    # 绘制水平线plt.hlines
    # plt.hlines(0.025, plt.xlim()[0], plt.xlim()[1], linestyles=':', linewidth=1)
    plt.show()


def main():
    data = load_data()
    delta = 1
    statistical_indicators = calculate_statistical_indicators(data, delta)
    plot_pdf(statistical_indicators)


if __name__ == '__main__':
    main()


