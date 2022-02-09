from asyncio.windows_events import NULL
import math
from re import I

class dataSet:
    def __init__(self):
        self.myDataSet = []
        self.attributes = []
        self.myDataSetSorted = []
        self.minMaxList = []         #formatted [ [attribute, max, min], [attribute, max, min]... ]
        self.discreteList = []       #foramtted [ [attribute, attribute values], [attribute, attribute values]... ]

    def getDataSet(self):
        print("Enter file name: ")
        filename = input()
        file = open(filename, "r")

        attrArr = []
        dataArr = []
        attrArrLen = 0
        for x in file:
            if(x[0] == '%'):
                continue
            elif('@ATTRIBUTE' in x or '@attribute' in x or '@Attribute' in x):
                newAttr = ''
                for ch in x:
                    if(ch == '%'):
                        break
                    else:
                        newAttr += ch
                arr = newAttr.split()
                attrArr.append(arr)

            elif('@DATA' in x or '@data' in x or '@Data' in x):
                attrArrLen = len(attrArr)
                continue
            elif('@RELATION' in x or '@relation' in x or '@Relation' in x):
                continue
            elif(x == '\n'):
                continue
            else:
                subDataArr = x.split(',')
                dataArr.append(subDataArr)
        self.myDataSet = dataArr
        self.attributes = attrArr

    def getSortedData(self):
        finalData = []
        for x in range(0, len(self.attributes)):
            newlist = [feature[x] for feature in self.myDataSet]
            finalData.append(newlist)
        self.myDataSetSorted = finalData

    def getMinMaxAndDiscreteFeatures(self):
        for x in range(0, len(self.attributes)):
            if(self.attributes[x][-1].lower() == "numeric" or self.attributes[x][-1].lower() == "real"):
                results = []
                for num in self.myDataSetSorted[x]:
                    results.append(float(num))
                    tempList = []
                    tempList.append(self.attributes[x][-2])
                    tempList.append(str(max(results)))
                    tempList.append(str(min(results)))
                self.minMaxList.append(tempList)

            if(self.attributes[x][-1][0] == '{'):
                tempList = []
                tempList.append(self.attributes[x][-2])
                tempList.append(self.attributes[x][-1])
                self.discreteList.append(tempList)

    def getEntropyOfFeature(self, arr):

        list_set = set(arr)
        unique_list = (list(list_set))

        def getEntropyHelper(n):
            cnt = 0
            for i in arr:
                if(i == n):
                    cnt = cnt + 1

            x = round((cnt/ len(arr)),4) 
            ans = -1 * (math.log(x) / math.log(2))
            newAns = float(x) * float(ans)
            newAns = round(newAns, 4)
            return newAns

        result = map(getEntropyHelper, unique_list)
        result = list(result)

        cnt = 0.00
        for x in result:
            cnt = cnt + x
        return cnt
 
    def getInformationGain(self, arr):
        finalInfoGainArray = []
        entropy = 0.00
        parentEntropy = self.getEntropyOfFeature(arr[-1])
        finalEntropyArray = []
        arrWithoutTarget = arr[:-1]
        x = 0
        while(x < len(arrWithoutTarget)):
            for feature in arrWithoutTarget:
                copyParentEntropy = parentEntropy
                valueArray = []
                uniqueSet = set(feature)
                uniqueSet = (list(uniqueSet))
                for value in uniqueSet:
                    for targetValue in self.myDataSet:
                        if(value == targetValue[x]):
                            valueArray.append(targetValue[-1])
                    entropy = self.getEntropyOfFeature(valueArray)
                    copyParentEntropy = copyParentEntropy - ((len(valueArray) / len(self.myDataSet[-1])) * entropy)
                    finalEntropyArray.append(round((-1 *(copyParentEntropy - entropy)),4))
                    valueArray = []
            finalInfoGainArray.append(copyParentEntropy)
            x = x + 1
        return finalInfoGainArray

class Node:
    def __init__(self):
        self.parent = None
        self.children = []
        self.targetFeatureValue = None

class id3Algorithm:
    def __init__(self):
        self.informationGainArray = NULL
        self.rootNode = NULL

    def createDecisionTree(self, infoGainArray):
        print()

    def id3Algorithm(self):
        data = dataSet()
        data.getDataSet()
        data.getSortedData()
        data.getMinMaxAndDiscreteFeatures()
        infoGainArray = data.getInformationGain(data.myDataSetSorted)
        print(str(infoGainArray))
        self.createDecisionTree(infoGainArray)

    




id3 = id3Algorithm()
id3.id3Algorithm()
























