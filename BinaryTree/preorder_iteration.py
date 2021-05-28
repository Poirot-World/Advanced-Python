class TreeNode(object):
    #创建一个节点类

    def __init__(self, val=0):

        self.val = val
        self.left = None
        self.right = None

class Order(object):
    #创建一个排序类

    def preorder(self, root:TreeNode):  #前序遍历

        re =[]

        if not root: return re

        stack =[]
        node = root

        while stack or node:        #中间节点
            while stack:
                node = stack.pop()
            re.append(node.val)

            if node.right: stack.append(node.right)  #右边节点
            if node.left: stack.append(node.left)    #左边节点

        return re



root = TreeNode(1)
order = Order()
print(order.preorder(root))

