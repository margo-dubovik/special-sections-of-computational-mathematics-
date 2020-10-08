import array as arr

# Initialising system base
print("insert power of 2 for system base:")
w = int(input())
b = 2 ** w
print("b=", b)

# Initialising hex string
print("insert hex string 1:")
ini_string1 = input()

print("insert hex string 2:")
ini_string2 = input()


# Converting hex to 2^w
def conv_from_hex(hex, b):
    n = int(hex, 16)
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % b)  # take remainder of division and add it leftmost of the array
        n = n // b
    return number


def conv_to_hex(num):
    n = len(num)
    hex_new = 0
    for i in reversed(range(0, n)):
        hex_new = num[i] * b ** (n - i - 1) + hex_new
    hex_new = hex(hex_new)[2:]  # position from 2 to the end
    return hex_new


A = conv_from_hex(ini_string1, b)
B = conv_from_hex(ini_string2, b)
# Print the result as a string
#print("A=", "".join(map(str, A)), "B=", "".join(map(str, B)))


# Equalize two numbers` length
def equalize(A, B):
    if len(A) > len(B):
        while len(A) != len(B):
            B.insert(0, 0)  # add zeros to the beginning to equal the length
    else:
        while len(A) != len(B):
            A.insert(0, 0)


def addition(A, B):
    if len(A) != len(B):
        equalize(A, B)
    #    print("A=", A)
    #    print("B=", B)
    n = len(A)
    C = arr.array('I', [])
    carry = 0
    for i in reversed(range(n)):
        temp = A[i] + B[i] + carry
        C.insert(0, temp & (b - 1))  # WHY??????????
        carry = temp >> w
    if carry != 0:  C.insert(0, carry)  # if the result is bigger than the incomes

    return C


# C = addition(A, B)
# print("A+B=", "".join(map(str, conv_to_hex(C))))

def substraction(A, B, c):
    if len(A) != len(B):
        equalize(A, B)
    #    print("A=", A)
    #    print("B=", B)
    n = len(A)
    D = arr.array('i', [])
    if comparison(A, B) == -1:  # A<B
        print("WRONG INPUT!!! A<B")
    else:
        borrow = 0
        for i in reversed(range(n)):
            temp = A[i] - B[i] - borrow
            if temp >= 0:
                D.insert(0, temp)
                borrow = 0
            else:
                D.insert(0, c + temp)
                borrow = 1
    return D


# D = substraction(A, B)
# print("A-B=", conv_to_hex(D))

def comparison(n_1, n_2):
    if len(n_1) > len(n_2):
        while len(n_1) != len(n_2):
            n_2.insert(0, 0)  # add zeros to the beginning to equal the length
    else:
        while len(n_1) != len(n_2):
            n_1.insert(0, 0)
    n = len(n_1)
    i = 0
    while n_1[i] == n_2[i]:
        i += 1
        if (i == n - 1):  # if equal
            return 0
    if n_1[i] > n_2[i]:  # if n_1 > n_2
        return 1
    else:
        return -1  # if n_1 < n_2


# print("A<B:", comparison(A,B))
# print("A>B:", comparison(B,A))
# print("A=B", comparison(B,B))

def mulOneDigit(A, d):
    C = arr.array('I', [])
    n = len(A)
    carry = 0
    for i in reversed(range(n)):
        temp = A[i] * d + carry
        C.insert(0, temp & (b - 1))
        carry = temp >> w
    C.insert(0, carry)
    return C


def mul(A, B):
    if len(A) != len(B):
        equalize(A, B)
    n = len(A)
    C = arr.array('I', [])
    j = 0
    for i in reversed(range(n)):
        temp = mulOneDigit(A, B[i])
        t = j
        while t > 0:
            temp.append(0)
            t = t - 1
        #   print("temp=", temp)
        C = addition(C, temp)
        j = j + 1
    return C


def square(A):
    C = mul(A, A)
    return C



def convert_to_bin(A):
    B = arr.array('I', [])
    n = len(A)
    for i in range(n):
        c = bin(A[i])
        conv = [int(x) for x in c[2:]]  # [2:] bcs c starts with "0b" to be understood as binary
        while len(conv) < w:
            conv.insert(0, 0)
        B.extend(conv)
    return B


def convert_from_bin(A):
    # print("w=", w)
    B = arr.array('I', [])
    n = len(A)
    while (n % w) > 0:  # make A the right length
        A.insert(0, 0)
        n += 1
    for i in range(n // w):
        beg = A[:w]  # slice first 3 values to turn into one number
        A = A[w:]
        s = "".join(map(str, beg))  # turn elements to strings & join --> binary number
        s = int(s, 2)
        B.append(s)
    return B


def degree_of_two_bin_array(A):
    conv = [0 for i in range(A + 1)]
    conv[0] = 1
    return conv


def ext(Arr, l):  # to extend the erray with given amount of zeros
    Arr1 = Arr[:]
    for j in range(l):
        Arr1.append(0)
    return Arr1


def remove_start_zeros(ar):  # remove zeros from the beginning of the word
    if len(ar) == 1 and ar[0] == 0:
        return ar
    else:
        while ar[0] == 0:
            if len(ar) == 1 and ar[0] == 0:
                return ar
            else:
                del ar[0]
        if ar[0] != 0: return ar


def division(A1, B1):
    A1 = convert_to_bin(A1)
    B1 = convert_to_bin(B1)
    remove_start_zeros(A1)
    remove_start_zeros(B1)
    k = len(B1)
    R = A1[:]  # copy A1 to R
    Q = arr.array('I', [])
    while comparison(R, B1) >= 0:  # R>=B
        remove_start_zeros(R)
        remove_start_zeros(B1)
        t = len(R)
        C1 = ext(B1, t - k)  # shifting
        if comparison(R, C1) == -1:  # R<C
            t = t - 1  # return on 1 bit back
            C1 = ext(B1, t - k)  # shifting
        R = substraction(R, C1, 2)
        remove_start_zeros(R)
        d = degree_of_two_bin_array(t - k)  # d = 2^(t-k) in binary
        Q = addition(Q, d)
    return Q, R


def degree_of_long(A1, B1):
    B1 = convert_to_bin(B1)
    # remove_start_zeros(A1)   #(надо?)
    remove_start_zeros(B1)
    m = len(B1)
    C1 = arr.array('I', [1])
    for i in reversed(range(m)):
        if B1[i] == 1:
            C1 = mul(C1, A1)
        A1 = mul(A1, A1)
    return C1


Addition = addition(A, B)
Sub = substraction(A, B, b)
Mul = mul(A, B)
Div = division(Mul, B)
#Deg = degree_of_long(A, B)

print("A+B=", "".join(map(str, conv_to_hex(Addition))))
print("A+B=", conv_to_hex(Addition))
print("A-B=", conv_to_hex(Sub))
print("AxB=", conv_to_hex(Mul))
print("A/B=", conv_to_hex(convert_from_bin(division(A, B)[0])))
print("(A*B)/B=", conv_to_hex(convert_from_bin(Div[0])))
#print("A^B=", conv_to_hex(Deg))
print("A^2=", conv_to_hex(square(A)))
