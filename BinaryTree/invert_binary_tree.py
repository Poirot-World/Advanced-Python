# -*- coding: utf-8 -*-
"""
Created on Fri May 28 19:48:57 2021

@author: lenovo
"""
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return root
        
        left = self.invertTree(root.left)
        right = self.invertTree(root.right)        
        root.left, root.right = right, left
        
        return root

