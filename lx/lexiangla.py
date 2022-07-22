#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-07-21 16:54
# @Author  : liuwenchao
# @File    : lexiangla
# @Software: IntelliJ IDEA
import os
import re
import urllib.parse

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'cookie': os.environ['LX_COOKIE'],
    'x-xsrf-token': ''
}

list = []


def yjsl():
    k8_resp = requests.get('https://lexiangla.com/gapi/v1/teams?limit=30&page=1&filter=list', headers=headers)
    if k8_resp.status_code == 200:
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
                    list.append(doc_detail_resp['name'])
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
        send_bark('任务成功', '任务执行完毕 ^_^' + '\n'.join(list))
    else:
        print("未登录")
        send_bark('登陆信息失效', '登陆信息失效, 请重新登陆~')


def send_bark(title, content):
    requests.get("https://api.day.app/" + os.environ['BARK_KEY'] + '/' + title + '/' + content)


if __name__ == '__main__':
    yjsl()
