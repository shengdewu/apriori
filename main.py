from algorithm.apriori import *


if '__main__' == __name__:
    dataPre = tool()
    alg = apriori()

    dataSet = dataPre.testData()

    C1 = alg.calcC1(dataSet)
    retC, L1 = alg.scanData(dataSet, C1, 0.5)
    print(retC)
    print(L1)

    support = alg.calcApriori(dataSet, 0.7)

    print(support)