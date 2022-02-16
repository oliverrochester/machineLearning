import math

dataArray = ['chapparal','chapparal','chapparal','riparian','riparian','connifer','connifer']

list_set = set(dataArray)
unique_list = (list(list_set))

def calculate(n):

    cnt = 0
    for i in dataArray:
        if(i == n):
            cnt = cnt + 1

    x = round((cnt/ len(dataArray)),4) 
    ans = -1 * (math.log(x) / math.log(2))
    newAns = float(x) * float(ans)
    newAns = round(newAns, 4)
    return newAns

result = map(calculate, unique_list)

result = list(result)
print(result)

cnt = 0.00
for x in result:
    cnt = cnt + x

print(round(cnt, 4))

