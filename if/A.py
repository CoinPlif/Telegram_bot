case = int(input())
for case in range(case):
    n = int(input())
    s = list(map(int, input().split()))
    if s[0] ==1:
        print('yes')
    else:
        print('no')