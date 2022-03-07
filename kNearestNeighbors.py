from asyncio.windows_events import NULL
import math

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

class knnAlgorithm:
    def __init__(self):
        self.initilized = True
        newDataSet = dataSet()
        newDataSet.getDataSet()
        newDataSet.getSortedData()
        self.dataset = newDataSet.myDataSet
        self.instanceToPredict = ["5.1","3.5","1.5","0.3"]

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def getDistance(self, modifiedInstance, instanceToPredict):
        distance = 0.00
        for value in range(0, len(modifiedInstance)):
            val = (float(modifiedInstance[value]) - float(instanceToPredict[value]))
            val = float(val) * float(val)
            distance = float(distance) + float(val) 
        distance = math.sqrt(distance)
        return distance

    def knnAlgorithm(self):
        shortestDistanceInstance = NULL
        shortestDistanceSoFar = NULL
        for instance in self.dataset:
            newArr = []
            for value in range(0, len(instance) - 1):
                if(self.isfloat(value) or str(value).isnumeric()):
                    newArr.append(instance[value])
                else:
                    if(instance[value] == self.instanceToPredict[value]):
                        newArr.append('1.0')
                        self.instanceToPredict[value] = '1.0'
                    else:
                        newArr.append('2.0')
                        self.instanceToPredict[value] = '1.0'
            distance = self.getDistance(newArr, self.instanceToPredict)  
            if(shortestDistanceSoFar == NULL):
                shortestDistanceSoFar = distance
                shortestDistanceInstance = instance
            else:
                if(distance < shortestDistanceSoFar):
                    shortestDistanceSoFar = distance
                    shortestDistanceInstance = instance
        return shortestDistanceInstance


instanceToPredict = []
alg = knnAlgorithm()
prediction = alg.knnAlgorithm()
print("Prediction is:  " + str(prediction[-1]))






    
        