from functools import reduce
import time
import datetime

start = time.time()
input_name = "generated.txt"


def GCD(a, b):  # Greatest Common Divisor
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
    m_arr = []  # list with values of m for each equation
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
    return arr[m_arr.index(min(m_arr))]  # index of min m equals to index of its equation


def redundant2(ar, input_len):
    """
    delete redundant vectors
    """
    ar2 = []  # for storing halfway solutions
    strings = []
    for j in range(len(ar)):  # searching for vectors with number of zero coordinates greater then number of vectors
        zerocounter = 0  # number of zero coordinates in a single vector
        binstr = ''  # binary representation of vector
        for i in range(len(ar[0])):
            if ar[j][i] == 0:
                zerocounter += 1
                binstr = binstr + '0'
            else:
                binstr = binstr + '1'
        if zerocounter > input_len:
            ar2.append(ar[j])
            strings.append(binstr)  # saving binary representation for later
    ar3 = []  # copying is faster than deleting
    strings2 = []
    for j in range(len(ar2)):  # eliminating vectors without unique bin. representation
        if strings[j] not in strings2:
            ar3.append(ar2[j])
            strings2.append(strings[j])

    """
    redundant with bool optimisation(old redundant)
    """
    decimal_ar = []
    for binstr in strings2:
        decimal_ar.append(int(binstr, 2))  # translating binary representation to decimal
    ar2 = []  # reusing ar2 to save memory
    jjs = range(len(ar3))  # not calculating same thing again
    for j in jjs:
        r = True  # do we need ar[j]
        for k in jjs:
            if j != k:  # are these different vectors
                an = decimal_ar[j] & decimal_ar[k]  # AND between binary representations of vectors
                if an == decimal_ar[k]:  # if [j] has 1's where [k] has 0's, e.g. [j] redundant to [k]
                    r = False
                    break
        if r:
            ar2.append(ar3[j])  # add if we still need this vector
    return ar2


def simplify(ar):
    """
    simplifying vectors of matrix
    :param ar: matrix of vectors
    :return: ar2: simplified matrix
    """
    ar2 = []  # for storing result(faster than deleting)
    for y in ar:
        d = reduce(GCD, y)  # searching for greatest common divisor
        if d != 1 and d != 0:
            y = list(map(lambda t: t//d, y))  # dividing by GCD
        ar2.append(y)  # append to answer
    return ar2


def set_basis(arr):
    """
    creating canonical basis matrix
    :param arr: matrix
    :return: basis
    """
    basis = []
    for p in range(len(arr)):
        basis.append([])
        for o in range(len(arr)):  # putting 1's on diagonal
            if p == o:
                basis[p].append(1)
            else:
                basis[p].append(0)
    return basis


def work(input_arr):
    """
    primary function
    :param input_arr:
    :return: x: TSS-solutions
    """
    for i in range(len(input_arr)):
        """
        diagonalize input matrix
        """
        if input_arr[i][i] == 0:  # search for vector with not zero on diagonal
            t = 0
            while i + t + 1 < len(input_arr) and input_arr[i + t][i] == 0:
                t += 1
            c = input_arr[i]  # switch places
            input_arr[i] = input_arr[i + t]
            input_arr[i + t] = c
            if input_arr[i][i] == 0:
                break
        """
        subtract vectors
        """
        for j in range(0, i):
            if input_arr[j][i] != 0:
                input_arr[j] = list(
                    map(lambda x, y: x * input_arr[i][i] - y * input_arr[j][i], input_arr[j], input_arr[i]))
        for j in range(i + 1, len(input_arr)):
            if input_arr[j][i] != 0:
                input_arr[j] = list(
                    map(lambda x, y: x * input_arr[i][i] - y * input_arr[j][i], input_arr[j], input_arr[i]))
        input_arr = simplify(input_arr)
    f_arr = Min_m(input_arr)  # choosing equation with min m
    input_arr.remove(f_arr)
    basis = set_basis(f_arr)  # setting canon basis for given equation
    x = []  # for storing answer
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
                    l1 = list(map(lambda x: x * -f_arr[i], basis[j]))
                    l2 = list(map(lambda x: x * f_arr[j], basis[i]))
                    y = list(map(lambda a1, a2: a1 + a2, l1, l2))
                    d = reduce(GCD, y)  # find greatest common divider of vector..
                    if d != 1:  # and if it is not 1..
                        y = list(map(lambda x: x // d, y))  # simplify vector
                    x.append(y)

    while len(input_arr) > 0:
        f_arr = []
        for e in input_arr:  # for each equation left..
            fn = []
            for xn in x:  # substitute every answer vector
                fx = 0
                for a in range(len(xn)):
                    fx += xn[a] * e[a]
                fn.append(fx)
            f_arr.append(fn)
        cur_eq2 = Min_m(f_arr)  # choose equation with min m=k*l+r on f_arr values
        input_arr.__delitem__(f_arr.index(cur_eq2))
        x2 = []
        """
        searching for TSS-solutions
        """
        for i in range(len(cur_eq2)):
            if cur_eq2[i] == 0:  # if zero just add to solutions
                x2.append(x[i])
            elif cur_eq2[i] < 0:  # otherwise combining positive with negative
                for j in range(len(cur_eq2)):
                    if cur_eq2[j] > 0:
                        l1 = list(map(lambda t: t * -cur_eq2[i], x[j]))
                        l2 = list(map(lambda t: t * cur_eq2[j], x[i]))
                        y = list(map(lambda a1, a2: a1 + a2, l1, l2))
                        x2.append(y)
        print('start r2: ' + str(len(x2)))  # length before elimination of redundant vectors
        x2 = redundant2(x2, len(input_arr))
        print('finish r2: ' + str(len(x2)))  # after elimination
        x2 = simplify(x2)
        x = x2
    return x


input_arr = []
with open(input_name) as input_file:
    """
    read input matrix
    """
    for line in input_file:
        l = line.split()
        int_l = []
        for ch in l:
            int_l.append(int(ch))
        input_arr.append(int_l)

x2 = work(input_arr)  # find TSS-solutions

end = time.time()

with open("output.txt", "a") as output_file:
    output_file.write('============================[ ' + str(datetime.datetime.today()) + ' ]====================================\n')
    output_file.write(input_name + '\n')
    output_file.write(str(end-start) + '\n')
    # for xv in x2:
    #     output_file.write(str(xv)+'\n')
print(x2)
