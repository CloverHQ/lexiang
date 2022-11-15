#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-10-30 20:30
# @Author  : liuwenchao
# @File    : record
# @Software: IntelliJ IDEA
import json
import random
import time

import openpyxl
from tqdm import tqdm


def get_data_batch(file_name):
    workbook = openpyxl.load_workbook(file_name, data_only=True)
    # 获取指定的sheet页对象
    sheet = workbook["Sheet1"]
    rows = sheet.rows
    list = []
    for row in rows:
        record = {
            "carNo": None,
            "date": None,
            "addr": None
        }

        for data in row[1:11]:
            if data.row < 4 or data.column > 11:
                continue
            if data.column == 2:
                record["date"] = str(data.value)
                continue
            if data.column == 4:
                record["carNo"] = data.value
                continue
            if data.column == 5 and record["carNo"] is None:
                record["carNo"] = data.value
                continue
            if data.column == 11:
                record["addr"] = data.value
                continue
        if record["carNo"] is not None:
            list.append(record)
    return list


def created_excel(header, data):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Sheet1"
    # 添加表头（不需要表头可以不用加）
    data.insert(0, list(header))
    # 开始遍历数组
    for row_index, row_item in enumerate(data):

        for col_index, col_item in enumerate(row_item):
            # 写入
            sheet.cell(row=row_index + 1, column=col_index + 1, value=col_item)

    # 写入excel文件 如果path路径的文件不存在那么就会自动创建
    workbook.save('记录.xlsx')


if __name__ == "__main__":

    str1 = '██    ██  █████   ██████'
    str2 = ' ██  ██  ██   ██ ██    ██'
    str3 = '  ████   ███████ ██    ██'
    str4 = '   ██    ██   ██ ██    ██'
    str5 = '   ██    ██   ██  ██████'
    # 获取数据
    print(str1)
    print(str2)
    print(str3)
    print(str4)
    print(str5)
    file_name = input('请输入文件名称  (°ー°〃) \r\n')
    before = time.time()
    print('正在解析请稍后....')
    records = get_data_batch(file_name)
    print("解析完成，正在生成新的Excel数据表...")
    header = ['日期/出站时间', '车号', '核定载质量', '出厂站核载质量', '驾驶员姓名', '联系方式', '送达/采购地址']

    data = []

    not_exists = []

    with open("info.json", encoding='utf-8') as fw:
        infos = json.load(fw)
        for record in tqdm(records, desc="生成进度"):
            for info in infos:
                if info['carNo'].strip() == record['carNo'].strip():
                    mass = int(info['ratedLoadingMass'][:-2])

                    result = [record['date'], info['carNo'], info['ratedLoadingMass'],
                              str(round(random.randint(mass - 3000, mass - 1000), -1)) + 'kg', info['name'],
                              info['contact'],
                              record['addr']]
                    data.append(result)
        not_exists = set(list(map(lambda x: x['carNo'].strip(), records))) - set(
            list(map(lambda x: x['carNo'].strip(), infos)))

        created_excel(header, data)
        fileName = 'notebook.txt'
        with open(fileName, 'w', encoding='utf-8')as file:
            file.writelines([line + '\n' for line in not_exists])
        print('[Mission Accomplished] 用时: %s  感谢使用！(￣_,￣ )' % str(time.time() - before))
