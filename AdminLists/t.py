


arr1 = [2]
arr2 = [2]
p = 11
count = 0
for i in range(len(arr1)):
    for j in range(len(arr2)):
        if(p > (arr1[i] ^ arr2[j])):
            if(((arr1[i]*(arr1[i] ^ arr2[j]))-1)%p == 0):
                count+=1

print(count)