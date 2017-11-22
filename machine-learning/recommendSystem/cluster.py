import codecs
import pprint
from math import sqrt
from pprint import pprint
from random import random
import numpy as np
import matplotlib.pyplot as plt


def read_file(filename):
    lines = codecs.open(filename, 'r', 'utf-8').readlines()

    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        rownames.append(p[0])
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data

# 欧几里德距离
def sim_distance(p1, p2):
    si = {}
    for item in p1:
        if item in p2:si[item] = 1

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(p1[item] - p2[item], 2) for item in p1 if item in p2])
    return 1 / (1 + sqrt(sum_of_squares))


# Tanimoto 系数
def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0

    for i in range(len(v1)):
        if v1[i] != 0: c1 += 1
        if v2[i] != 0: c2 += 1
        if v1[i] != 0 and v2[i] != 0: shr += 1
    return 1.0 - (float(shr) / (c1 + c2 - shr))

def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])

    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    # 相似度越大，距离越短
    return 1.0 - num / den


class Cluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance


def hcluster(rows, distance=pearson):
    distances = {}
    current_cluster_id = -1

    clust = [Cluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                if (clust[i].id, clust[j].id) not in distances:
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        merge_vec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in
                     range(len(clust[0].vec))]

        new_cluster = Cluster(merge_vec, left=clust[lowestpair[0]], right=clust[lowestpair[1]], distance=closest,
                              id=current_cluster_id)

        current_cluster_id -= 1
        del clust[lowestpair[1]]
        del clust[lowestpair[0]]
        clust.append(new_cluster)

    return clust[0]


def print_clust(clust, labels=None, n=0):
    for i in range(n): print('  ', end='')
    if clust.id < 0:
        print('-')
    else:
        if labels is None:
            print(clust.id)
        else:
            print(labels[clust.id])

    if clust.left is not None: print_clust(clust.left, labels=labels, n=n + 1)
    if clust.right is not None: print_clust(clust.right, labels=labels, n=n + 1)


def rotate_matrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
    return newdata


def scale_down(data, distance=pearson, rate=0.01):
    n = len(data)

    realdist = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]

    outersum = 0.0

    loc = [[random(), random()] for i in range(n)]
    fake_dist = [[0.0 for j in range(n)] for i in range(n)]

    last_error = None

    for m in range(0, 1000):
        for i in range(n):
            for j in range(n):
                fake_dist[i][j] = sqrt(sum([pow(loc[i][x] - loc[j][x], 2) for x in range(len(loc[i]))]))

        grad = [[0.0, 0.0] for i in range(n)]

        total_error = 0

        for k in range(n):
            for j in range(n):
                if j == k: continue

                error_term = (fake_dist[j][k] - realdist[j][k]) / realdist[j][k]

                grad[k][0] += ((loc[k][0] - loc[j][0]) / fake_dist[j][k] * error_term)
                grad[k][1] += ((loc[k][1] - loc[j][1]) / fake_dist[j][k] * error_term)

                total_error += abs(error_term)

        if last_error and last_error < total_error: break
        last_error = total_error

        for k in range(n):
            loc[k][0] -= rate * grad[k][0]
            loc[k][1] -= rate * grad[k][1]
    return loc


def draw2d(dots, labels):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    x = [i[0] for i in dots]
    y = [i[1] for i in dots]
    plt.scatter(x, y)

    for i, xd, yd in zip(range(len(x)), x, y):
        print(labels[i], xd, yd)
        plt.annotate(labels[i][:10], xy=(xd, yd), xytext=(-10, 10), textcoords='offset points', ha='right', va='bottom',
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))

    plt.show()


rownames, colnames, data = read_file('articleData.txt')

dots = scale_down(data)

draw2d(dots, rownames)
# print_clust(hcluster(rotate_matrix(data)), labels=colnames)
