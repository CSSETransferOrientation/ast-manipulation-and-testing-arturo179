#!/usr/bin/python3
import os
from os.path import join as osjoin

import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'operator'])

class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        else:
            self.type = NodeType.operator
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.operator:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        if self.type == NodeType.operator and self.val == '+':
            if self.right.type == NodeType.number and self.right.val == '0':
                return self.left
            elif self.left.type == NodeType.number and self.left.val == '0':
                return self.right
        
        if self.type == NodeType.operator:
            if self.left:
                self.left = self.left.additive_identity()
            if self.right:
                self.right = self.right.additive_identity()
        
        return self

    def multiplicative_identity(self):
        if self.type == NodeType.operator and self.val == '*':
            if self.right.type == NodeType.number and self.right.val == '1':
                return self.left
            elif self.left.type == NodeType.number and self.left.val == '1':
                return self.right
        
        if self.type == NodeType.operator:
            if self.left:
                self.left = self.left.multiplicative_identity()
            if self.right:
                self.right = self.right.multiplicative_identity()

        return self
        # IMPLEMENT ME!
    
                
    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        self = self.additive_identity()
        self = self.multiplicative_identity()
        return self
        #self.multiplicative_identity()
       # self.mult_by_zero()
        #self.constant_fold()

class BinOpAstTester(unittest.TestCase):
    # ins = osjoin(input('Enter test folder name (enter for testbench): ').strip() or 'testbench')
    ins = 'testbench'
    def testAll(self):
        print('\n')
        for test_type in os.listdir(self.ins):
            for test_file in os.listdir(osjoin(self.ins, test_type, 'inputs')):
                if test_file.endswith('.txt'):
                    with open(osjoin(self.ins, test_type, 'inputs', test_file)) as test:
                        test_name = test.readline().strip()
                        data = test.readline().strip()
                    with open(osjoin(self.ins, test_type, 'outputs', test_file)) as solution:
                        expected = solution.readline().strip()
                    print(f'Testing {test_name}')
                    with self.subTest(msg=f'Testing {test_name}', inp=data, expected=expected):
                        result = BinOpAst(list(data.split()))
                        result.simplify_binops()
                        result = result.prefix_str()
                        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
    


   