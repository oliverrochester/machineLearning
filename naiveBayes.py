from asyncio.windows_events import NULL
import math
from traceback import print_tb

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
        
        for i in dataArr:
            temp = i[-1].rstrip()
            i[-1] = temp

        self.myDataSet = dataArr
        self.attributes = attrArr
        del self.attributes[0]

    def getSortedData(self):
        finalData = []
        for x in range(0, len(self.attributes) + 1):
            newlist = [feature[x] for feature in self.myDataSet]
            finalData.append(newlist)
        self.myDataSetSorted = finalData

    def getMinMaxAndDiscreteFeatures(self):
        for x in range(0, len(self.attributes)):
            if(self.attributes[x][-1].lower() == "numeric" or self.attributes[x][-1].lower() == "real"):
                results = []
                for num in self.myDataSetSorted[x]:
                    results.append(num)
                    tempList = []
                    tempList.append(self.attributes[x][-2])
                    tempList.append(str(max(results)))
                    tempList.append(str(min(results)))
                    self.minMaxList.append(tempList)

            elif(self.attributes[x][-1][0] == '{'):
                tempList = []
                tempList.append(self.attributes[x][-2])
                tempList.append(self.attributes[x][-1])
                self.discreteList.append(tempList)
            else:
                print("hello")


class NaiveBayes:
    def __init__(self):
        newDataSet = dataSet()
        newDataSet.getDataSet()
        newDataSet.getSortedData()
        self.dataset = newDataSet.myDataSet
        self.sortedDataSet = newDataSet.myDataSetSorted
        self.totalInstances = len(self.sortedDataSet[-1])
        self.structure = []

    def setUpStructure(self, targetList):
        sortedDataSet = self.sortedDataSet[:-1]
        structure = []
        for value in targetList:       #iterating over yes and no    
            for featureValue in sortedDataSet:
                featureValueSet = set(featureValue)
                featureValueSet = list(featureValueSet)
                for feature in featureValueSet:
                    cnt = 1
                    arr = []
                    arr.append(value)
                    arr.append(feature)
                    for instance in self.dataset:
                        if feature in instance and instance[-1] == value:
                            cnt = cnt + 1
                    arr.append(cnt)
                    structure.append(arr)
        self.structure = structure
        # for x in self.structure:
        #     print(x)
        

    def naiveBayesAlgorithm(self, instance):
        targetList = self.sortedDataSet
        targetListSet = set(targetList[-1])
        targetListSet = list(targetListSet)
        self.setUpStructure(targetListSet)

        probabilities = []
        for value in targetListSet:
            prob = 0.0
            for feature in instance:
                for item in self.structure:
                    if(value == item[0] and feature in item):
                        prob = float(prob) + (float(item[-1] / float(self.totalInstances)))
            probabilities.append(prob)
                        
        # print(probabilities)   
        max_item = max(probabilities)
        index = probabilities.index(max_item)
        return targetListSet[index]

        
alg = NaiveBayes()
test = NaiveBayes()
print("Evaluating...")
setLength = len(test.dataset)
amountCorrect = 0
for i in test.dataset:
    instance = i[:-1]
    prediction = alg.naiveBayesAlgorithm(instance)
    if(prediction == i[-1]):
        amountCorrect = amountCorrect + 1

print("Accuracy: " + str(amountCorrect / setLength))



