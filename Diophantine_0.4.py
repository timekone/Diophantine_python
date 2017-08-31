from functools import reduce
import time

start = time.time()
input_name = "input.txt"


def GCD(a, b):  # It takes too long!
    if b == 0:
        return a
    else:
        return GCD(b, a % b)


def Min_m(arr):
    """
    Choose equation with min m=k*l+r
    where k - number of positive coefficients, l - negative,
    r - zeroes
    :param arr: array of equations
    :return: equation with min m
    """
    m_arr = []
    for vec in arr:
        k = 0
        l = 0
        r = 0
        for a in vec:
            if a > 0:
                k += 1
            elif a < 0:
                l += 1
            else:
                r += 1
        m_arr.append(k*l+r)
    return arr[m_arr.index(min(m_arr))]


def redundant(ar):
    ar2 = []  # = list(ar)
    """
    delete redundant vectors
    """
    jjs = range(len(ar))
    decar = []  # array of decimal representations converted from binaries
    for y in ar:
        binstr = ''  # binary representation of vector
        for c in y:
            if c != 0:
                binstr = binstr + '1'
            else:
                binstr = binstr + '0'
        decar.append(int(binstr, 2))
    for j in jjs:
        r = True  # do we need ar[j]
        for k in jjs:
            an = decar[j] & decar[k]
            if an == decar[k] and j != k:
                r = False
                break
        if r:
            ar2.append(ar[j])
    return ar2


def redundant2(ar):
    ar2 = []
    strings = []
    iis = range(len(ar[0]))
    for j in range(len(ar)):
        zcounter = 0
        s = ''
        for i in iis:
            if ar[j][i] == 0:
                zcounter += 1
                s = s + '0'
            else:
                s = s + '1'
        if zcounter > len(input_arr):
            ar2.append(ar[j])
            strings.append(s)
    #return ar2
    ar3 = []
    strings2 = []
    for j in range(len(ar2)):
        if strings[j] not in strings2:
            ar3.append(ar2[j])
            strings2.append(strings[j])
    return ar3


def simplify(ar):
    ar2 = []
    for y in ar:
        d = reduce(GCD, y)  # move from here, after redundant
        if d != 1 and d != 0:
            y = list(map(lambda t: t//d, y))
        ar2.append(y)
    return ar2


def set_basis(arr):
    basis = []
    for p in range(len(arr)):
        basis.append([])
        for o in range(len(arr)):
            if p == o:
                basis[p].append(1)
            else:
                basis[p].append(0)
    return basis

""""
input_arr = [[4, 2, -3, -2, -1], gd
             [2, -1, -4, 1, 5],
             [0, 2, 4, 0, -9]]
sdp77@i.ua  10:00  15.12.2016
"""
"""
input_arr = [[2, -1, 3, 1, -4, 2], 
             [1, 0, -2, -3, 2, 1],
             [-3, 1, 1, 0, -1, 2],
             [4, 1, -1, -2, 0, 1]]
"""

input_arr = []
with open(input_name) as input_file:
    for line in input_file:
        l = line.split()
        int_l = []
        for ch in l:
            int_l.append(int(ch))
        input_arr.append(int_l)

for i in range(len(input_arr)):
    """
    diagonilize input matrix
    """
    if input_arr[i][i] == 0:
        t = 0
        while i+t+1 < len(input_arr) and input_arr[i+t][i] == 0:
            t += 1
        c = input_arr[i]
        input_arr[i] = input_arr[i + t]
        input_arr[i + t] = c
        if input_arr[i][i] == 0:
            break
    for j in range(0, i):
        if input_arr[j][i] != 0:
            input_arr[j] = list(map(lambda x, y: x * input_arr[i][i] - y * input_arr[j][i], input_arr[j], input_arr[i]))
    for j in range(i+1, len(input_arr)):
        if input_arr[j][i] != 0:
            input_arr[j] = list(map(lambda x, y: x * input_arr[i][i] - y * input_arr[j][i], input_arr[j], input_arr[i]))

input_arr = simplify(input_arr)
f_arr = Min_m(input_arr)  # choosing equation with min m
input_arr.remove(f_arr)
#print(cur_eq)

basis = set_basis(f_arr)  # setting canon basis for given equation
"""[[1, 0, 0, 0, 0], #basis = x
         [0, 1, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 0, 1, 0],
         [0, 0, 0, 0, 1],]

basis = [[1, 0, 0, 0, 0, 0], #basis = x
         [0, 1, 0, 0, 0, 0],
         [0, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0],
         [0, 0, 0, 0, 1, 0],
         [0, 0, 0, 0, 0, 1],]
         """
#f_arr = []
#for e in range(len(basis)):            # appends value of equation with substituted basis
#    f_arr.append(basis[e][e]*cur_eq[e])  # TODO maybe just cur_eq[e], since basis[e][e] always 1?

# TODO check if not all zeroes, positive or negative only

x = []
#print(str(f_arr)+'\n')


"""
if value of eq is zero, add corresponding basis vector to answer
otherwise for every pair of ei and ej, add y = -L(ei)*ej + L(ej)*ei, where ej - basis for which L>0, ei - for which L<0
"""
for i in range(len(f_arr)):
    if f_arr[i] == 0:
        x.append(basis[i])
    elif f_arr[i] < 0:
        for j in range(len(f_arr)):
            if f_arr[j] > 0:
                l1 = list(map(lambda x: x*-f_arr[i], basis[j]))
                l2 = list(map(lambda x: x*f_arr[j], basis[i]))
                y = list(map(lambda a1, a2: a1+a2, l1, l2))
                d = reduce(GCD, y)  # find greatest common divider of vector..
                if d != 1:  # and if it is not 1..
                    y = list(map(lambda x: x//d, y))  # simplify vector
                x.append(y)
#print(x)

while len(input_arr) > 0:
    f_arr = []
    for e in input_arr:  # for each equation left..
        fn = []
        for xn in x:  # substitute every answer vector
            fx = 0
            for a in range(len(xn)):
                fx += xn[a]*e[a]
            fn.append(fx)
        f_arr.append(fn)
    cur_eq2 = Min_m(f_arr)
    input_arr.__delitem__(f_arr.index(cur_eq2))
    print('{0} {1}'.format(len(cur_eq2),len(input_arr)))
    x2 = []
    for i in range(len(cur_eq2)):
        if cur_eq2[i] == 0:
            x2.append(x[i])
        elif cur_eq2[i] < 0:
            for j in range(len(cur_eq2)):
                if cur_eq2[j] > 0:
                    l1 = list(map(lambda t: t * -cur_eq2[i], x[j]))
                    l2 = list(map(lambda t: t*cur_eq2[j], x[i]))
                    y = list(map(lambda a1, a2: a1+a2, l1, l2))
                    x2.append(y)
    print(len(x2))
    print('start r2')
    x2 = redundant2(x2)
    print(len(x2))
    print('start r')
    x2 = redundant(x2)
    print('finish r')
    print(len(x2))
    x2 = simplify(x2)
    #print(x2)
    x = x2

end = time.time()

with open("output.txt", "w") as output_file:
    for xv in x2:
        output_file.write(str(xv)+'\n')
    output_file.write(str(end-start))
print(x2)