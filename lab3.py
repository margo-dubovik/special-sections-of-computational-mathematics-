# GF(2^m). m=251.
# generator: f = x^251 + x^14 + x^4 + x + 1.

import array as arr


def bin_str_to_arr(num):
    number = arr.array('I', [])
    for i in range(len(num)):
        number.append(int(num[i], 2))
    return number


def hex_str_to_arr(num):
    number = arr.array('I', [])
    for i in range(len(num)):
        k = bin(int(num[i], 16))
        conv = [int(x) for x in k[2:]]
        number.extend(conv)
    return number


def insert_numbers():
    print("Bin(1) ot Hex(2)?")
    ans = input()
    if ans == '1':
        print("Insert bin A:")
        x = bin_str_to_arr(input())
        print("Insert bin B:")
        y = bin_str_to_arr(input())
    elif ans == '2':
        print("Insert hex A:")
        x = hex_str_to_arr(input())
        print("Insert hex B:")
        y = hex_str_to_arr(input())
    else:
        print("WRONG INPUT. TRY AGAIN")
        insert_numbers()
    return x, y


inserted_values = insert_numbers()
a = inserted_values[0]
b = inserted_values[1]

print("A=", a)
print("B=", b)


def equalize(A, B):   # Equalize two numbers` length
    if len(A) > len(B):
        while len(A) != len(B):
            B.insert(0, 0)  # add zeros to the beginning to equal the length
    else:
        while len(A) != len(B):
            A.insert(0, 0)


def addition_pol(A, B):
    if len(A) != len(B):
        equalize(A, B)
    n = len(A)
    C = arr.array('I', [])
    for i in reversed(range(n)):
        temp = A[i] + B[i]
        C.insert(0, temp & (1))
    return C


addition = addition_pol(a, b)
print(addition)