s = list(map(int, input().split()))
min_n = 1000000000000000000000000000000000000000000000000
for i in range(len(s)):
    if s[i]%2==1:
        min_n = min(min_n, s[i])
if min_n!=1000000000000000000000000000000000000000000000000:
    print(min_n)
else:

    print(0)