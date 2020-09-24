mian.py为目前的最终版，后续有改进会继续添加新版本文件.

test.py为第一版，mian2.py为第二版。


* 题目要求
* 查阅资料
* 模块接口的设计与实现过程
* 模块接口部分的性能改进
* 单元测试展示
* 异常处理
* PSP表格
* 参考资料


**题目要求**
> 设计一个论文查重算法，给出一个原文文件和一个在这份原文上经过了增删改的抄袭版论文的文件，在答案文件中输出其重复率。
> 原文示例：今天是星期天，天气晴，今天晚上我要去看电影。
> 抄袭版示例：今天是周天，天气晴朗，我晚上要去看电影。
> 要求输入输出采用文件输入输出，规范如下：
> 从命令行参数给出：论文原文的文件的绝对路径。
> 从命令行参数给出：抄袭版论文的文件的绝对路径。
> 从命令行参数给出：输出的答案文件的绝对路径。
> 我们提供一份样例，课堂上下发，上传到班级群，使用方法是：orig.txt是原文，其他orig_add.txt等均为抄袭版论文。

**查阅资料**

方法：利用余弦定理求相似度，语言使用python
具体步骤：

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924165928715-2004128955.png)


**模块接口的设计与实现过程**

removePunctuation函数：对标点符号过滤，只剩下数字，中文，英文

```
def removePunctuation(text):
    query = []
    for s in text:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", s)):
            query.append(s)
    return query

```
get_sim函数：jieba分词,将文本转化为稀疏向量，得出相似度
```  
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
```
**总的代码：**

```
# -*- coding: utf-8 -*-
import re
import time
import jieba
import gensim
'''
# 仅去常见标点
def removePunctuation(text):
    text = [i for i in text if i not in (' ',',','.','。','?','？','!','！','')]
    return text
'''
'''
def removePunctuation(query):
    rule = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    query = rule.sub('', query)
    return query
'''
# 去除标点、符号（只留字母、数字、中文)
def removePunctuation(text):
    query = []
    for s in text:
        if (re.match(u"[a-zA-Z0-9\u4e00-\u9fa5]", s)):
            query.append(s)
    return query

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
    
    path1 = "C:/Users/youth/Desktop/test//orig.txt"
    path2 = "C:/Users/youth/Desktop/test/orig_0.8_dis_1.txt"
    '''
    #现实使用中可将固定路径改为以下模块，更改工作路径
    #工作路径为桌面
    #work_dir = "C:/Users/youth/Desktop/test/"
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
```

**模块接口部分的性能改进**

原采用jieba.cut进行分词，分词后需要将利用for循环分词结果转换为列表；
改成jieba.lcut进行分词，直接将分词结果转为列表。
（main2.py采用jieba.cut进行分词，main.py改成jieba.lcut进行分词，文件见github仓库）
**单元测试**

性能分析：

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924085832559-596849533.png)
代码覆盖率：

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924085927314-542718455.png)

测试：

文本路径：

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924173817855-93163746.png)

答案文件路径：

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924173833921-415811023.png)

orig.txt 、orig_0.8_add.txt

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924170528470-1800579928.png)

orig.txt 、orig_0.8_del.txt

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924170535233-1291066001.png)

orig.txt 、orig_0.8_dis_1.txt

![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924170540458-1181158636.png)

如果采用以下去除标点（仅去常见标点）的函数，相识度会降低，原因是英文连符'-'。（orig.txt 、orig_0.8_dis_1.txt）
```
def removePunctuation(text):
    text = [i for i in text if i not in (' ',',','.','。','?','？','!','！','')]
    return text
```
![](https://img2020.cnblogs.com/blog/2005170/202009/2005170-20200924170600214-370544179.png)


**异常处理**

   ```
 print("工作路径为桌面，请输入原文本文件名：\n")
    path1_1 = ""
    path2_1 = ""
    path1_1  = input(path1_1)
    path1 = work_dir + path1_1 
    print("请输入第二个文本文件名：\n")
    path2_1 = input(path2_1)
    path2 = work_dir + path2_1
```
采用以上代码，若输入的文件名错误，程序异常。

**参考资料**

[https://blog.csdn.net/Nonoroya_Zoro/article/details/80342532](文本相似度1)
[https://titanwolf.org/Network/Articles/Article?AID=26627f5e-1ce9-40cb-a091-b771ae91d69d](文本相似度3)
[https://www.cnblogs.com/airnew/p/9563703.html](文本相似度4)
[https://blog.csdn.net/qq236237606/article/details/107815605](去除标点符号)
[https://www.bilibili.com/video/BV1SQ4y1A739?t=1510]()
