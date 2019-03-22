# -*- coding: utf-8 -*
import operator

'''
正向与反向结合
'''

# 正向
class MM(object):
    def __init__(self):
        self.window_size = 3


    def cut(self, text):
        result1 = []
        index = 0
        text_length = len(text)
        dic = ['研究', '研究生', '生命', '命', '的', '起源']
        while text_length > index:
            for size in range(self.window_size+index, index, -1):  # 3,0,1
                piece = text[index:size]
                if piece in dic:
                    index = size-1
                    break  # 打破最小封闭的for或者while循环
            index += 1
            result1.append(piece+'---')
        return result1


# 逆向
class RMM(object):
    def __init__(self):
        self.window_size = 3


    def cut(self, text):
        result2 = []
        index = len(text)
        dic = ['研究', '研究生', '生命', '命', '的', '起源']
        while index > 0:
            for size in range(index-self.window_size, index):
                piece = text[size:index]
                if piece in dic:
                    index = size+1
                    break  # 打破最小封闭的for或者while循环
            index -= 1
            result2.append(piece+'---')
        result2.reverse()
        return result2


if __name__ == '__main__':
    text = '研究生命的起源'
    tokenizer1 = MM()
    tokenizer2 = RMM()
    result_MM = tokenizer1.cut(text)
    result_RMM = tokenizer2.cut(text)
    len_MM = len(result_MM)
    len_RMM = len(result_RMM)
    if len_MM != len_RMM:  # 正反向词数不同
        if len_MM < len_RMM:
            result = result_MM
        else:
            result = result_RMM
    else:  # 分词结果数相同
        if operator.eq(result_MM, result_RMM):  # 两个分词结果相同
            result = result_MM  # 返回任意一个
        else:  # 分词结果不同，返回单个字数较少的那个
            min_MM = (x for x in result_MM if len(x) == 4)  # 返回MM中的单个字
            min_RMM = (x for x in result_RMM if len(x) == 4)  # 返回RMM中的单个字
            min_len_MM = len(list(min_MM))
            min_len_RMM = len(list(min_RMM))
            if min_len_MM > min_len_RMM:
                result = result_RMM
            else:
                result = result_MM
    print(result)



