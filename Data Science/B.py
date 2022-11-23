case = int(input())
for case in range(case):
    a= list(map(int, input().split()))
    mas = list(map(int, input().split()))
    m = a[0]
    s = a[1]
    sum_m = sum(mas)
    res = sum_m+s
    flag=False
    for i in range(max(mas),100):
        if res ==(i*(i+1))//2:
            flag = True
            break
    if flag:
        print('yes')
    else:
        print('no')