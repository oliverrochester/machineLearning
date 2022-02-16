from asyncio.windows_events import NULL
import math
from re import I

from numpy import array

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
                dataArr.append(subDataArr[1:])
        
        for i in dataArr:
            temp = i[-1].rstrip()
            i[-1] = temp

        self.myDataSet = dataArr
        self.attributes = attrArr
        del self.attributes[0]

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
        print("parent entropy: " + str(parentEntropy))
        arrWithoutTarget = arr[:-1]
        
        x = 0
        for feature in arrWithoutTarget:
            copyParentEntropy = parentEntropy
            valueArray = []
            uniqueSet = set(feature)
            uniqueSet = (list(uniqueSet))
            print(uniqueSet)
            for value in uniqueSet:
                print("interating on: " + value)
                for targetValue in self.myDataSet:
                    if(value == targetValue[x]):
                        valueArray.append(targetValue[-1])
                print(valueArray)
                entropy = self.getEntropyOfFeature(valueArray)
                print("entropy: " + str(entropy))
                copyParentEntropy = copyParentEntropy - ((len(valueArray) / len(self.myDataSetSorted[-1])) * entropy)
                print(copyParentEntropy)
                valueArray = []
                print('\n')
            x = x + 1
            finalInfoGainArray.append(round(copyParentEntropy, 4))  
        
        return finalInfoGainArray

class Node:
    def __init__(self, parent, instancesArr, targetFeature):
        self.parent = parent
        self.routes = instancesArr
        self.children = []
        self.targetFeatureValue = targetFeature

    def getInstances(self,infoGainArray, instances, attributes):
        # print(str(infoGainArray))
        if(len(infoGainArray) == 0):
            return []
        max_value = max(infoGainArray)
        max_index = infoGainArray.index(max_value)
        print(max_index)
        rootFeature = attributes[max_index]
        targets = rootFeature[-1]
        targets = targets.replace('{', '')
        targets = targets.replace('}', '')
        targets = targets.split(',')
        instancesArray = []
        for value in targets:
            arr = []
            arr.append(value)
            for instance in instances:
                if(instance[max_index] == value):
                    del instance[max_index]
                    arr.append(instance)
            instancesArray.append(arr)
        return instancesArray

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

    def getInformationGain(self, arr, sortedData):
        finalInfoGainArray = []
        entropy = 0.00
        parentEntropy = self.getEntropyOfFeature(sortedData[-1])
        print('\n')
        print("parent entropy: " + str(parentEntropy))
        arrWithoutTarget = sortedData[:-1]
        
        x = 0
        for feature in arrWithoutTarget:
            copyParentEntropy = parentEntropy
            valueArray = []
            uniqueSet = set(feature)
            uniqueSet = (list(uniqueSet))
            print(uniqueSet)
            for value in uniqueSet:
                print("interating on: " + value)
                for targetValue in arr:
                    if(value == targetValue[x]):
                        valueArray.append(targetValue[-1])
                print(valueArray)
                entropy = self.getEntropyOfFeature(valueArray)
                print("entropy: " + str(entropy))
                copyParentEntropy = copyParentEntropy - ((len(valueArray) / len(sortedData[-1])) * entropy)
                print(copyParentEntropy)
                valueArray = []
                print('\n')
            x = x + 1
            finalInfoGainArray.append(round(copyParentEntropy, 4))  
        
        return finalInfoGainArray

    def createDecisionTree(self, route, attributes, cnt):
        if(len(route) == 2):
            leafNode = Node(self, NULL, route)
            self.children.append(leafNode)
            print('created leaf node: ' + str(leafNode.targetFeatureValue) +  "    parent node is: " + str(leafNode.parent.targetFeatureValue))
        elif(len(route) >= 3):
            instances = route[1:]
            sortedData = []
            for x in range(0, len(route[1])):
                newlist = [feature[x] for feature in instances]
                sortedData.append(newlist)
            infoGainArr = self.getInformationGain(instances, sortedData)
            max_value = max(infoGainArr)
            max_index = infoGainArr.index(max_value)
            print(max_index)
            print('info gain array; ' + str(infoGainArr))
            instances = self.getInstances(infoGainArr, instances, attributes)
            print('instances')
            for i in instances:
                print(i)
            

            treeNode = Node(self, instances, attributes[max_index])
            treeNode.targetFeatureValue[0] = route[0]
            self.children.append(treeNode)
            print("created tree node: " + str(treeNode.targetFeatureValue)+ "    parent node is: " + str(treeNode.parent.targetFeatureValue))
            treeNode.iterateRoutes(instances, attributes, cnt)
            

    def iterateRoutes(self, routes, attributes, cnt):
        for route in routes:
            self.createDecisionTree(route, attributes, cnt)
        cnt = cnt + 1

    def printNode(self):    
        for i in self.children:
            i.printNode()
        # print(self.targetFeatureValue)
        # print(self.routes)

    def predict(self, instance):
        targets = []
        if(len(instance) <= 1):
            return self.targetFeatureValue[1]
        print(self.targetFeatureValue)
        if(self.targetFeatureValue[-1][0] == '{'):
            targets = self.targetFeatureValue[-1]
            targets = targets.replace('{', '')
            targets = targets.replace('}', '')
            targets = targets.split(',')
        print(targets)
        for i in self.children:
            print(instance[0])
            print(i.targetFeatureValue[0])
            if(instance[0] == i.targetFeatureValue[0]):
                newInstance = instance[1:]
                print("new instance; " + str(newInstance))
                i.predict(newInstance)
                

class id3Algorithm:
    def __init__(self):
        self.informationGainArray = NULL
        self.rootNode = NULL

    def printTree(self):
        self.rootNode.printNode()

    def id3Algorithm(self):
        data = dataSet()
        data.getDataSet()
        data.getSortedData()
        data.getMinMaxAndDiscreteFeatures()
        infoGainArray = data.getInformationGain(data.myDataSetSorted)
        print(str(infoGainArray))
        max_value = max(infoGainArray)
        max_index = infoGainArray.index(max_value)
        print(max_index)
        rootFeature = data.attributes[max_index]
        del data.attributes[max_index]
        targets = rootFeature[-1]
        targets = targets.replace('{', '')
        targets = targets.replace('}', '')
        targets = targets.split(',')
        instancesArray = []
        for value in targets:
            arr = []
            arr.append(value)
            for instance in data.myDataSet:
                if(instance[max_index] == value):
                    del instance[max_index]
                    arr.append(instance)
            instancesArray.append(arr)

        dataSetCopy = data.myDataSet
        sortedDataSetCopy = data.myDataSetSorted

        self.rootNode = Node(NULL, instancesArray, rootFeature)
        print("created tree node:  " + str(self.rootNode.targetFeatureValue) + "    parent node is: " + str(self.rootNode.parent))
        for i in self.rootNode.routes:
            print(i)
        self.rootNode.iterateRoutes(self.rootNode.routes, data.attributes, 1)

    def predictInstance(self, instance):
        return self.rootNode.predict(instance)

id3 = id3Algorithm()
id3.id3Algorithm()
print('\n')
print('\n')
print('\n')
id3.printTree()
prediction = id3.predictInstance(['low', 'false', 'steep'])
print("prediction: " + str(prediction))
























