#!/usr/bin/env python
# coding: utf-8
# author: Leo <jiangwenhua@yoyohr.com>

# from ai.crawler import http_client

import unittest


def addNum(a, b):
    return a + b


def delNum(a, b):
    return a - b


class TestCase(unittest.TestCase):
    def testAdd(self):
        self.assertEqual(2, addNum(1, 1))

    def testDel(self):
        self.assertEqual(0, delNum(1, 1))


if __name__ == "__main__":
    unittest.main()
