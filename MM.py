# -*- coding: utf-8 -*

class MM(object):
    '''
    正向
    '''
    def __init__(self):
        self.window_size = 3


    def cut(self, text):
        result = []
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
            result.append(piece+'---')
        print(result)


if __name__ == '__main__':
    text = '研究生命的起源'
    tokenizer = MM()
    print(tokenizer.cut(text))