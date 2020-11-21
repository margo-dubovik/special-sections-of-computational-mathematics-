import array as arr
import long_basic as lb
import time

# print("insert power of 2 for system base:")  # Initialising system base
# w = int(input())
# b = 2 ** w
# print("b=", b)
#
# print("insert hex string 1:")  # Initialising hex string
# ini_string1 = input()
#
# print("insert hex string 2:")
# ini_string2 = input()
#
# A = lb.conv_from_hex(ini_string1, b)
# B = lb.conv_from_hex(ini_string2, b)
#
# lb.remove_start_zeros(A)
# lb.remove_start_zeros(B)
#

def is_even(N):
    l = len(N)
    if N[l - 1] % 2 == 0:  # last number is a multiple of 2 --> number is even
        return 1
    else:
        return 0  # else: odd


def abs_substraction(A1, B1, c):  # c - system base
    if len(A1) != len(B1):
        lb.equalize(A1, B1)
    n = len(A1)
    if lb.comparison(A1, B1) == -1:  # A<B
        D = lb.substraction(B1, A1, c)
    else:
        D = lb.substraction(A1, B1, c)
    return D


def min_number(A1, B1):
    if lb.comparison(A1, B1) == -1:  # A<B
        return A1
    else:
        return B1


def division_bin(A1, B1):  # division of binary input
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
        R = lb.substraction(R, C1, 2)
        lb.remove_start_zeros(R)
        d = lb.degree_of_two_bin_array(t - k)  # d = 2^(t-k) in binary
        Q = addition_bin(Q, d)
    return Q, R


def addition_bin(A, B):
    if len(A) != len(B):
        lb.equalize(A, B)
    n = len(A)
    C = arr.array('I', [])
    carry = 0
    for i in reversed(range(n)):
        temp = A[i] + B[i] + carry
        C.insert(0, temp & (1))
        carry = temp >> 1
    if carry != 0:
        C.insert(0, carry)  # if the result is bigger than the incomes
    return C


def mulOneDigit_bin(A, d):
    C = arr.array('I', [])
    n = len(A)
    carry = 0
    for i in reversed(range(n)):
        temp = A[i] * d + carry
        C.insert(0, temp & 1)
        carry = temp >> 1
    C.insert(0, carry)
    return C


def mul_bin(A, B):
    if len(A) != len(B):
        lb.equalize(A, B)
    n = len(A)
    C = arr.array('I', [])
    j = 0
    for i in reversed(range(n)):
        temp = mulOneDigit_bin(A, B[i])
        t = j
        while t > 0:
            temp.append(0)
            t = t - 1
        C = addition_bin(C, temp)
        j = j + 1
    return C


def gcd(X1, Y1):  # Greatest Common Divisor. input&output are binary
    lb.remove_start_zeros(X1)
    lb.remove_start_zeros(Y1)
    d = arr.array('I', [1])
    X = X1[:]
    Y = Y1[:]
    while (is_even(X) & is_even(Y)) == 1:  # while X&Y are even
        del X[-1]  # remove last item which is нщгтпуые = X/2
        del Y[-1]  # Y/2
        d.append(0)  # d*2 = add zero to the end
    while is_even(X) == 1:  # while X is even
        del X[-1]
    while lb.comparison(Y, [0]) != 0:  # while Y != 0
        while is_even(Y) == 1:  # while Y is even
            del Y[-1]
        X2 = min_number(X, Y)
        lb.remove_start_zeros(X2)
        Y2 = abs_substraction(X, Y, 2)
        lb.remove_start_zeros(Y2)
        return lb.remove_start_zeros(mul_bin(d, gcd(X2, Y2)))
    d = mul_bin(d, X)
    return d


# lcm(a,b) = (a*b)/gcd(a,b)
def lcm(X1, Y1):  # Least Common Multiplier. input&output binary
    lb.remove_start_zeros(X1)
    lb.remove_start_zeros(Y1)
    d = gcd(X1, Y1)
    l_1 = mul_bin(X1, Y1)
    l = division_bin(l_1, d)[0]
    return l

#
# A_conv = lb.convert_to_bin(A)
# B_conv = lb.convert_to_bin(B)
#
# start = time.time()
# GCD = gcd(A_conv, B_conv)
# end = time.time()
# print("GCD time (sec):", end - start)
# print("gcd:", lb.conv_to_hex(lb.convert_from_bin(GCD)))
#
# start = time.time()
# LCM = lcm(A_conv, B_conv)
# end = time.time()
# print("LCM time (sec):", end - start)
# print("lcm:", lb.conv_to_hex(lb.convert_from_bin(LCM)))


def conv_from_int(n, b):  # decimal number to 2^w number
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % b)  # take remainder of division and add it leftmost of the array
        n = n // b
    return number


def miu(N):  # miu = (b**2k)%N
    lb.remove_start_zeros(N)
    k = len(N)
    b_arr = arr.array('I', [1, 0])
    k_1 = conv_from_int(2 * k, b)
    b_1 = lb.degree_of_long(b_arr, k_1)  # b**(2*k)
    lb.remove_start_zeros(b_1)
    return lb.convert_from_bin(lb.division(b_1, N)[0])


def remove_last_digits(X, l):  #remove last l digits from X
    k = len(X)
    X1 = X[:(k - l)]
    return X1


def barrett_reduction(X, N):  # r = X mod N, M=miu(N)
    lb.remove_start_zeros(N)
    M = miu(N)
    lb.remove_start_zeros(X)
    lb.remove_start_zeros(N)
    k = len(N)
    if len(X) < 2 * k:
        while len(X) != 2 * k:  # so that |N|=k, |X|=2k
            X.insert(0, 0)
    else:
        while len(X) != 2 * k:  # so that |N|=k, |X|=2k
            N.insert(0, 0)
            k += 1
    Q = remove_last_digits(X, k - 1)
    Q = lb.mul(Q, M)
    Q = remove_last_digits(Q, k + 1)
    t = lb.mul(Q, N)
    R = lb.substraction(X, t, b)
    while lb.comparison(R, N) != -1:
        R = lb.substraction(R, N, b)
        lb.remove_start_zeros(R)
    print("e")
    return R


def addition_modular(X1, Y1, N):
    X = barrett_reduction(X1, N)
    Y = barrett_reduction(Y1, N)
    Z1 = lb.addition(X, Y)
    Z = barrett_reduction(Z1, N)
    return Z


def substraction_modular(X1, Y1, N):
    #  X = barrett_reduction(X1, N)
    #  Y = barrett_reduction(Y1, N)
    Z1 = abs_substraction(X1, Y1, b)
    Z = barrett_reduction(Z1, N)
    return Z


def mul_modular(X1, Y1, N):
    X = barrett_reduction(X1, N)
    Y = barrett_reduction(Y1, N)
    Z1 = lb.mul(X, Y)
    Z = barrett_reduction(Z1, N)
    return Z


def square_modular(X1, N):
    X = barrett_reduction(X1, N)
    Z1 = lb.square(X)
    Z = barrett_reduction(Z1, N)
    return Z


def degree_of_long_modular(X1, Y1, N):
    X = barrett_reduction(X1, N)
    Y = lb.convert_to_bin(Y1)
    lb.remove_start_zeros(Y)
    Z = arr.array('I', [1])
    m = len(Y)
    f = 1
    for i in reversed(range(m)):
        if Y[i] == 1:
            Z = barrett_reduction(lb.mul(Z, X), N)
        X = barrett_reduction(lb.mul(X, X), N)
    return Z

#
# print("insert module for modular operations:")
# inp_module = input()
# N = lb.conv_from_hex(inp_module, b)
# # N = '2AB3786D3A85E62EC763A05A73A7F08D21EEE3CBCAE207E4085'
# # A = '3A7EF2554E8940FA9B93B2A5E822CC7BB262F4A14159E4318CA'
# # B = 'D4D2110984907B5625309D956521BAB4157B8B1ECE04043249A'
#
# lb.remove_start_zeros(A)
# lb.remove_start_zeros(B)
# lb.remove_start_zeros(N)
#
# start = time.time()
# Addition_mod = addition_modular(A, B, N)
# end = time.time()
# print("Addition time (sec):", end - start)
#
# start = time.time()
# Sub_mod = substraction_modular(A, B, N)
# end = time.time()
# print("Subtraction time (sec):", end - start)
#
# start = time.time()
# Mul_mod = mul_modular(A, B, N)
# end = time.time()
# print("Multiplication time (sec):", end - start)
#
# start = time.time()
# Square_mod = square_modular(A, N)
# end = time.time()
# print("Square time (sec):", end - start)
#
# # start = time.time()
# # Deg_mod = degree_of_long_modular(A, B, N)
# # end = time.time()
# # print("Deg time (sec):", end - start)
#
# lb.remove_start_zeros(Addition_mod)
# lb.remove_start_zeros(Sub_mod)
# lb.remove_start_zeros(Mul_mod)
# lb.remove_start_zeros(Square_mod)
# # lb.remove_start_zeros(Deg_mod)
#
#
# print("A mod B =", lb.conv_to_hex(barrett_reduction(A, B)))
# print("(A+B)mod N =", lb.conv_to_hex(Addition_mod))
# print("(A-B)mod N =", lb.conv_to_hex(Sub_mod))
# print("(A*B)mod N =", lb.conv_to_hex(Mul_mod))
# print("(A^2)mod N =", lb.conv_to_hex(Square_mod))
#
#
# # print("(A^B)mod N =", lb.conv_to_hex(Deg_mod))

def test_func():
    a_n = A_n_times(A, 110)
    test1 = lb.comparison(mul_modular(A, T, N), barrett_reduction(a_n, N))
    print("(A*T)mod N =?= (A+..+A T times)mod N: ", test1)
    test2 = lb.comparison(mul_modular(C, Addition_mod, N),
                          addition_modular(mul_modular(A, C, N), mul_modular(B, C, N), N))
    print("(A+B)*C=?=A*C+B*C:", test2)


def A_n_times(A, n):
    F = A[:]
    for i in range(n - 1):
        F = lb.addition(F, A)
    return F


# ini_stringT = '6E'
# T = lb.conv_from_hex(ini_stringT, b)
#
# print("insert hex string C for tests:")
# ini_stringC = input()
# C = lb.conv_from_hex(ini_stringC, b)
#
# test_func()
