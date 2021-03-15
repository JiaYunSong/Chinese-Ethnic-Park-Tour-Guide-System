# -*- coding: UTF-8 -*-
# editor: Li YiMing,JiaYunSong

import threading
import re
import jieba
import numpy as np
import pyttsx3
from sklearn.feature_extraction.text import TfidfVectorizer


class FAQRobot:
    """智能问答机器人"""

    def __init__(self, qtxtPath, atxtPath):
        self.QtxtPath = qtxtPath
        self.AtxtPath = atxtPath

    @staticmethod
    def __readCorpus(filepath) -> list:
        """
        读取相应文件路径的文件(语料资源)

        :param filepath: <str> 文件路径
        :return: <list> 列表，被读取的语料资源
        """
        with open(filepath, 'r', encoding='utf8', errors='ignore') as f:
            corpus = [line.replace('\n', '') for line in f.readlines()]
        return corpus

    @staticmethod
    def __filter(inputText):
        """
        使用正则表达式过滤文本

        :param inputText: <str> 中文文本
        :return: <str> 过滤后的文本，主要替换问题中的数字与字母
        """
        newInput = re.sub('([a-zA-Z0-9])', '', inputText)
        newInput = ''.join(e for e in newInput if e.isalnum())
        return newInput

    @staticmethod
    def __wordSegmentation(inputText):
        """
        使用jieba分词

        :param inputText: <str> 中文文本
        :return: <str> 分词后的文本，以逗号分隔，得到的是独立的汉语词语
        """
        newInput = ','.join(jieba.cut(inputText))
        return newInput

    @staticmethod
    def __preprocessText(text):
        """
        预处理文本，主要对其做过滤和分词。

        :param text: <str> 中文文本
        :return: <str> 预处理后的文本
        """
        newtext = []
        for seq in text:
            seq = FAQRobot.__filter(seq)
            seq = FAQRobot.__wordSegmentation(seq)
            newtext.append(seq)
        return newtext

    @staticmethod
    def __tfidfExtractor(corpus, ngram_range=(1, 1)):
        """
        利用sklearn获得tfidf特征提取器

        :param corpus: 中文语料
        :param ngram_range: n元语法
        :return: <vectorizer, features>TfidfVectorizer的实例化对象, tf-idf稀疏矩阵
        """
        vectorizer = TfidfVectorizer(min_df=1, norm='l2', smooth_idf=True, use_idf=True, ngram_range=ngram_range)
        features = vectorizer.fit_transform(corpus)
        return vectorizer, features

    @staticmethod
    def __conver2tfidf(text):
        """
        封装tfidf

        :param text: 文本信息
        :return: <vectorizer, features> TfidfVectorizer的实例化对象, tf-idf稀疏矩阵
        """
        tfidf_vectorizer, tfidf_X = FAQRobot.__tfidfExtractor(text)
        return tfidf_vectorizer, tfidf_X

    @staticmethod
    def __searchLargestCosineSim(inputText, questions):
        """
        查询输入的问题与问题列表中哪一个问题相似度最高

        :param inputText: 用户所输入的问题
        :param questions: 知识库中的问题列表
        :return: 相似度最高问题的索引
        """
        coses = []
        inputText = (inputText.toarray())[0]
        for question in questions:
            question = question.toarray()
            #计算两个向量的内积
            num = float(np.matmul(question, inputText))
            #计算两个向量二范数的乘积
            denom = np.linalg.norm(question) * np.linalg.norm(inputText)
            #计算余弦相似度
            cos = 0.0 if denom == 0 else num / denom
            coses.append(cos)
        bestidx = coses.index(max(coses))
        return bestidx

    @staticmethod
    def __answerTfidf(inputText, tfidf_vectorizer, tfidf_X, answers):
        """
        将整个匹配流程封装在一起

        :param inputText: 用户输入的问题
        :param tfidf_vectorizer: 在训练文本中训练得到的tfidfVectorize实例化对象
        :param tfidf_X: 在训练文本中训练得到的tfidf矩阵
        :param answers: 回答列表
        :return: 最佳匹配答案
        """
        inputText = FAQRobot.__filter(inputText)
        inputText = FAQRobot.__wordSegmentation(inputText)
        wordvec = tfidf_vectorizer.transform([inputText])
        bestidx = FAQRobot.__searchLargestCosineSim(wordvec, tfidf_X)
        return answers[bestidx]

    def FAQAnswer(self, query):
        """
        问答

        :param query: 用户输入的问题
        :return: 问题答案
        """
        # 加载知识库
        questions = FAQRobot.__readCorpus(self.QtxtPath)
        answers = FAQRobot.__readCorpus(self.AtxtPath)
        # 文本预处理
        qlist = FAQRobot.__preprocessText(questions)
        tfidf_vectorizer, tfidf_X = FAQRobot.__conver2tfidf(qlist)

        Answer = FAQRobot.__answerTfidf(query, tfidf_vectorizer, tfidf_X, answers)

        self.synthesis(Answer)
        return Answer

    def synthesis(self, strText):
        """
        调用内置引擎进行语音合成

        :param strText: 待语音合成的文本
        """
        Speaking(strText)


class Speaking(threading.Thread):
    """窗口后台线程类"""

    def __init__(self, SpeakText):
        super(Speaking, self).__init__()
        self.SpeakText = SpeakText
        self.start()

    def run(self):
        try:
            # 防止预加载 BUG
            import pythoncom
            pythoncom.CoInitialize()

            engine = pyttsx3.init()
            engine.setProperty(
                "voice",
                "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ZH-CN_HUIHUI_11.0"
            )
            engine.say(self.SpeakText)
            engine.runAndWait()
        except Exception as e:
            print(f"语速过快导致pyttsx3懵逼，ERROR：{e}")


if __name__ == '__main__':
    # 测试问答系统
    Robot = FAQRobot('./Q.txt', './A.txt')
    Answer = Robot.FAQAnswer(input("请输入您的问题："))
    print(Answer)
