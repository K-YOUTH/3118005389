# -*- coding: utf-8 -*-
import re
import time
import jieba
import math
from gensim import corpora
from gensim.similarities import Similarity
from collections import defaultdict

# 定义文件目录
'''
work_dir = "C:/Users/youth/Desktop/test"
f1 = work_dir + "/orig.txt"
f3 = work_dir + "/orig_0.8_del.txt"
'''


# 去除标点符号（只留字母、数字、中文)

def removePunctuation(query):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    query = rule.sub('', query)
    return query

# 获取相似度
def get_sim(f1, f2):
    c1 = open(f1, encoding='utf8').read()
    c1 = removePunctuation(c1)
    print(c1)
    # jieba 进行分词
    data1 = jieba.cut(c1)
    data11 = ""
    # 获取分词内容
    for i in data1:
        data11 += i + " "
    doc1 = [data11]
    # 检验分词，程序成功可去掉
    print("分词内容:\n")
    print(doc1)

    t1 = [[word for word in doc.split()]
          for doc in doc1]
    # print(t1)

    #  frequence频率
    freq = defaultdict(int)
    for i in t1:
        for j in i:
            freq[j] += 1
    # print(freq)

    # 限制词频
    '''t2 = [[token for token in k if freq[j] >= 3]
        for k in t1]
    '''

    # corpora语料库建立字典

    dic1 = corpora.Dictionary(t1)

    # 对比文件
    c2 = open(f2, encoding='utf8').read()
    c2 = removePunctuation(c2)

    # jieba 进行分词
    data2 = jieba.cut(c2)
    data21 = ""
    for i in data2:
        data21 += i + " "
    new_doc = data21
    # print(new_doc)
    # doc2bow把文件变成一个稀疏向量
    new_vec = dic1.doc2bow(new_doc.split())
    # 对字典进行doc2bow处理，得到新语料库
    new_corpor = [dic1.doc2bow(t3) for t3 in t1]
    # 特征数
    featurenum = len(dic1.token2id)
    # SparseMatrixSimilarity 稀疏矩阵相似度
    idx = Similarity('-Similarity-index', new_corpor, featurenum)
    sims = idx[new_corpor]
    f = open(r'/output.txt', 'w')
    print('%.2f' % sims, file=f)
    f.close()
    print('%.2f' % sims)


if __name__ == '__main__':
    # 工作路径为桌面
    work_dir = "//"
    print("工作路径为桌面，请输入原文本文件名：\n")
    f1 = ""
    f2 = ""
    f1 = input(f1)
    f3 = work_dir + f1
    print("请输入第二个文本文件名：\n")
    f2 = input(f2)
    f4 = work_dir + f2
    start = time.time()
    get_sim(f3, f4)
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
