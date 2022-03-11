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

    def nnAlgorithm(self, instanceToPredict):
        shortestDistanceInstance = NULL
        shortestDistanceSoFar = NULL
        for instance in self.dataset:
            newArr = []
            for value in range(0, len(instance) - 1):
                if(self.isfloat(instance[value]) or str(instance[value]).isnumeric()):
                    newArr.append(instance[value])
                else:
                    if(instance[value] == instanceToPredict[value]):
                        newArr.append('1.0')
                        instanceToPredict[value] = '1.0'
                    else:
                        newArr.append('2.0')
                        instanceToPredict[value] = '1.0'
            distance = self.getDistance(newArr, instanceToPredict)  
            if(shortestDistanceSoFar == NULL):
                shortestDistanceSoFar = distance
                shortestDistanceInstance = instance
            else:
                if(distance < shortestDistanceSoFar):
                    shortestDistanceSoFar = distance
                    shortestDistanceInstance = instance
        return shortestDistanceInstance

    def sortArray(self, arr):
        cpyArr = arr
        cnt = 0
        while(cnt != len(cpyArr)):
            for x in range(0, len(cpyArr)-1):
               if(cpyArr[x][0] > cpyArr[x+1][0]):
                   temp = cpyArr[x]
                   cpyArr[x] = cpyArr[x+1]
                   cpyArr[x+1] = temp
            cnt = cnt + 1
        return cpyArr

    def knnAlgorithm(self, k, instanceToPredict):
        endArray = []
        for instance in self.dataset:
            newArr = []
            tempArr = []
            for value in range(0, len(instance) - 1):
                if(self.isfloat(instance[value]) or str(instance[value]).isnumeric()):
                    newArr.append(instance[value])
                else:
                    if(instance[value] == instanceToPredict[value]):
                        newArr.append('1.0')
                        instanceToPredict[value] = '1.0'
                    else:
                        newArr.append('2.0')
                        instanceToPredict[value] = '1.0'
            distance = self.getDistance(newArr, instanceToPredict)  
            tempArr.append(distance)
            tempArr.append(instance[-1])
            endArray.append(tempArr)
        endArray = self.sortArray(endArray)
        kthArray = []
        for x in range(0, k - 1):
            kthArray.append(endArray[x][1])

        if(self.isfloat(kthArray[0]) or str(kthArray[0]).isnumeric()):
            return sum(kthArray) / len(kthArray)
        else:
            return max(set(kthArray), key = kthArray.count)
 


alg = knnAlgorithm()
test = knnAlgorithm()
setLength = len(test.dataset)
amountCorrect = 0
print("Evaluating...")
for i in test.dataset:
    instance = i[:-1]
    prediction = alg.knnAlgorithm(5, instance)
    # prediction = prediction[-1]
    if(prediction == i[-1]):
        amountCorrect = amountCorrect + 1

print("Accuracy: " + str(amountCorrect / setLength))

# 
# print("Prediction is:  " + str(prediction))






    
        