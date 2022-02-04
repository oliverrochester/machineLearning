from os import write
import math

class dataSet:
    def __init__(self):
        self.myDataSet = []
        self.attributes = []
        self.myDataSetSorted = []
        self.minMaxList = []            #formatted [ [attribute, max, min], [attribute, max, min]... ]
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
            for i in unique_list:
                if(i == n):
                    cnt  = cnt + 1

            x = round((cnt/ len(unique_list)),4) 
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
        targetFeatureEntropy = self.getEntropyOfFeature(arr[-1])
        entropyArray = []
        arrWithoutTarget = arr[:-1]
        for feature in arrWithoutTarget:
            entropy = self.getEntropyOfFeature(feature)
            entropyArray.append(round((-1 *(targetFeatureEntropy - entropy)),4))
        return list(entropyArray)

    def id3Algorithm(self):
        print(self.getInformationGain(self.myDataSetSorted))

class Node:
    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None
        self.targetFeatureValue = None


data = dataSet()
data.getDataSet()
data.getSortedData()
data.getMinMaxAndDiscreteFeatures()
data.id3Algorithm()






















