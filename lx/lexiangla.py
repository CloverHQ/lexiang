#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-07-21 16:54
# @Author  : liuwenchao
# @File    : lexiangla
# @Software: IntelliJ IDEA
import re
import urllib.parse

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'cookie': '',
    'x-xsrf-token': ''
}


def yjsl():
    k8_resp = requests.get('https://lexiangla.com/gapi/v1/teams?limit=30&page=1&filter=list', headers=headers)
    for k8 in k8_resp.json()['data']:
        if not (1 == k8['is_secret'] or 1 == k8['type']):
            doc_list = requests.get(
                'https://lexiangla.com/tapi/leda/teams/' + k8['code'] + '/v1/list?module=doc&type=latest&limit=5',
                headers=headers)
            for doc in doc_list.json()['data']:
                doc_detail = requests.get(
                    'https://lexiangla.com/api/v1/teams/' + k8['code'] + '/docs/' + doc[
                        'id'] + '?lazy_load=1&increment=1',
                    headers=headers)
                doc_detail_resp = doc_detail.json()
                print(doc_detail_resp['read_count'])
                if not (doc_detail_resp['target']['is_favorited'] and doc_detail_resp['target']['is_liked']):
                    headers['x-xsrf-token'] = urllib.parse.unquote(
                        re.search('XSRF-TOKEN=(.*?);', doc_detail.headers['set-cookie']).group(1))

                    # 点赞
                    print(requests.put(
                        'https://lexiangla.com/api/v1/staff/likes/documents/' + doc_detail_resp['target_id'],
                        headers=headers).status_code)
                    # 收藏
                    print(requests.put(
                        'https://lexiangla.com/api/v1/staff/favorites/documents/' + doc_detail_resp['target_id'],
                        headers=headers).status_code)
                    # 评论
                    payload = {
                        "target_id": doc_detail_resp['target_id'],
                        'target_type': 'document',
                        'content': '/强'
                    }
                    requests.post("https://lexiangla.com/api/v1/comments", data=payload, headers=headers)


if __name__ == '__main__':
    yjsl()