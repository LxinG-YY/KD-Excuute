# from racker.core import Base
import json
import pandas as pd
import numpy as np
import time
import datetime


class example2(object):
    def run(self, para):
        print(para)
        dates = pd.date_range('20130101 15:36', periods=6)
        df1 = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list('ABCD'))
        # print("Test for df1:")
        # print(df1)
        dates = pd.bdate_range('20130201', periods=5)
        df2 = pd.DataFrame(np.random.randn(5, 5), index=dates, columns=list('ABCDE'))
        dates = ['2017-06-20', '2017-06-23', '2017-06-24', '2017-06-25', '2017-06-26', '27/06/2018 16:02']
        df3 = pd.DataFrame(np.random.randn(6, 5), index=pd.to_datetime(dates), columns=list('ABCDE'))
        # zz_dict = ({'data': df1.to_json(), 'title': [1, 2, 3]}, {'data': (1, 2, 3)})
        # return json.dumps(zz_dict)
        current_time1 = datetime.datetime.today()
        current_time2 = time.localtime()
        current_time3 = pd.to_datetime('2017-06-20')
        current_time4 = pd.datetime.today()
        current_time5 = datetime.date.today()
        current_time6 = datetime.time(16, 24, 2)
        time_info = [current_time1, current_time2, current_time3, current_time4, current_time5, current_time6]
        time_info1 = [current_time1] * 6
        time_info2 = [current_time2] * 6
        time_info3 = [current_time3] * 6
        time_info4 = [current_time4] * 6
        time_info5 = [current_time5] * 5
        time_info6 = [current_time6] * 5
        df1['A'] = time_info1
        df1['B'] = time_info2
        df1['C'] = time_info3
        df1['D'] = time_info4
        df2['A'] = time_info5
        df2['B'] = time_info6
        df3['A'] = time_info
        df3['B'] = [None] * 6
        df3['C'] = [np.NaN] * 6
        # zz_dict = ({'data': df1, 'title': 'Test1', 'number': 12, 'placeholder1': ['a', 'b', 1, 2]},
        #            {'data': df2, 'name': 'Test2', 'result': 121111111111111111111, 'placeholder2': ['c', 'd', 3, 4]},
        #            {'data': df3, 'name': 'Test2', 'result': 12.123, 'placeholder3': ['c', 'd', 3, 4]}
        #            )
        # return zz_dict
        test1 = ({'data': df1})
        return test1


# class ComplexEncoder(json.JSONEncoder):
#     """
#     处理datetime格式的日期无法直接JSON化的问题
#     """
#     def default(self, obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.strftime('%Y-%m-%d %H:%M:%S')
#         elif isinstance(obj, datetime.date):
#             return obj.strftime('%Y-%m-%d')
#         elif isinstance(obj, datetime.time):
#             return obj.strftime('%H:%M:%S')
#         else:
#             return json.JSONEncoder.default(self, obj)
def parse_time_type(obj):
    """
    为了保证数据串可以正常进行JSON化需要对其中的时间格式的数据进行处理
    并记录下其时间类型方便接下来将时间数据转化回来
    :param obj: 待处理的时间类型
    :return: 处理后的时间类型 和 一个表示时间类型的字符串
    """
    if isinstance(obj, pd._libs.tslibs.timestamps.Timestamp):
        # return obj.strftime('%Y-%m-%d %H:%M:%S'), 'Timestamp'
        return obj.to_pydatetime().timestamp(), 'Timestamp'

    elif isinstance(obj, datetime.datetime):
        return obj.timestamp(), 'datetime'

    elif isinstance(obj, datetime.date):
        time_structure = datetime.date.timetuple(obj)
        return time.mktime(time_structure), 'date'

    elif isinstance(obj, datetime.time):
        return obj.strftime('%H:%M:%S'), 'time'

    elif isinstance(obj, time.struct_time):
        return time.mktime(obj), 'struct_time'

    elif obj is None:
        return obj, 'None'

    else:
        return obj, 'other_type'


a = example2()
a = a.run({'a': '1', 'b': '2'})
# print(a)
if isinstance(a, dict):
    item = a
    data_type = []
    for i in range(len(item['data'].columns)):
        item['data'].columns.values[i], tmp_type = parse_time_type(item['data'].columns.values[i])
        if i == 0:
            data_type.append(tmp_type)
        elif data_type[0] != 'other_type':
            if tmp_type != data_type[0]:
                data_type[0] = 'other_type'

    # 处理index数据，如果数据类型相同则记录类型并进行恢复否则只转换不记录类型
    index_update = ['0'] * len(item['data'].index)
    for i in range(len(item['data'].index)):
        index_update[i], tmp_type = parse_time_type(item['data'].index[i])
        if i == 0:
            data_type.append(tmp_type)
        elif data_type[1] != 'other_type':
            if tmp_type != data_type[1]:
                data_type[1] = 'other_type'
    if data_type[1] != 'Timestamp':
        item['data'].index = index_update

    # 按列处理values数据，如果数据类型相同则记录类型并进行恢复否则只转换不记录类型
    for i in range(len(item['data'].columns)):
        for j in range(len(item['data'].index)):
            item['data'].loc[item['data'].index[j], item['data'].columns[i]], tmp_type = \
                parse_time_type(item['data'].loc[item['data'].index[j], item['data'].columns[i]])
            if j == 0:
                data_type.append(tmp_type)
            elif data_type[i+2] != 'other_type':
                if tmp_type != data_type[i+2]:
                    data_type[i+2] = 'other_type'

    # result_type.append(data_type)
    item['data'] = item['data'].to_json(orient='split')
    item['data_type'] = data_type
else:
    for item in a:
        data_type = []
        # 处理columns数据，如果数据类型相同则记录类型并进行恢复否则只转换不记录类型
        for i in range(len(item['data'].columns)):
            item['data'].columns.values[i], tmp_type = parse_time_type(item['data'].columns.values[i])
            if i == 0:
                data_type.append(tmp_type)
            elif data_type[0] != 'other_type':
                if tmp_type != data_type[0]:
                    data_type[0] = 'other_type'

        # 处理index数据，如果数据类型相同则记录类型并进行恢复否则只转换不记录类型
        index_update = ['0'] * len(item['data'].index)
        for i in range(len(item['data'].index)):
            index_update[i], tmp_type = parse_time_type(item['data'].index[i])
            if i == 0:
                data_type.append(tmp_type)
            elif data_type[1] != 'other_type':
                if tmp_type != data_type[1]:
                    data_type[1] = 'other_type'
        if data_type[1] != 'Timestamp':
            item['data'].index = index_update

        # 按列处理values数据，如果数据类型相同则记录类型并进行恢复否则只转换不记录类型
        for i in range(len(item['data'].columns)):
            for j in range(len(item['data'].index)):
                item['data'].loc[item['data'].index[j], item['data'].columns[i]], tmp_type = \
                    parse_time_type(item['data'].loc[item['data'].index[j], item['data'].columns[i]])
                if j == 0:
                    data_type.append(tmp_type)
                elif data_type[i+2] != 'other_type':
                    if tmp_type != data_type[i+2]:
                        data_type[i+2] = 'other_type'

        # result_type.append(data_type)
        item['data'] = item['data'].to_json(orient='split')
        item['data_type'] = data_type
# '''
# result_type:记录原数据中每一项的数据格式，方便后期进行转换
# index：原数据中字典结构的数据下标
# '''
# result_type = []
# index = 0
# for item in a:
#     result_type.append({})
#     for key in item:
#         if isinstance(item[key], pd.core.frame.DataFrame):
#             # 初始化记录DataFrame的list
#             result_type[index][key] = []
#
#             # 处理DataFrame.values数据并记录其对应数据类型
#             # data_values = item[key].values
#             data_type = []
#             # print(type(item[key]))
#             for i in range(len(item[key].values)):
#                 tmp = ['0'] * len(item[key].values[i])
#                 for j in range(len(item[key].values[i])):
#                     tmp_value, tmp[j] = parse_time_type(item[key].loc[item[key].index[i], item[key].columns[j]])
#                     item[key].loc[item[key].index[i], item[key].columns[j]] = tmp_value
#                 data_type.append(tmp)
#             result_type[index][key].append(data_type)
#
#             # 处理DataFrame.columns数据并记录其对应数据类型
#             columns_values = item[key].columns.values
#             columns_type = ['0'] * len(columns_values)
#             for i in range(len(columns_values)):
#                 columns_values[i], columns_type[i] = parse_time_type(columns_values[i])
#             result_type[index][key].append(columns_type)
#
#             # 处理DataFrame.index数据并记录其对应数据类型
#             index_values = item[key].index.values
#             index_update = ['0'] * len(index_values)
#             index_type = ['0'] * len(index_values)
#             for i in range(len(index_values)):
#                 index_update[i], index_type[i] = parse_time_type(index_values[i])
#             item[key].index = index_update
#             result_type[index][key].append(index_type)
#
#             item[key] = item[key].to_json(orient='split')
#
#         elif isinstance(item[key], list):
#             result_type[index][key] = ['0'] * len(item[key])
#             for i in range(len(item[key])):
#                 item[key][i], result_type[index][key][i] = parse_time_type(item[key][i])
#
#         else:
#             item[key], result_type[index][key] = parse_time_type(item[key])
#
#     index += 1

b = json.dumps(a)

with open('exampleText.txt', 'w+') as f:
    f.write(b)
# # with open('exampleText.txt', 'r+') as f:
#     x = f.read()
#     print(x)

# c = json.loads(b)
# for item in c:
#     item['data'] = pd.read_json(item['data'])
#     for key in item:
#         print(key + ':')
#         print(item[key])

