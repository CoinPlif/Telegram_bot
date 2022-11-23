events = []
vares = []
print('values of events: ')
events = list(map(float, input().split()))
print('veraity of an event: ')
vares = list(map(float, input().split()))
E_X = 0
E_sqX = 0
for i in range(len(events)):
    E_X += events[i]*vares[i]
    E_sqX += vares[i]*(events[i]**2)
Var_X = E_sqX - E_X**2
print('edges: ')
edges = list(map(float,input().split()))
print('number: ')
number = int(input())
s = ""
for i in range(len(edges)):
    s += f'edge_{i+1} = {(edges[i]-(E_X*number))/((Var_X*number)**0.5)} '
print(f'E_X = {E_X} E_sqX = {E_sqX} Var_X = {Var_X}')
print(s)
