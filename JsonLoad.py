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



def parse_item(x, dtype):
    """
    根据dtype类型对传递过来的x进行处理
    以if的形式可以保证以后对其他类型的扩展
    :param x: 每个Series中待处理的数据
    :param dtype: 当前列的数据结构
    :return: 返回x处理过的数值
    """
    if dtype == 'datetime64[ns]':
        # 即对应数据结构为Timestamp
        x = datetime.datetime.fromtimestamp(x)
    else:
        pass
    return x



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

    json_load = json.loads(s)
    if isinstance(json_load, dict):
        json_load = [json_load]

    # for item in a:
    #     item['data'] = pd.read_json(item['data'], orient='split')
    #     for i in range(len(item['data'].columns)):
    #         item['data'].columns.values[i] = decode_time_type(item['data'].columns.values[i], item['data_type'][0])
    #
    #     index_update = ['0'] * len(item['data'].index)
    #     for i in range(len(item['data'].index)):
    #         if item['data_type'][1] != 'Timestamp':
    #             index_update[i] = decode_time_type(item['data'].index[i], item['data_type'][1])
    #             item['data'].index = index_update
    #
    #     for i in range(len(item['data'].columns)):
    #         tmp = ['0'] * len(item['data'].index)
    #         for j in range(len(item['data'].index)):
    #             tmp[j] = decode_time_type(item['data'].loc[item['data'].index[j], item['data'].columns[i]],
    #                                       item['data_type'][i+2])
    #         item['data'][item['data'].columns[i]] = tmp
    #     del item['data_type']
    for item in json_load:
        item['data'] = pd.read_json(item['data'], orient='split', convert_dates=False)
        df = item['data']

        # 处理index数据
        # dtype = item['data_type'][0]
        # if dtype == 'datetime64[ns]':
        #     tmp = pd.Series(df.index)
        #     df.index = tmp.apply(parse_item, dtype=dtype)

        # 处理columns数据
        dtype = item['data_type'][1]
        if dtype == 'datetime64[ns]':
            tmp = pd.Series(df.columns)
            df.columns = tmp.apply(parse_item, dtype=dtype)

        # 处理vlues数据
        for i in range(len(df.columns)):
            dtype = item['data_type'][i+2]
            if dtype == 'datetime64[ns]':
                df.iloc[:, i] = df.iloc[:, i].apply(parse_item, dtype=dtype)

        del item['data_type']
    json_load = tuple(json_load)
    return json_load


if __name__ == '__main__':
    url = 'http://localhost:5000/racker/example2/%7B%7D'
    a = get_origin_data(url)
    print(a)

