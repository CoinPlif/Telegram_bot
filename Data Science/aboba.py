s = list(map(int, input().split()))
if len(s)!=1:
    for i in range(1,len(s)):
        if s[i-1]*s[i]>0:
            print(s[i-1], s[i])
            break