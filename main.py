from algorithm.apriori import *


if '__main__' == __name__:
    dataPre = tool()
    alg = apriori()

    dataSet = dataPre.testData()

    C1 = alg.calcC1(dataSet)
    print(C1)
    retC, L1 = alg.scanData(dataSet, C1, 0.5)
    print(retC)
    print(L1)

    print(alg.calcCk(C1))
    L, support = alg.calcApriori(dataSet, 0.5)

    print(L)
    print(support)

    conf = alg.calcDepend(L, support, 0.6)

    print(conf)