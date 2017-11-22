from math import sqrt
from pprint import pprint
from random import random

import requests

API_HOST = 'http://127.0.0.1:88'

usr_api = API_HOST + '/api/users'
req = requests.get(usr_api)
content = req.json()


# 欧几里德距离
def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in prefs[person1] if item in prefs[person2]])
    return 1 / (1 + sqrt(sum_of_squares))


# 皮尔逊系数
def sim_person(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]: si[item] = 1

    n = len(si)

    if n == 0: return 1

    sum1 = sum([prefs[person1][it] for it in si])
    sum2 = sum([prefs[person2][it] for it in si])

    sum1Sq = sum([pow(prefs[person1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in si])

    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0: return 0

    return num / den


def top_matches(prefs, person, n=5, similarity=sim_distance):
    scores = [(similarity(prefs, person, other), other) for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]


def getRecommendations(prefs, person, similarity=sim_person):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <= 0: continue
        for item in prefs[other]:
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                simSums.setdefault(item, 0)
                simSums[item] += sim

        rankings = [(total / simSums[item], item) for item, total in totals.items()]

        rankings.sort()
        rankings.reverse()
        return rankings


class DistancesStore:
    def __init__(self, role_a, role_b, distance=None):
        self.roleA = role_a
        self.roleB = role_b
        self.distance = distance


