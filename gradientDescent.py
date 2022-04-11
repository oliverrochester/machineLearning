from asyncio.windows_events import NULL
import math
import random

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


class GradientDescent:
    def __init__(self):
        newDataSet = dataSet()
        newDataSet.getDataSet()
        newDataSet.getSortedData()
        self.dataset = newDataSet.myDataSet
        self.weights = self.getWeights()
        self.summedWeights = []
    
    def getWeights(self):
        weightList = []
        for x in range(0, len(self.dataset[0]) - 1):
           weightList.append(random.random())

        weightList = [-.146,.185,-.044,.119]            #potentially take this line out later
        print(weightList)
        return weightList

    def GD(self):
        x = 0
        improved = True
        notImprovedCnt = 0
        previousFirstWeight = 0.00
        while(improved):
            summedErrorDeltas = []
            sumOfSquaredError = 0.00
            sumOfSquaredErrorDividedByTwo = 0.00
            for instance in self.dataset:
                t_1 = instance[-1]
                d_1 = instance[:-1]
                M_w = 0.00
                for num in range(0,len(d_1)):
                    M_w = M_w + (float(d_1[num]) * float(self.weights[num]))

                error = float(t_1) - float(M_w)
                squaredError = error * error
                sumOfSquaredError = sumOfSquaredError + squaredError
                errorDeltaArray = []
                for num in range(0,len(self.weights)):
                    errorDeltaArray.append(float(error) * float(d_1[num]))

                if(len(summedErrorDeltas) == 0):
                    summedErrorDeltas = errorDeltaArray
                else:
                    for num in range(0,len(errorDeltaArray)):
                        summedErrorDeltas[num] = summedErrorDeltas[num] + errorDeltaArray[num]

            for num in range(0,len(summedErrorDeltas)):
                self.weights[num] = round(float(self.weights[num]) + (summedErrorDeltas[num] * 0.00000002),6)
                 
            # print(self.weights)

            sumOfSquaredErrorDividedByTwo = sumOfSquaredError / 2
            x = x + 1
            if(self.weights[0] == previousFirstWeight):
                notImprovedCnt = notImprovedCnt + 1
            else:
                notImprovedCnt = 0

            previousFirstWeight = self.weights[0]
            if(notImprovedCnt == 100):
                improved = False

        print("interations: " + str(x))
newGradientDescent = GradientDescent()
newGradientDescent.GD()