import json
from pprint import pprint
from myHtml import MyHtml

lists=[]
for page in range(2, 7):
    items = MyHtml('http://opinion.scdaily.cn/wygz/index_{}.html'.format(page)).get_content()
    for item in items:
        lists.append(item)

print(json.dumps(lists))