s = input()
key = []
val = []
key.append(s[0])
count = 0
flag = False
cur = s[0]
for i in range(len(s)):
    if cur == s[i]:
        count+=1
    else:
        cur = s[i]
        key.append(s[i])
        val.append(count)
        count = 1
val.append(count)
while len(key)>1:
    if (key[0]==key[-1]):
        key.pop(0)
        key.pop(-1)
        val.pop(0)
        val.pop(-1)
    else:
        flag = True
        break
res = 0
if flag:
    for i in range(len(val)):
        res +=val[i]
    print(res)
else:
    if val[0]>1:
        print(0)
    else:
        print(1)