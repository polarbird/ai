#!/usr/bin/env python
# coding: utf-8
# author: Leo <jiangwenhua@yoyohr.com>

import os
import unittest

all_suite = unittest.TestLoader().discover(os.path.dirname(__file__), "test_*.py")