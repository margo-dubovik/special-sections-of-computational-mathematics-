import array as arr
import long_basic as lb

print("insert power of 2 for system base:")  # Initialising system base
w = int(input())
b = 2 ** w
print("b=", b)

print("insert hex string 1:")  # Initialising hex string
ini_string1 = input()

print("insert hex string 2:")
ini_string2 = input()

A = lb.conv_from_hex(ini_string1, b)
B = lb.conv_from_hex(ini_string2, b)


def is_even(N):
    l = len(N)
    if N[l - 1] % 2 == 0:   # last number is a multiple of 2 --> number is even
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
        C.insert(0, temp & (1))
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
        del X[-1]  # remove last item which 1s zero = X/2
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

A_conv = lb.convert_to_bin(A)
B_conv = lb.convert_to_bin(B)
print("gcd:", lb.conv_to_hex(lb.convert_from_bin(gcd(A_conv, B_conv))))
print("lcm:", lb.conv_to_hex(lb.convert_from_bin(lcm(A_conv, B_conv))))

def conv_from_int(n, b):
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % b)  # take remainder of division and add it leftmost of the array
        n = n // b
    return number

def miu(N): #miu = (b**2k)%N
    lb.remove_start_zeros(N)
    k = len(N)
    b_arr = arr.array('I', [1, 0])
    k_1 = conv_from_int(2*k, b)
    b_1 = lb.degree_of_long(b_arr, k_1)   #b**(2*k)
    lb.remove_start_zeros(b_1)
    return lb.convert_from_bin(lb.division(b_1, N)[0])


def remove_last_digits(X, l):
    k = len(X)
    X1 = X[:(k - l)]
    return X1


def barrett_reduction(X, N, M):  # r = XmodN, M=miu(N)
    #    print("miu=", M)
    lb.remove_start_zeros(X)
    lb.remove_start_zeros(N)
    k = len(N)
    while len(X) != 2 * k:  # so that |N|=k, |X|=2k
        X.insert(0, 0)
    Q = remove_last_digits(X, k - 1)
    Q = lb.mul(Q, M)
    Q = remove_last_digits(Q, k + 1)
    t = lb.mul(Q, N)
    R = lb.substraction(X, t, b)
    while lb.comparison(R, N) != -1:
        R = lb.substraction(R, N, b)
    return R


print("A mod B =", lb.conv_to_hex(barrett_reduction(A, B, miu(B))))
