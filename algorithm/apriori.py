import numpy as np

class tool(object):
    def testData(self):
        return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]


class apriori(object):
    def calcC1(self, dataSet):
        C = set()
        for val in dataSet:
            tmp = set(val)
            C.update(tmp)
        C = sorted(C)
        C1 = []
        for c in C:
            t = []
            t.append(c)
            C1.append(t)
        return C1

    def calcCk(self, Ck_1):
        Ck = []
        for i in range(len(Ck_1)-1):
            for j in range(i+1, len(Ck_1)):
                tmp = Ck_1[i].copy()
                tmp = list(set(tmp) | set(Ck_1[j]))
                length = len(Ck)
                bFind = False
                if length >= 1:
                    for k in range(len(Ck)):
                        if tmp == Ck[k]:
                            bFind = True
                            break
                if not bFind:
                    Ck.append(tmp)
        return Ck

    def scanData(self, dataSet, Ck, limit):
        support = {}
        for C in Ck:
            for val in dataSet:
                if set(C).issubset(val):
                    if not support.get(str(C)):
                        support[str(C)] = [C,0]
                    support[str(C)][1] += 1

        num = len(dataSet)
        retSup = {}
        retC = []
        for key, val in support.items():
            sup = val[1] / num
            if sup >= limit:
                retSup[key] = [val[0],sup]
                retC.append(val[0])

        return retC, retSup


    def calcApriori(self, dataSet, limit):
        support = []
        C1 = self.calcC1(dataSet)
        L1, L1Sup = self.scanData(dataSet, C1, limit)
        support.append(L1Sup)

        Ck_1 = L1
        while True:
            Ck = self.calcCk(Ck_1)
            Lk, LkSup = self.scanData(dataSet, Ck, limit)
            if not Lk:
                break
            support.append(LkSup)
            Ck_1 = Lk
        return support
