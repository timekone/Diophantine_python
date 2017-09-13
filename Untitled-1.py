print('Hello world!')
def Min_m(arr):
    m_arr = []
    for vec in arr:
        k=0
        l=0
        r=0
        for a in vec:
            if a>0:
                k+=1
            elif a<0:
                l+=1
            else:
                r+=1
        m_arr.append(k*l+r)
    return arr[m_arr.index(min(m_arr))]     
def set_basis(arr):
    basis = []
    for p in range(len(arr)):
        basis.append([])
        for o in range(len(arr)):
            if p==o:
                basis[p].append(1)
            else:
                basis[p].append(0)
    return basis

input_arr = [[2,-1,3,1,-4,2],
             [1,0,-2,-3,2,1],
             [-3,1,1,0,-1,2],
             [4,1,-1,-2,0,1]]
cur_eq = Min_m(input_arr)
#print(cur_eq)

#basis= set_basis(cur_eq)
basis = [[1,0,0,0,0,0],
        [0,1,0,0,0,0],
        [0,0,1,0,0,0],
        [0,0,0,1,0,0],
        [0,0,0,0,1,0],
        [0,0,0,0,0,1,]]
f_arr=[]
for e in range(len(basis)):
    f_arr.append(basis[e][e]*cur_eq[e])

x=[]
print(f_arr)

def plus(arr1, arr2):
    r=[]
    for i in range(len(arr1)):
        r.append(arr1[i]+arr2[i])
    return r
def GCD(a, b): #It takes too long!d

    if b == 0:
        return a
    else:
        return GCD(b, a % b)
def divideonGCD(ar):
    for a in ar:
        d = reduce(GCD, a)

for i in range(len(f_arr)):
    if f_arr[i]==0:
        x.append(basis[i])
    elif f_arr[i]<0:
        for j in range(len(f_arr)):
            if f_arr[j]>0:
                y = plus(list(map(lambda x: x*-f_arr[i],basis[j])),list(map(lambda x: x*f_arr[j], basis[i])))
                x.append(y)
print(x)






