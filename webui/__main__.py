#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

from ai.kernel import Kernel

kernel = Kernel()
# result = kernel.nlp.sentiment('武汉是个好地方')
# print(result)

print(kernel.crawler.get('http://yoyohr.com'))


