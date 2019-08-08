#!/usr/bin/env python
# coding: utf-8
# author: polarbird <jlm0808@126.com>

from ai.crawler import WeixinCrawler


def main():
    crawler()


def crawler():
    c = WeixinCrawler()
    c.get(['data-is-king'])


# def crawler():
#     c = WeixinClient()
#     html = c.get('https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3MzI4MjgzMw==&f=json&offset=20&count=10&is_ok=1&scene=124&uin=MTE1MDEzMzI4MA%3D%3D&key=463a4b7a72c8cab5f90bdc2a2abb5156eae7957a8d5d06b105353caa7cc9b2055850965795f8527668c205cb5f25356d15dd383cd82a28084eaa333467be0940821b6f77a8d01b7a03ddae265ae43737&pass_ticket=N7rfTPNd6zjMa9FhXb4xguRlBPAJc8LbrlH4a0bfpBrkIo9nSyjqg4QChiQ9mQWV&wxtoken=&appmsg_token=966_L%252FGNaEsWT4RNv188Jfa0n2rHXYIS-4ydS-GYuA~~&x5=0&f=json')
#     soup = c.formatHtml(html)
#     print(soup)

# def nlp():
#     print(Kernel().nlp.tag(['亚投行意向创始成员国确定为57个', '“流量贵”频被吐槽']))

if __name__ == '__main__':
    main()
