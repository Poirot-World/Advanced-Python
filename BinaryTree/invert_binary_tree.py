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

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return True
        
        def dfs(left, right):
            
            if not (left or right):
                return True
            if not (left and right):
                return False
            if left.val != right.val:
                return False
 	#         outside = dfs(left.left, right.right)
	#         inside = dfs(left.right, right.left)
	#        
	#         return outside and inside            
            return dfs(left.left, right.right) and dfs(left.right, right.left)
        
        return dfs(root.left, root.right)

