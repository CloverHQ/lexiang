#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-07-21 16:54
# @Author  : liuwenchao
# @File    : lexiangla
# @Software: IntelliJ IDEA
import json
import os
import re
import threading
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 '
                  'Safari/537.36',
    'cookie': '',
    'x-xsrf-token': ''
}


def k8_yjsl(cookie, bark_key):
    headers['cookie'] = cookie
    print(headers)
    k8_resp = requests.get('https://lexiangla.com/gapi/v1/teams?limit=30&page=1&filter=list', headers=headers)
    if check_json(k8_resp.text):
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
                    sl(doc_detail)
    else:
        print("未登录")
        send_bark('登陆信息失效', '[K8]:登陆信息失效, 请重新登陆~', bark_key)


def send_bark(title, content, key):
    requests.get("https://api.day.app/" + key + '/' + title + '/' + content)


def doc_yjsl(cookie, bark_key):
    headers['cookie'] = cookie
    print(headers)
    # 获取全部doc
    doc_resp = requests.get('https://lexiangla.com/api/v1/docs?filter=category&limit=20&page=1&order=-created_at'
                            '&category_id=', headers=headers)
    if check_json(doc_resp.text):
        for doc in doc_resp.json()['data']:
            doc_detail = requests.get(
                'https://lexiangla.com/api/v1/docs/' + doc['id'] + '?lazy_load=1&increment=1',
                headers=headers)
            # 如果点赞和收藏过中断执行
            detail_json = doc_detail.json()
            if detail_json['target']['is_favorited'] and detail_json['target']['is_liked']:
                print(detail_json['name'])
                return
            sl(doc_detail)
    else:
        print("未登录")
        send_bark('登陆信息失效', '[知识库]:登陆信息失效, 请重新登陆~', bark_key)


def check_json(str):
    try:
        json.loads(str)
        return True
    except ValueError:
        return False


def sl(doc_detail):
    doc_detail_resp = doc_detail.json()
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
        items.append(doc_detail_resp['name'])


def fun(config, items):
    cookie = config['cookie']
    bark_key = config['bark_key']
    k8_yjsl(cookie, bark_key)
    doc_yjsl(cookie, bark_key)
    if items:
        send_bark('任务成功', '任务执行完毕 ^_^' + '\n' + '\n'.join(items), bark_key)
    else:
        send_bark('任务成功', '任务执行完毕 ^_^! 没有需要点赞的文章', bark_key)
    return 'success'


if __name__ == '__main__':

    items = []

    configs = json.loads(os.environ['LX_CONFIG'])

    with ThreadPoolExecutor(max_workers=len(configs)) as pool:
        for config in configs:
            task = pool.submit(fun, config, items)


            def get_result(future):
                print(threading.current_thread().name + '运行结果：' + future.result())


            task.add_done_callback(get_result)

    print('线程结束')
