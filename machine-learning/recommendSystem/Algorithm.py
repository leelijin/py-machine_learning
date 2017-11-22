from math import sqrt


# 皮尔逊值
def pearson(v1, v2):
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1_sq = sum([pow(v, 2) for v in v1])
    sum2_sq = sum([pow(v, 2) for v in v2])

    p_sum = sum([v1[i] * v2[i] for i in range(len(v1))])

    num = p_sum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1_sq - pow(sum1, 2) / len(v1)) * (sum2_sq - pow(sum2, 2) / len(v1)))
    if den == 0: return 0

    return num / den


# 欧几里德距离
def sim_distance(p1, p2):
    si = {}
    for item in p1:
        if item in p2:si[item] = 1

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(p1[item] - p2[item], 2)
                          for item in p1 if item in p2])
    return 1 / (1 + sqrt(sum_of_squares))


# Tanimoto 系数
def tanimoto(v1, v2):
    c1, c2, shr = 0, 0, 0

    for i in range(len(v1)):
        if v1[i] != 0: c1 += 1
        if v2[i] != 0: c2 += 1
        if v1[i] != 0 and v2[i] != 0: shr += 1
    return 1.0 - (float(shr) / (c1 + c2 - shr))
