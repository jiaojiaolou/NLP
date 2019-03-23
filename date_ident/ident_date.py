# -*- coding: utf-8 -*-

'''
日期识别
针对预定系统
'''

import re
from datetime import datetime, timedelta
from dateutil.parser import parser
import jieba.posseg as psg

UTIL_CN_NUM = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}

UTIL_CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}

def cn2dig(src):
    '''
    将具体的文本转换成相应的数字
    :param src:
    :return:
    '''
    if src == "":
        return None
    m = re.match("\d+", src)
    if m:
        return int(m.group(0))
    rsl = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            rsl += num * unit
        else:
            return None
    if rsl < unit:
        rsl += unit
    return rsl

def year2dig(year):
    '''
    将具体的文本转换成相应的数字
    :param year:
    :return:
    '''
    res = ''
    for item in year:
        if item in UTIL_CN_NUM.keys():
            res = res + str(UTIL_CN_NUM[item])
        else:
            res = res + item
    m = re.match("\d+", res)
    if m:
        if len(m.group(0)) == 2:
            return int(datetime.datetime.today().year/100)*100 + int(m.group(0))
        else:
            return int(m.group(0))
    else:
        return None

def parse_datetime(msg):
    '''
    将每个提取到的文本日期串进行时间转换，
    用正则表达式将日期串进行切割，然后针对每个
    子维度单独进行识别
    :param msg:
    :return:
    '''
    # print('msg:', msg)
    if msg is None or len(msg) == 0:
        return None

    try:
        dt = parser(msg, fuzzy=True)  # parse是根据字符串解析成datetime
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        '''
        用于处理阿拉伯数字与汉字混杂的日期串的提取，
        还加入了早中晚上下的考虑，调整输出的时间格式
        '''
        m = re.match(
        r"([0-9零一二两三四五六七八九十]+年)?([0-9一二两三四五六七八九十]+月)?([0-9一二两三四五六七八九十]+[号日])?([上中下午晚早]+)?([0-9零一二两三四五六七八九十百]+[点:.\时])?([0-9零一二三四五六七八九十百]+分?)?([0-9零一二三四五六七八九十百]+秒)?",
             msg)
    # print('m.group:', m.group(0), m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
    if m.group(0) is not None:
        res = {
            "year": m.group(1),
            "month": m.group(2),
            "day": m.group(3),
            "noon":m.group(4),  # 上中下午晚早
            "hour": m.group(5) if m.group(5) is not None else '00',
            "minute": m.group(6) if m.group(6) is not None else '00',
            "second": m.group(7) if m.group(7) is not None else '00',
        }
        params = {}
        for name in res:
            if res[name] is not None and len(res[name]) != 0:
                tmp = None
                if name == 'year':
                    tmp = year2dig(res[name][:-1])
                else:
                    tmp = cn2dig(res[name][:-1])
                if tmp is not None:
                    params[name] = int(tmp)
        target_date = datetime.today().replace(**params)
        print('target_date:', target_date)
        is_pm = m.group(4)
        if is_pm is not None:
            if is_pm == u'下午' or is_pm == u'晚上' or is_pm =='中午':
                hour = target_date.time().hour
                if hour < 12:
                    target_date = target_date.replace(hour=hour + 12)
        return target_date.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None


def check_time_valid(word):
    '''
    #对提取出的拼接日期串进行进一步的处理，进行有效性判断
    :param word:
    :return:
    '''
    # print('check:', word)
    m = re.match("\d+$", word)  # \d表数字，+表至少出现一次，$行结尾
    if m:
        if len(word) <= 6:
            return None
    word1 = re.sub('[号|日]\d+$', '日', word)  # 将word中所有的“号”或“日”都替换成“日“
    # print('word1:', word1)
    if word1 != word:
        return check_time_valid(word1)
    else:
        return word1


def time_extract(text):
    '''
    将带有时间信息的词进行切分，
    记录连续时间信息的词，用Jieba，
    提取其中"m"(数字)"t"(时间)词性的词，
    并进行上下文拼接。
    :param text:
    :return:
    '''
    time_res = []
    word = ''
    keyDate = {'今天': 0, '明天': 1, '后天': 2}
    for k, v in psg.cut(text):
        print(k, v)
        if k in keyDate:
            if word != '':
                time_res.append(word)
            # 日期的转换，timedelta提取任意延迟天数的信息
            word = (datetime.today() + timedelta(days=keyDate.get(k, 0))).\
                      strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')

        elif word != '':
            if v in ['m', 't']:
                word = word + k
            else:
                time_res.append(word)
                word = ''
        elif v in ['m', 't']:  # m:数字 t:时间
            word = k
    # print('word:', word)
    if word != '':
        time_res.append(word)
    # print('time_res:', time_res)
    # filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
    result = list(filter(lambda x: x is not None, [check_time_valid(w) for w in time_res]))
    # print('result:', result)
    final_res = [parse_datetime(w) for w in result]
    # print('final_res:', final_res)
    return [x for x in final_res if x is not None]


text1 = '我要住到明天下午三点'
print(text1, time_extract(text1), sep=':')

#
# text2 = '预定28号的房间'
# print(text2, time_extract(text2), sep=':')
#
# text3 = '我要从26号下午4点住到11月2号'
# print(text3, time_extract(text3), sep=':')
#
#
# text5 = '今天30号呵呵'
# print(text5, time_extract(text5), sep=':')
#
# text4 = '我要预订今天到30的房间'
# print(text4, time_extract(text4), sep=':')

