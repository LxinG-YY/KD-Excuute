import json
import pandas as pd
import requests
import datetime
import time


def decode_time_type(obj, string):
    """
    对racker中获取的JSON串内容进行解析
    还原成源字符串
    :param obj: JSON化后的数据类型
    :return: 返回JSON化之前的原字符串
    """
    if string == 'Timestamp':
        return datetime.datetime.fromtimestamp(obj)

    elif string == 'datetime':
        return datetime.datetime.fromtimestamp(obj)

    elif string == 'date':
        return datetime.date.fromtimestamp(obj)

    elif string == 'time':
        return datetime.time(int(obj[0:2]), int(obj[3:5]), int(obj[6:]))

    elif string == 'struct_time':
        return time.localtime(obj)

    elif string == 'None':
        return None

    elif string == 'other_type':
        return obj


def get_origin_data(url):
    """

    :param url: url是调用resful接口获取json数据的地址，因为在本机测试所以调用的是localhost:5000
    :return: 返回获取json数据解析后的tuple
    """
    s = requests.get(url)
    s = s.json()
    a = json.loads(s)
    if isinstance(a, dict):
        a = [a]

    for item in a:
        item['data'] = pd.read_json(item['data'], orient='split')
        for i in range(len(item['data'].columns)):
            item['data'].columns.values[i] = decode_time_type(item['data'].columns.values[i], item['data_type'][0])

        index_update = ['0'] * len(item['data'].index)
        for i in range(len(item['data'].index)):
            if item['data_type'][1] != 'Timestamp':
                index_update[i] = decode_time_type(item['data'].index[i], item['data_type'][1])
                item['data'].index = index_update

        for i in range(len(item['data'].columns)):
            tmp = ['0'] * len(item['data'].index)
            for j in range(len(item['data'].index)):
                tmp[j] = decode_time_type(item['data'].loc[item['data'].index[j], item['data'].columns[i]],
                                          item['data_type'][i+2])
            item['data'][item['data'].columns[i]] = tmp
        del item['data_type']

    a = tuple(a)
    return a


if __name__ == '__main__':
    url = 'http://localhost:5000/racker/example2/%7B%7D'
    a = get_origin_data(url)
