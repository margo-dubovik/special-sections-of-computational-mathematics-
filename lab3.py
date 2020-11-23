# GF(2^m). m=251.
# generator: f = x^251 + x^14 + x^4 + x + 1.

import array as arr
import long_modular as lm
import long_basic as lb


m = 251

def generate_by_degs(deg_vec):
    pol = arr.array('I', [])
    s = set(deg_vec)
    n = deg_vec[0]
    for i in range (n+1):
        if i in s:
            pol.insert(0, 1)
        else:
            pol.insert(0, 0)
    return pol


def print_as_polynomial(deg_vec):
    str_pol = ""
    s = set(deg_vec)
    n = deg_vec[0]
    for i in reversed(range (n+1)):
        if i in s:
            str_pol = str_pol + f" x^{i} +"
    str_pol = str_pol[:-1]
    return str_pol


def bin_str_to_arr(num):
    number = arr.array('I', [])
    for i in range(len(num)):
        number.append(int(num[i], 2))
    return number


def hex_str_to_arr(num):
    n = int(num, 16)
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % 2)  # take remainder of division and add it leftmost of the array
        n = n // 2
    return number


def arr_to_hex_str(num):
    number = hex(int(num, 2))[2:]
    if len(number) < 64:
        while len(number) != 64:
            number = '0' + number
    return number


def insert_numbers():
    print("Bin(1) ot Hex(2)?")
    sys = input()
    if sys == '1':
        print("Insert bin A:")
        x = bin_str_to_arr(input())
        print("Insert bin B:")
        y = bin_str_to_arr(input())
        print("Insert bin N:")
        z = bin_str_to_arr(input())
    elif sys == '2':
        print("Insert hex A:")
        x = hex_str_to_arr(input())
        print("Insert hex B:")
        y = hex_str_to_arr(input())
        print("Insert hex N:")
        z = hex_str_to_arr(input())
    else:
        print("WRONG INPUT. TRY AGAIN")
        insert_numbers()
    return x, y, sys, z



def division_bin_pol(A1, B1):  # division of binary input
    lb.remove_start_zeros(A1)
    lb.remove_start_zeros(B1)
    k = len(B1)
    R = A1[:]  # copy A1 to R
    Q = arr.array('I', [])
    while lb.comparison(R, B1) >= 0:  # R>=B
        lb.remove_start_zeros(R)
        lb.remove_start_zeros(B1)
        t = len(R)
        C1 = lb.ext(B1, t - k)  # shifting
        if lb.comparison(R, C1) == -1:  # R<C
            t = t - 1  # return on 1 bit back
            C1 = lb.ext(B1, t - k)  # shifting
        R = addition_pol(R, C1)
        lb.remove_start_zeros(R)
        d = lb.degree_of_two_bin_array(t - k)  # d = 2^(t-k) in binary
        Q = addition_pol(Q, d)
    return Q, R

def mod_f(x):
    z = division_bin_pol(x, f)[1]
    if len(z) > 251 and z[0] == 0:
        z = z[1:]
    if len(z) <251:
        while len(z) != 251:
            z.insert(0, 0)
    return z

def addition_pol(x, y):
    if len(x) != len(y):
        lb.equalize(x, y)
    n = len(x)
    z = arr.array('I', [])
    for i in reversed(range(n)):
        temp = x[i] + y[i]
        z.insert(0, temp & 1)
    if len(z) < 251:
        while len(z) != 251:
            z.insert(0, 0)
    return z


def mul_pol(x, y):
    if len(x) != len(y):
        lb.equalize(x, y)
    n = len(x)
    c = arr.array('I', [])
    j = 0
    for i in reversed(range(n)):
        temp = lm.mulOneDigit_bin(x, y[i])
        t = j
        while t > 0:
            temp.append(0)
            t = t - 1
        c = addition_pol(c, temp)
        j = j + 1
    z = mod_f(c)
    return z

def square_pol(x):
    y = x[:]
    for i in range(0, 2 * len(y) - 2, 2):
        y.insert(i+1, 0)
    z = mod_f(y)
    return z

def trace_pol(x):
    tr = x[:]
    c = x[:]
    for i in range(m-1):
        c = square_pol(c)
        tr = addition_pol(tr, c)
    tr = mod_f(tr)
    lb.remove_start_zeros(tr)
    return tr

def inv_by_mul(x):
    z = x[:]
    y = x[:]
    for i in range(1, m-1):
        y = square_pol(y)
        z = mul_pol(z, y)
    z = square_pol(z)
    z = mod_f(z)
    return z

def degree_of_long_pol(x, n):
    lb.remove_start_zeros(x)
    lb.remove_start_zeros(n)
    l = len(n)
    z = arr.array('I', [1])
    for i in reversed(range(l)):
        if n[i] == 1:
            z = mul_pol(z, x)
        x = square_pol(x)
    return z



f_degs = arr.array('I', [251, 14, 4, 1, 0])
f = generate_by_degs(f_degs) #polynomial-generator in polynomial basis
#print(f)

inserted_values = insert_numbers()
a = inserted_values[0]
b = inserted_values[1]
sys = inserted_values[2]
n = inserted_values[3]

f_as_str = print_as_polynomial(f_degs)
print("polynomial-generator:", f_as_str)

addition = addition_pol(a, b)
multiplication = mul_pol(a,b)
square = square_pol(a)
trace = trace_pol(a)
inv = inv_by_mul(a)
degr = degree_of_long_pol(a, n)

addition_str = ''.join(map(str, addition))
multiplication_str = ''.join(map(str, multiplication))
square_str = ''.join(map(str, square))
trace_str = ''.join(map(str, trace))
inv_str = ''.join(map(str, inv))
degr_str = ''.join(map(str, degr))


if sys == '1':
    print("A+B=", addition_str)
    print("A*B=", multiplication_str)
    print("A^2=", square_str)
    print("Tr(A)=", trace_str)
    print("A^-1=", inv_str)
    print("A^N=", degr_str)
else:
    print("A+B hex=", arr_to_hex_str(addition_str))
    print("A*B hex=", arr_to_hex_str(multiplication_str))
    print("A^2=", arr_to_hex_str(square_str))
    print("Tr(A)=", trace_str)
    print("A^-1=", arr_to_hex_str(inv_str))
    print("A^N=", arr_to_hex_str(degr_str))


