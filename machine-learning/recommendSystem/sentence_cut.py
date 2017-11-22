import jieba.analyse


def get_tags(sentence):
    return jieba.analyse.extract_tags(sentence, topK=50, withWeight=True)
