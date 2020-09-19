import array as arr

# Initialising system base
print("insert power of 2 for system base:")
w = int(input())
b = 2 ** w
print("b=", b)

# Initialising hex string
print("insert hex string 1:")
ini_string1 = input()
print("Initial string 1", ini_string1)

print("insert hex string 2:")
ini_string2 = input()
print("Initial string 2", ini_string2)


# Converting hex to 2^w
def convhex(hex, b):
    n = int(hex, 16)
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % b)  # take remainder of division and add it leftmost of the array
        n = n // b
    return number


A = convhex(ini_string1, b)
B = convhex(ini_string2, b)
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

#Test values
#81A13
#2C9 1F6B19
def addition(A, B, b):
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


#C = addition(A, B, b)
#print("A+B=", "".join(map(str, C)))

def substraction (A, B, b):
    if len(A) != len(B):
        equalize(A, B)
    print("A=", A)
    print("B=", B)
    n = len(A)
    D = arr.array('i', [])
    A1 = arr.array('i', [])
    B1 = arr.array('i', [])
    if A>B:
        s = 1
        A1 = A
        B1 = B
    else:
        s = -1 #sign
        A1 = B
        B1 = A
    borrow = 0
    for i in reversed(range(n)):
        temp = A1[i] - B1[i] - borrow
        if temp >= 0:
            D.insert(0, temp)
            borrow = 0
        else:
            D.insert(0, b + temp)
            borrow = 1
    D[0] = D[0] * s
    return D

D = substraction(A, B, b)
print("A-B=", "".join(map(str, D)))

#Test values
#81A13
#2C9 1F6B19