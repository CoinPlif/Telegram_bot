n = list(map(int, input().split()))
x=n[0]
y=n[1]
n=n[2]
left = 0
right = max(x,y)*n+1
while right-left>1:
    mid =int((right +left)/2)
    if int(mid/x)*int(mid/y)>=n:
        right = mid
    else:
        left = mid
print(right)