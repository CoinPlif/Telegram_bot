case = int(input())
for case in range(case):
    n = int(input())
    s = list(map(int, input().split()))
    mas = []
    for i in range(1,n+1):
        if i in s:
            mas.append(i)
    s.sort()
    newmas = []
    for i in range(n/2):
        newmas.append(mas[i])
        newmas.append(s[i])
    resmas = []
    for i in range(n/2):
        resmas.append(max(newmas[i], newmas[i+1]))
