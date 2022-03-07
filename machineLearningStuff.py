from asyncio.windows_events import NULL
from logging import root
import math
from re import I
from typing import final

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
        # print("parent entropy: " + str(parentEntropy))
        arrWithoutTarget = arr[:-1]
        
        x = 0
        for feature in arrWithoutTarget:
            copyParentEntropy = parentEntropy
            valueArray = []
            uniqueSet = set(feature)
            uniqueSet = (list(uniqueSet))
            # print(uniqueSet)
            for value in uniqueSet:
                # print("interating on: " + value)
                for targetValue in self.myDataSet:
                    if(value == targetValue[x]):
                        valueArray.append(targetValue[-1])
                # print(valueArray)
                entropy = self.getEntropyOfFeature(valueArray)
                # print("entropy: " + str(entropy))
                copyParentEntropy = copyParentEntropy - ((len(valueArray) / len(self.myDataSetSorted[-1])) * entropy)
                # print(copyParentEntropy)
                valueArray = []
                print('\n')
            x = x + 1
            finalInfoGainArray.append(round(copyParentEntropy, 4))  
        
        return finalInfoGainArray

class Node:
    def __init__(self, nodeType, path, children, nodeLabel, parent, instancesArr):
        self.nodeType = nodeType
        self.parent = parent
        self.routes = instancesArr
        self.children = children
        self.nodeLabel = nodeLabel
        self.path = path

    def sortData(self, arr):
        print(arr)
        finalData = []
        for x in range(0, len(arr[1])):
            newlist = [val[x] for val in arr]
            finalData.append(newlist)
        return finalData

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
        # print('\n')
        # print("parent entropy: " + str(parentEntropy))
        arrWithoutTarget = sortedData[:-1]
        
        x = 0
        for feature in arrWithoutTarget:
            copyParentEntropy = parentEntropy
            valueArray = []
            uniqueSet = set(feature)
            uniqueSet = (list(uniqueSet))
            # print(uniqueSet)
            for value in uniqueSet:
                # print("interating on: " + value)
                for targetValue in arr:
                    if(value == targetValue[x]):
                        valueArray.append(targetValue[-1])
                # print(valueArray)
                entropy = self.getEntropyOfFeature(valueArray)
                # print("entropy: " + str(entropy))
                copyParentEntropy = copyParentEntropy - ((len(valueArray) / len(sortedData[-1])) * entropy)
                # print(copyParentEntropy)
                valueArray = []
                
            x = x + 1
            finalInfoGainArray.append(round(copyParentEntropy, 4))  
        
        return finalInfoGainArray

    def createDecisionTree(self, route, attributes):
        if(len(route) < 2):
            leafNode = Node("LeafNode", route[0], [], "undetermined", self, NULL)
            self.children.append(leafNode)
        if(len(route) == 2):
            leafNode = Node("LeafNode", route[0], [], route[1][-1], self, NULL)
            self.children.append(leafNode)
        if(len(route) > 2):
            instancesArr = route[1:]
            allTheSame = True
            initial = instancesArr[0][-1]
            for i in instancesArr:
                if initial != i[-1]:
                    allTheSame = False
            
            if(allTheSame):
                leafNode = Node("LeafNode", route[0], [], instancesArr[0][-1], self, NULL)
                self.children.append(leafNode)
            else:
                sortedData = self.sortData(instancesArr)
                infoGainArr = self.getInformationGain(instancesArr, sortedData)
                print(infoGainArr)
                print(attributes)
                max_value = max(infoGainArr)
                max_index = infoGainArr.index(max_value)
                print(max_index)
                print(attributes[max_index])
                rootFeature = attributes[max_index]
                targets = rootFeature[-1]
                targets = targets.replace('{', '')
                targets = targets.replace('}', '')
                targets = targets.split(',')
                instancesArray = []
                for value in targets:
                    arr = []
                    arr.append(value)
                    for instance in instancesArr:
                        if(instance[max_index] == value):
                            del instance[max_index]
                            arr.append(instance)
                    instancesArray.append(arr)
                for i in instancesArray:
                    print(i)

                treeNode = Node("TreeNode", route[0], [], rootFeature, self, instancesArray)
                
                self.children.append(treeNode)
                treeNode.iterateRoutes(instancesArray, attributes)
                print('\n')

    def iterateRoutes(self, routes, attributes):
        for route in routes:
            self.createDecisionTree(route, attributes)

    def printNode(self):  
        print("Node Type: " + str(self.nodeType) + ":   Node value: " + str(self.nodeLabel))
        for i in self.children:
            i.printNode()
        # print(self.targetFeatureValue)
        # print(self.routes)

    def predict(self, instance):
        cpyInstance = instance
        tempNode = self
        if(self.nodeType == "LeafNode"):
            print('hit leaf node')
            print('prediction is: ' + str(self.nodeLabel))
            # ans = str(self.nodeLabel)
            # return ans
        else:
            for i in instance:
                for x in self.children:
                    if i == x.path:
                        cpyInstance.remove(i)
                        tempNode = x
                        break
            tempNode.predict(cpyInstance)

            # for i in self.children:
            #     if(str(instance[0]) == str(i.path)):
            #         print('found it')
            #         cpyInstance = cpyInstance[1:]
            #         print(cpyInstance)
            #         tempNode = i
            #         break
            # tempNode.predict(cpyInstance)
            
       
                

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
        for i in data.myDataSetSorted:
            print(i)
        infoGainArray = data.getInformationGain(data.myDataSetSorted)
        print(str(infoGainArray))
        max_value = max(infoGainArray)
        max_index = infoGainArray.index(max_value)
        print(max_index)
        rootFeature = data.attributes[max_index]
        del data.attributes[max_index]
        del data.attributes[-1]
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
        
        self.rootNode = Node("TreeNode",NULL, [],rootFeature,NULL,instancesArray)
        print("created root node:  " + str(self.rootNode.nodeLabel) + "    parent node is: " + str(self.rootNode.parent))
        print(data.attributes)
        for i in self.rootNode.routes:
            print(i)
        print('\n')
        self.rootNode.iterateRoutes(self.rootNode.routes, data.attributes)

    def predictInstance(self, instance):
        self.rootNode.predict(instance)
        # return ans



id3 = id3Algorithm()
id3.id3Algorithm()
print('\n')
print('\n')
print('\n')
id3.printTree()

testInstances = [
    ['false', 'steep', 'high'],
    ['true', 'moderate', 'low'],
    ['true', 'steep', 'medium'],
    ['false', 'steep', 'medium'],
    ['false', 'flat', 'high'],
    ['true', 'steep', 'highest'],
    ['true', 'steep', 'high'],
    ['false', 'moderate', 'high'],
    ['true', 'flat', 'high']
]

for instance in testInstances:
    id3.predictInstance(instance)
# print("prediction: " + str(prediction))
























