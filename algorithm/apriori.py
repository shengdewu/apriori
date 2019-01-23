import numpy as np

class tool(object):
    def testData(self):
        return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

    @staticmethod
    def toList(element):
        val = [element]
        return val

class apriori(object):
    def calcC1(self, dataSet):
        C = set()
        for val in dataSet:
            tmp = set(val)
            C.update(tmp)
        C = sorted(C)
        C1 = list(map(tool.toList, C))
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

    def scanData(self, dataSet, Ck, minSupport=0.5):
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
            if sup >= minSupport:
                retSup[key] = [val[0],sup]
                retC.append(val[0])

        return retC, retSup


    def calcApriori(self, dataSet, limit):
        support = []
        L = []
        C1 = self.calcC1(dataSet)
        L1, L1Sup = self.scanData(dataSet, C1, limit)
        support.append(L1Sup)
        L.append(L1)

        Ck_1 = L1
        while True:
            Ck = self.calcCk(Ck_1)
            Lk, LkSup = self.scanData(dataSet, Ck, limit)
            if not Lk:
                break
            support.append(LkSup)
            L.append(Lk.copy())
            Ck_1 = Lk
        return L, support

    def calcR2(self, L):
        Ck = []
        for i in range(len(L)-1):
            for j in range(i+1, len(L)):
                tmp = list(set([L[i], L[j]]))
                Ck.append(tmp)
        return Ck

    def calcR1(self, L):
        C1 = []
        for l in L:
            C1.append([l])
        return C1

    def calcRule(self,Lk):
        rule = {}
        for L in Lk:
            for l in L:
                if len(l) <= 1:
                    continue
                if len(l) == 2:
                    rule[str(l)] = self.calcR1(l)
                    continue
                l2 = self.calcR2(l)
                r = l2
                lk_1 = l2
                m = 3
                while len(l) > m:
                    lk = self.calcCk(lk_1)
                    r.extend(lk)
                    m += 1
                    lk_1 = lk

                rule[str(l)] = r
        return rule

    def calcConfidence(self, pfh, freq, minConf=0.7):
        # p freq_p h
        validConf = {}
        for r in pfh:
            conf = freq[1]/r[1]
            if conf >= minConf:
                key = str(r[0]) + '-->' + str(r[2])
                validConf[key] = conf
        return validConf

    def calcDepend(self, L, support, minConf = 0.7):
        '''
        P-->H = (p|h)/p
        '''
        ruleDict = self.calcRule(L)
        print(ruleDict)
        validConf = []
        for key, rule in ruleDict.items():
            index = len(rule[0])
            freq = support[index].get(key)

            validP= []  # p freq_p h
            for r in rule:
                p = list(set(freq[0]) - set(r))
                pVal = support[0].get(str(p))
                if pVal:
                    validP.append((pVal[0], pVal[1], r))
            validConf.append(self.calcConfidence(validP, freq, minConf))

        return validConf


