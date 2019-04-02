# 分词
import jieba
from nltk.parse import stanford
import os

string = '他骑自行车去了菜市场。'
seg_list = jieba.cut(string, cut_all=False, HMM=True)  # 使用精确模式进行分词
seg_str = ' '.join(seg_list)  # 将词用空格切分后再重新拼接成字符串。Stanford_parser的输入是分词完后以空格隔开的句子
print(seg_str)

parser_path = 'D:/NLP/stanford_parser/stanford-parser-full-2018-10-17/stanford-parser.jar'  # Stanford-parser的jar包
model_path = 'D:/NLP/stanford_parser/stanford-parser-full-2018-10-17/stanford-parser-3.9.2-models.jar'  # 训练好的模型jar包

# 指定JDK路径
if not os.environ.get('JAVA_HOME'):
    JAVA_HOME = 'C:/Program Files/Java/jdk1.8.0_161'
    os.environ['JAVA_HOME'] = JAVA_HOME

# PCFG模型路径
pcfg_path = 'edu/stanford/nlp/models/lexparser/chinesePCFG.ser.gz'

parser = stanford.StanfordParser(path_to_jar=parser_path, path_to_models_jar=model_path, model_path=pcfg_path)

sentence = parser.raw_parse(seg_str)
for line in sentence:
    print(line)
    line.draw()