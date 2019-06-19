class TreeNode:
    """This is the Class Node with constructor that contains data variable to type data and left,right pointers."""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def new_in_order_traversal(self) -> list:
        """
        (代码优化)深度优先-中序遍历
        :return: list[TreeNode]
        """
        if self is None:
            return []
        return self.in_order_traversal(self.left) + [self] + self.in_order_traversal(self.right)

    def in_order_traversal(self, current_node) -> list:
        """
        (冗余传参)深度优先-中序遍历
        :type current_node: TreeNode
        :return: list[TreeNode]
        """
        if current_node is None:
            return []
        return self.in_order_traversal(current_node.left) + [current_node] + self.in_order_traversal(current_node.right)

    def pre_order_traversal(self) -> list:
        """
        深度优先-前序遍历
        :return: list[TreeNode]
        """
        if self is None:
            return []
        return [self] + self.left.pre_order_traversal() + self.right.pre_order_traversal()

    def post_order_traversal(self) -> list:
        """
        深度优先-后序遍历
        :return: list[TreeNode]
        """
        if self is None:
            return []
        return self.left.post_order_traversal() + self.right.post_order_traversal() + [self]

    @classmethod
    def base_width_order_traversal(cls, root) -> list:
        """
        基本广度优先遍历
        :type root: TreeNode
        :return: list[TreeNode]
        """

        def base_recursion_helper(current_node, current_level):
            """
            基本递归遍历，同一层次由左到右遍历
            :type current_level: int
            :type current_node: TreeNode
            """
            # 递归结束条件
            if current_node is None:
                return

            # 收集本层元素
            sol[current_level - 1].append([current_node])

            # 新的一层元素，需要添加收集容器
            if len(sol) == current_level:
                sol.append([])

            # 先左子树
            base_recursion_helper(current_node.left, current_level + 1)
            # 后右子树
            base_recursion_helper(current_node.right, current_level + 1)

        sol = [[]]
        base_recursion_helper(root, 1)
        # sol为三层嵌套list, 且需要去除最后一个空元素[]，以下方式可将三层list[]元素平铺为一层
        result_list = sum(sum(sol[:-1], []), [])
        # result_list = [tree_node for second_list in sol[:-1] for third_list in second_list for tree_node in third_list]
        return result_list

    @classmethod
    def level_reverse_width_order_traversal(cls, root) -> list:
        """
        基本广度优先遍历
        :type root: TreeNode
        :return: list[TreeNode]
        """

        def level_reverse_recursion_helper(current_node, current_level):
            """
            基本递归遍历，同一层次由左到右遍历
            :type current_level: int
            :type current_node: TreeNode
            """
            # 递归结束条件
            if current_node is None:
                return

            # 收集本层元素
            sol[current_level - 1].append([current_node])

            # 新的一层元素，需要添加收集容器
            if len(sol) == current_level:
                sol.append([])

            # 先右子树
            level_reverse_recursion_helper(current_node.right, current_level + 1)
            # 后左子树
            level_reverse_recursion_helper(current_node.left, current_level + 1)

        sol = [[]]
        level_reverse_recursion_helper(root, 1)
        # sol为三层嵌套list, 且需要去除最后一个空元素[]，以下方式可将三层list[]元素平铺为一层
        result_list = sum(sum(sol[:-1], []), [])
        # result_list = [tree_node for second_list in sol[:-1] for third_list in second_list for tree_node in third_list]
        return result_list

    @classmethod
    def zigzag_width_order_traversal(cls, root) -> list:
        """
        锯齿型广度优先遍历
        :type root: TreeNode
        :return: list[TreeNode]
        """

        def zigzag_recursion_helper(current_node, current_level):
            """
            基本递归遍历，同一层次由左到右遍历
            :type current_level: int
            :type current_node: TreeNode
            """
            # 递归结束点
            if current_node is None:
                return
            # 按照奇偶层进行拼接
            if current_level % 2 == 1:
                # 收集本层元素，后插
                sol[current_level - 1].append([current_node])
            else:
                # 收集本层元素，前插
                sol[current_level - 1].insert(0, [current_node])

            # 新的一层元素，需要添加收集容器
            if len(sol) == current_level:
                sol.append([])

            # 先左子树
            zigzag_recursion_helper(current_node.left, current_level + 1)
            # 后右子树
            zigzag_recursion_helper(current_node.right, current_level + 1)

        sol = [[]]
        zigzag_recursion_helper(root, 1)
        # sol为三层嵌套list, 且需要去除最后一个空元素[]，以下方式可将三层list[]元素平铺为一层
        result_list = sum(sum(sol[:-1], []), [])
        # result_list = [tree_node for second_list in sol[:-1] for third_list in second_list for tree_node in third_list]
        return result_list

    def depth_of_tree(self) -> int:
        """
        树的深度
        :return: int
        """
        if self is None:
            return 0
        return 1 + max(self.left.depth_of_tree(), self.right.depth_of_tree())

    def is_full_binary_tree(self) -> bool:
        """
        检查是否为满二叉树
        :return: bool
        """
        if self is None:
            return True
        if (self.left is None) and (self.right is None):
            return True
        if (self.left is not None) and (self.right is not None):
            return self.left.is_full_binary_tree() and self.right.is_full_binary_tree()
        return False


def test_init_tree() -> TreeNode:
    """
    测试使用，构造树
                            1
            2                                   3
    4               5                   7
                6               8
                                    9
    :return: TreeNode
    """
    tree = TreeNode(1)
    tree.left = TreeNode(2)
    tree.right = TreeNode(3)
    tree.left.left = TreeNode(4)
    tree.left.right = TreeNode(5)
    tree.left.right.left = TreeNode(6)
    tree.right.left = TreeNode(7)
    tree.right.left.left = TreeNode(8)
    tree.right.left.left.right = TreeNode(9)
    return tree


def test_in_order_traversal():
    """
    二叉树中序遍历测试
    """
    init_tree = test_init_tree()
    in_order_result = init_tree.in_order_traversal(init_tree)
    in_order_data = fetch_tree_data(in_order_result)
    out(in_order_data)


def test_new_in_order_traversal():
    """
    二叉树中序遍历测试
    """
    init_tree = test_init_tree()
    in_order_result = init_tree.new_in_order_traversal()
    in_order_data = fetch_tree_data(in_order_result)
    out(in_order_data)


def test_pre_order_traversal():
    """
    二叉树前序遍历测试
    """
    init_tree = test_init_tree()
    pre_order_result = init_tree.pre_order_traversal()
    pre_order_data = fetch_tree_data(pre_order_result)
    out(pre_order_data)


def test_post_order_traversal():
    """
    二叉树后序遍历测试
    """
    init_tree = test_init_tree()
    post_order_result = init_tree.post_order_traversal()
    post_order_data = fetch_tree_data(post_order_result)
    out(post_order_data)


def test_basic_width_order_traversal():
    """
    二叉树基本层次遍历测试
    """
    init_tree = test_init_tree()
    basic_width_order_result = TreeNode.base_width_order_traversal(init_tree)
    basic_width_order_data = fetch_tree_data(basic_width_order_result)
    out(basic_width_order_data)


def test_level_reverse_width_order_traversal():
    """
    二叉树同层反序层次遍历测试
    """
    init_tree = test_init_tree()
    level_reverse_width_order_result = TreeNode.level_reverse_width_order_traversal(init_tree)
    level_reverse_width_order_data = fetch_tree_data(level_reverse_width_order_result)
    out(level_reverse_width_order_data)


def test_zigzag_width_order_traversal():
    """
    二叉树同层反序层次遍历测试
    """
    init_tree = test_init_tree()
    zigzag_width_order_result = TreeNode.zigzag_width_order_traversal(init_tree)
    zigzag_width_order_data = fetch_tree_data(zigzag_width_order_result)
    out(zigzag_width_order_data)


def fetch_tree_data(tree_list) -> list:
    """
    根据树的平铺列表，获取数据[data]
    :type tree_list: list
    :return: list[TreeNode.data]
    """
    return [e.data for e in tree_list if e is not None]


def out(content):
    """
    输出内容
    :type content: object
    """
    print(content)


def main():
    """
    python函数及其参数约定： https://www.cnblogs.com/xialiaoliao0911/p/9430491.html
    """

    tree = '''
                          初始树
                            1
            2                                   3
    4               5                   7
                6               8
                                    9
    
    '''
    out(tree)

    out("深度优先之[前序]遍历：")
    test_in_order_traversal()

    out("(代码优化后的)深度优先之[前序]遍历:")
    test_new_in_order_traversal()
    # out("深度优先之[中序]遍历：")
    # test_pre_order_traversal()
    #
    # out("深度优先之[后序]遍历：")
    # test_post_order_traversal()
    #
    # out("广度优先之正序层次遍历：")
    # test_basic_width_order_traversal()
    #
    # out("广度优先之同层反遍历：")
    # test_level_reverse_width_order_traversal()
    #
    # out("广度优先之锯齿型遍历：")
    # test_zigzag_width_order_traversal()


if __name__ == '__main__':
    main()
