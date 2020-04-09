def begin():
    print("装饰开始：瓜子板凳备好，坐等[生成]")


def end():
    print("装饰结束：瓜子嗑完了，板凳坐歪了，撤！")


def wrapper_counter_generator(func):
    # 接受func的所有参数
    def wrapper(*args, **kwargs):
        # 处理前
        begin()
        # 执行处理
        result = func(*args, **kwargs)
        # 处理后
        end()
        # 返回处理结果
        return result
    # 返回装饰的函数对象
    return wrapper


class DIGCounter:
    """
    装饰器-迭代器-生成器，一体化打包回家
    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __iter__(self):
        """
        迭代获取的当前元素
        :rtype: object
        """
        return self

    def __next__(self):
        """
        迭代获取的当前元素的下一个元素
        :rtype: object
        :exception StopIteration
        """
        if self.start > self.end:
            raise StopIteration
        current = self.start
        self.start += 1
        return current

    @wrapper_counter_generator
    def counter_generator(self):
        """
        获取生成器
        :rtype: generator
        """
        while self.start <= self.end:
            yield self.start
            self.start += 1


def main():
    """
    迭代器/生成器(iterator)是不可重复遍历的，
    而可迭代对象(iterable)是可以重复遍历的，
    iter()内置方法只会返回不可重复遍历的迭代器
    """

    k_list = list(DIGCounter(1, 19))
    even_list = [e for e in k_list if not e % 2 == 0]
    odd_list = [e for e in k_list if e % 2 == 0]
    print(even_list)
    print(odd_list)

    g_list = DIGCounter(1, 19).counter_generator()
    five_list = [e for e in g_list if e % 5 == 0]
    print(five_list)


if __name__ == '__main__':
    main()
