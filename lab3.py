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
    elif sys == '2':
        print("Insert hex A:")
        x = hex_str_to_arr(input())
        print("Insert hex B:")
        y = hex_str_to_arr(input())
    else:
        print("WRONG INPUT. TRY AGAIN")
        insert_numbers()
    return x, y, sys



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
    z = division_bin_pol(c, f)[1]  #(x * y)mod f
    if len(z) > m and z[0] == 0:
        z = z[1:]
    if len(z) < m:
        while len(z) != m:
            z.insert(0, 0)
    return z

f_degs = arr.array('I', [251, 14, 4, 1, 0])
f = generate_by_degs(f_degs) #polynomial-generator in polynomial basis
#print(f)

inserted_values = insert_numbers()
a = inserted_values[0]
b = inserted_values[1]
sys = inserted_values[2]

f_as_str = print_as_polynomial(f_degs)
print("polynomial-generator:", f_as_str)

addition = addition_pol(a, b)
multiplication = mul_pol(a,b)

addition_str = ''.join(map(str, addition))
multiplication_str = ''.join(map(str, multiplication))


if sys == '1':
    print("A+B=", addition_str)
    print("A*B=", multiplication_str)
else:
    print("A+B hex=", arr_to_hex_str(addition_str))
    print("A*B hex =", arr_to_hex_str(multiplication_str))