from collections import deque
a=deque(list(map(int,input().split())))
b=deque(list(map(int,input().split())))
k=0

while len(a)!=0 and len(b)!=0 and k<10**6:
    if a[0] > b[0]:
        if a[0] != 9 or b[0] != 0:
            a.append(a.popleft())
            a.append(b.popleft())
        else:
            b.append(a.popleft())
            b.append(b.popleft())
    else:
        if b[0] != 9 or a[0] != 0:
            b.append(a.popleft())
            b.append(b.popleft())
        else:
            a.append(a.popleft())
            a.append(b.popleft())
    k+=1
    if k >= 10**6:
        print("botva")
    elif len(a) == 0:
        print("second",k)
    elif len(b) == 0:
        print("first",k)