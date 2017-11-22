import jieba
import jieba.analyse

# file_name = './extra_dict/dict.txt.big'
# jieba.load_userdict(file_name)
jieba.load_userdict('./userDict.txt')
jieba.suggest_freq('POP MART',True)
text = '#新店开业#POP MART作为国内乃至全球最大的潮流玩具运营商之一，签约了多个国内外一线潮流玩具品牌，同时以做温暖的品牌为愿景，传递美好。昨天，POP ' \
       'MART成都远洋太古里店已欢乐开业，新店开业惊喜优惠不停，欢迎莅临选购！#Welcome to the Open Lanes#';
seg_list = jieba.cut(text, cut_all=False)
print(jieba.analyse.extract_tags(text, topK=20, withWeight=False, allowPOS=()))
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式