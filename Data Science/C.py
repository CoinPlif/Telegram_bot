case = int(input())
for case in range(case):
    mit,mat, step = list(map(int, input().split()))
    s, f= list(map(int, input().split()))
    if s==f:
        print(0)
    elif abs(f-s)>=step:
        print(1)
    elif (s+step>mat and s-step<mit) or (f+step>mat and f-step<mit):
        print(-1)
    else:
        if s+step<=f+step<=mat or f+step<=s+step<=mat or f-step>=s-step>=mit or s-step>=f-step>=mit:
            print(2)
        else:
            print(3)
