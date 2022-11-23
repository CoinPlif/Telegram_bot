def check(dist, number_cows, mas):
    last_cow = mas[0]
    cows = 1
    for i in range(1, len(mas)):
        if mas[i]-last_cow>=dist:
            last_cow = mas[i]
            cows+=1
    if cows >= number_cows:
        return False
    else:
        return True

n = list(map(int, input().split()))
mas = list(map(int, input().split()))
number_cows=n[1]
number_place=n[0]
left = 0
right = mas[-1] - mas[0] + 1
while right - left > 1:
    middle = int((right+left)/2)
    if (check(middle, number_cows, mas)):
        right = middle
    else:
        left = middle
print(left)