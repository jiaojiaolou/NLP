import jieba

'''
使用Jieba进行高频词的提取，
数据在data/news中，有9个目录，均为txt文件，
分别代表不同领域的新闻。
'''
def get_content(path):
    '''
    数据读取
    :param path:
    :return:
    '''
    with open(path, 'r', encoding='gbk', errors='ignore') as f:
        content = ''
        for l in f:
            l = l.strip()  # 用于移除字符串头尾指定的字符（空格或换行符）或字符序列
            content += l
        return content


def get_TF(words, topK):
    '''
    高频词统计的函数
    :param words: 一个词的词组
    :param topK: 获取出现频率次数最多的前top
    :return:
    '''
    tf_dic = {}
    for w in words:
        tf_dic[w] = tf_dic.get(w, 0) + 1  # get返回指定键的值，若键不存在，返回默认值0
    return sorted(tf_dic.items(), key=lambda x: x[1], reverse=True)[:topK]  # 降序


def stop_words(path):
    '''
    停用词，过滤无意义的词
    :param path:
    :return:
    '''
    with open(path, encoding='UTF-8') as f:
        return [l.strip() for l in f]


def main():
    import glob
    import random
    import jieba

    files = glob.glob('D:/NLP/nlp_ex/jieba_fre_word/data/news/C000008/*.txt')  # glob返回所有匹配的文件路径列表
    corpus = [get_content(x) for x in files]

    sample_inx = random.randint(0, len(corpus))  # 从0到len中随机返回一个整数
    # split_words = list(jieba.cut(corpus[sample_inx]))  # 分词
    split_words = [x for x in jieba.cut(corpus[sample_inx]) if x not in stop_words('D:/NLP/nlp_ex/jieba_fre_word/data/stop_words.utf8')]
    print('样本之一：' + corpus[sample_inx])
    print('样本分词效果：'+'/'.join(split_words))
    print('样本出现频率前topk的词：' + str(get_TF(split_words, 10)))

main()