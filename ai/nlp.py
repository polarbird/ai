#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

from bosonnlp import BosonNLP


class YoNLP:
    def __init__(self, boson_api_token):
        self._nlp = BosonNLP(boson_api_token)

    def sentiment(self, contents):
        return self._nlp.sentiment(contents)

    def tag(self, contents):
        return self._nlp.tag(contents)
