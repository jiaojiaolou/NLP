from HMM import HMM

hmm = HMM()
hmm.train('D:/NLP/nlp_ex/HMM/trainCorpus.txt_utf8')  # 采用人民日报的分词语料

text = '经过你的阐述，这是一个非常棒的方案！'
res = hmm.cut(text)
print(text)
print(str(list(res)))
