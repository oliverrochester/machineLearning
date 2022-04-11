


def isPalindrome(str):
    end = len(str) - 1
    for i in range(0,end):
        if(str[i] != str[end]):
            return "False"
        else:
            end = end - 1
    return "True"
    
def palindroneRecurse(str):
    if(len(str)==1):
        return True
    elif(len(str) ==2):
        return str[0] == str[1]
    else:
        if(str[0] == str[-1]):
            newStr = str[:-1]
            newStr = newStr[1:]
            return palindroneRecurse(newStr)
        else:
            return False


def normalMatrixMult(m1, m2):
    if(len(m1[0]) != len(m2)):
        return []
    cnt = 0
    ansArr = []
    ans = 0
    finalArr = []
    for vec in m1:
        row = 0
        col = 0 
        cnt = 0
        while(cnt < len(m2[0])):
            for num in vec:
                ans = ans + (num * m2[row][col])
                row = row + 1 
            ansArr.append(ans)
            if(len(ansArr) == len(m2[0])):
                finalArr.append(ansArr)
                ansArr = []
            row = 0
            col = col + 1
            ans = 0
            cnt = cnt + 1
        
    return finalArr
    
       




#66
m1 = [
        [3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5],
        [1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4,1,2,4],
        [8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1,8,3,1]
    ]
m2 = [
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        [3,1,2,3],
        [8,4,4,1],
        [3,1,1,2],
        
        
    ]

newMatrix = normalMatrixMult(m1, m2)
if(len(newMatrix)==0):
    print("Invalid matrix sizes for multiplication")
else:
    for x in newMatrix:
        print(x)
ans = isPalindrome("abcdefghiihgfedcba")
print(ans)

ans2 = palindroneRecurse("abcdefghiihgfedcba")
print(ans2)