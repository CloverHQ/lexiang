#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-11-24 18:11
# @Author  : liuwenchao
# @File    : lexianglanew
# @Software: IntelliJ IDEA

import requests


class LeXiangVJ:

    def __init__(self):
        self.pending_list = self.journal_list()
        pass

    def init_headers(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/103.0.0.0 '
                          'Safari/537.36',
            'cookie': 'rememberme-wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw'
                      '=d281OHlZQ1FBQUNURzM5OGUyZ1kwOHBCN084bmo2LUFAMzAzMzgyOjE'
                      '2Njk4ODg3MzcxMTY6ODQ2OTYyMzk2YjAxYTZlMmExOGU4NzI5NWI2Njk2MzM',
            'accept': 'application/json;charset=utf-8'
        }
        return headers

    def read(self):
        # https://qy.51vj.cn/announcement/page?_=1669291733894&_v=1.8.12&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=64&parentid=1002&cms_id=836323
        pass

    def comment(self):
        pass

    def like(self):
        pass

    def journal_list(self):
        # https://qy.51vj.cn/home/list?_=1669288714544&_v=3.22.14&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=1002&page=1&size=10&app_ids=64,36&check-latest=true
        # 获取最新的文章列表
        response = requests.get(
            'https://qy.51vj.cn/home/list?_=1669288714544&_v=3.22.14&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=1002&page=1&size=10&app_ids=64,36&check-latest=true',
            headers=self.init_headers())
        home_contents = response.json()['home_contents']

        pending_list = []

        for content in home_contents:
            # https://qy.51vj.cn/announcement//836323?_=1669288714611&_v=3.22.14&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=64
            app_id = content['app_id']
            business_id = content['business_id']
            business_type = content['business_type']
            if app_id == 64:
                url = 'https://qy.51vj.cn/userpreference/prise/list?_=1669293338751&_v=1.8.12&app-id=64&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&' \
                      'appid=64&parentid=1002&business-id={0}&business-type={1}&business-sec-id=0&page-num=1&page-size=10'.format(business_id, business_type)
                prise_count = requests.get(url, headers=self.init_headers()).json()['total_count']
            elif app_id == 36:

                url = 'https://qy.51vj.cn/magazine/{0}?_=1669288714611&_v=3.22.14' \
                      '&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=36&page=1&size=15&article=1' \
                    .format(business_id)
                prise_count = requests.get(url, headers=self.init_headers()).json()['journal']['articles'][0]['number'][
                    'prise']

                # https://qy.51vj.cn/userpreference/prise/?_=1669291733897&_v=1.8.12&app-id=64&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=64&parentid=1002&business-id=836323&business-type=30301&business-sec-id=0
                prise_url = 'https://qy.51vj.cn/userpreference/prise/?_=1669291733897&_v=1.8.12&app-id=64' \
                            '&corpid=wp58yYCQAAIPCiRQrU7UaqV4bgPo05Vw&appid=64&parentid=1002' \
                            '&business-id={0}&business-type={1}&business-sec-id=0'.format(business_id, business_type)
                msg = requests.get(prise_url, headers=self.init_headers()).json()['msg']
                # 点赞总数大于50并且自己未点赞的文章
                if prise_count > 50 and msg == '记录不存在':
                    data = {
                        'app_id': app_id,
                        'business_id': business_id,
                        'business_type': business_type
                    }
                    pending_list.append(data)
        print(pending_list)
        return pending_list


if __name__ == '__main__':
    vj = LeXiangVJ()
