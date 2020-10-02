import array as arr

# Initialising system base
print("insert power of 2 for system base:")
w = int(input())
b = 2 ** w
print("b=", b)

# Initialising hex string
print("insert hex string 1:")
ini_string1 = input()

#print("insert hex string 2:")
#ini_string2 = input()



# Converting hex to 2^w
def conv_from_hex(hex, b):
    d = len(hex)
    l = d//(w//4)
    number = arr.array('I', [])
    for i in range(l):
        hex_1 = hex[(d - l):]
        n = int(hex_1, 16)
        while n > 0:
            number.insert(0, n % b)  # take remainder of division and add it leftmost of the array
            n = n // b
        hex = hex[:(d - l)]
    return number

def conv_to_hex(num):
    n = len(num)
    hex_new = 0
    for i in reversed(range(0, n)):
        hex_new = hex_new + num[i] * b ** (n - i - 1)
    hex_new = hex(hex_new)[2:]  # position from 2 to the end
    return hex_new


A = conv_from_hex(ini_string1, b)
#K = conv_to_hex(A)

#print("K=", K)

if len(A) == len(K):
    print("equal")
else:
    print("unequal")
print("len A =", len(A), " len(K)=", len(K))
B = conv_from_hex(ini_string2, b)
# Print the result as a string
print("A=", "".join(map(str, A)), "B=", "".join(map(str, B)))


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
    print("A=", A)
    print("B=", B)
    n = len(A)
    C = arr.array('I', [])
    carry = 0
    for i in reversed(range(n)):
        temp = A[i] + B[i] + carry
        C.insert(0, temp & (b - 1))  # WHY??????????
        carry = temp >> w
    if carry!=0:  C.insert(0,carry) # if the result is bigger than the incomes

    return C


#C = addition(A, B)
#print("A+B=", "".join(map(str, conv_to_hex(C))))

def substraction (A, B):
    if len(A) != len(B):
        equalize(A, B)
#    print("A=", A)
#    print("B=", B)
    n = len(A)
    D = arr.array('i', [])
    if A<B :
        print("WRONG INPUT!!! A<B")
    else:
        borrow = 0
        for i in reversed(range(n)):
            temp = A[i] - B[i] - borrow
            if temp >= 0:
                D.insert(0, temp)
                borrow = 0
            else:
                D.insert(0, b + temp)
                borrow = 1
    return D

#D = substraction(A, B)
#print("A-B=", conv_to_hex(D))



def mulOneDigit(A,d):
    C = arr.array('I', [])
    n = len(A)
    carry = 0
    for i in reversed(range(n)):
        temp = A[i] * d + carry
        C.insert(0, temp & (b - 1))
        carry = temp >> w # скільки значущих біт містить carry?
    C.insert(0, carry)
    return C

def mul(A, B):
    if len(A) != len(B):
        equalize(A, B)
    n = len(A)
    C = arr.array('I', [])
    j=0
    for i in reversed(range(n)):
        temp = mulOneDigit(A, B[i])
        print("i=",i)
        t = j
        while t>0:
            temp.append(0)
            t = t - 1
        print("temp=", temp)
        C = addition (C, temp)
        j = j + 1
    return C

#E = mul(A, B)
#print("AxB=", conv_to_hex(E))




