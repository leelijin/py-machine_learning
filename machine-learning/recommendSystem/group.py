import codecs

import requests
import jieba
import jieba.analyse
import pprint


class GroupArticle:
    api_url = 'http://127.0.0.1:88/api/articles/50'

    def __init__(self):
        pass

    @staticmethod
    def _get_tags(sentence):
        return jieba.analyse.extract_tags(sentence, topK=10)
        punct = set(u''':!),.:;?]}¢'"、。〉》」』】〕〗〞︰︱︳﹐､﹒
        ﹔﹕﹖﹗﹚﹜﹞！），．：；？｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
        々‖•·ˇˉ―--′’”([{£¥'"‵〈《「『【〔〖（［｛￡￥〝︵︷︹︻
        ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
        tags = jieba.cut(sentence)
        return [tag for tag in tags if tag not in punct and not tag.isdigit()]

    def _get_remote_contents(self):
        return requests.get(self.api_url).json()

    def get_word_count(self, content):
        wordcount = {}
        tags = self._get_tags(content['title'] + content['content'])
        for tag in tags:
            wordcount.setdefault(tag, 0)
            wordcount[tag] = wordcount[tag] + 1

        return content['title'], wordcount

    def set_article_txt(self):
        contents = self._get_remote_contents()
        article_count = {}
        wordcounts = {}
        for content in contents:
            title, wordcount = self.get_word_count(content)
            wordcounts[title] = wordcount
            for word, count in wordcount.items():
                article_count.setdefault(word, 0)
                if count > 1:
                    article_count[word] = int(article_count[word]) + 1

        f = codecs.open('articleData.txt', 'w', 'utf-8')
        f.write('article')
        for word in article_count.keys(): f.write('\t%s' % word)
        f.write('\n')
        for article_title, wordcount in wordcounts.items():
            f.write(article_title)
            for word in article_count:
                if word in wordcount:
                    f.write('\t%d' % wordcount[word])
                else:
                    f.write('\t0')
            f.write('\n')
        f.close()




print(GroupArticle().set_article_txt())
