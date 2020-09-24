# -*- coding: utf-8 -*-
import re
import time
import jieba
import gensim

# 仅去常见标点
def removePunctuation(text):
    text = [i for i in text if i not in (' ',',','.','。','?','？','!','！','')]
    return text

'''
def removePunctuation(query):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    query = rule.sub('', query)
    return query
'''
# 去除标点、符号（只留字母、数字、中文)
'''
def removePunctuation(text):
    query = []
    for s in text:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", s)):
            query.append(s)
    return query
'''
def get_sim(path1,path2):
    text1 = open(path1, encoding='utf8').read()
    text2 = open(path2, encoding='utf8').read()
    # jieba 进行分词
    text_cut1 = jieba.lcut(text1)
    text_cut1 = removePunctuation(text_cut1)
    # 去除标点符号（只留字母、数字、中文)
    text_cut2 = jieba.lcut(text2)
    text_cut2 = removePunctuation(text_cut2)
    text_cut =  [text_cut1,text_cut2]
    # 检验分词内容，成功后可去掉
    print(text_cut)
    #corpora语料库建立字典
    dictionary = gensim.corpora.Dictionary(text_cut)
    # 对字典进行doc2bow处理，得到新语料库
    new_dictionary = [dictionary.doc2bow(text) for text in text_cut]
    num_features = len(dictionary)# 特征数
    # SparseMatrixSimilarity 稀疏矩阵相似度
    similarity = gensim.similarities.Similarity('-Similarity-index', new_dictionary, num_features)
    text_doc = dictionary.doc2bow(text_cut1)
    sim = similarity[text_doc][1]
    f = open(r'C:/Users/youth/Desktop/test/output.txt', 'w')
    print('%.2f' % sim, file=f)
    print('文本相似度： %.2f'% sim)

if __name__ == '__main__':
    # 工作路径为桌面
    #work_dir = "C:/Users/youth/Desktop/test/"
    path1 = "C:/Users/youth/Desktop/test//orig.txt"
    path2 = "C:/Users/youth/Desktop/test/orig_0.8_dis_1.txt"
    '''
    #现实使用中可将固定路径改为以下模块，更改工作
    print("工作路径为桌面，请输入原文本文件名：\n")
    path1_1 = ""
    path2_1 = ""
    path1_1  = input(path1_1)
    path1 = work_dir + path1_1 
    print("请输入第二个文本文件名：\n")
    path2_1 = input(path2_1)
    path2 = work_dir + path2_1
    '''
    start = time.time()
    get_sim(path1, path2)
    end = time.time()
    print('运行时间: %s 秒' % (end - start))

