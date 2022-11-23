def Check(mid, number_paper, x, y):
    papers = 1+int((mid-min(x,y))/x)+int((mid-min(x,y))/y)
    #print(int((mid-min(x,y))/x),int((mid-min(x,y))/y))
    if papers>=number_paper:
        return True
    else:
        return False



n=list(map(int,input().split()))
number_paper = n[0]
x = n[1]
y = n[2]
left = 0
right = number_paper * max(x,y)+1
if number_paper == 1:
    print(min(x,y))
else:
    while right-left>1:
        mid=int((right+left)/2)
        #print(f"time={mid} res={Check(mid, number_paper, x, y)}")
        if (Check(mid, number_paper, x, y)):
            right=mid
        else:
            left=mid
    print(right)
