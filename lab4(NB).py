import array as arr
import long_modular as lm
import long_basic as lb
import polynomial_bas as pb
import time

m = 251


def check_existance(num):
    p = 2 * num + 1
    k = num * 2
    if p > 1:
        for i in range(2, p // 2):
            if (p % i) == 0:
                print(p, "=p is not a prime number")
        if (p % 4) == 3 and (2 ** k) % p == 1:
            print(f"ONB for GF(2^{num}) EXISTS")
        else:
            print(f"ONB for GF(2^{num}) DOESN`T EXIST")
    else:
        print(num, "=p is not a prime number")


def generate_constant_0_1(c):
    if c != 0 and c != 1:
        return 0
    c_arr = arr.array('I', [])
    for i in range(m):
        c_arr.append(c)
    return c_arr


def bin_str_to_arr(num):
    number = arr.array('I', [])
    for i in range (len(num)):
        number.append(int(num[i],2))
    return number

def hex_str_to_arr(num):
    n = int(num, 16)
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % 2)  # take remainder of division and add it leftmost of the array
        n = n // 2
    return number

def bin_str_to_hex_str(num):
    number = hex(int(num, 2))[2:]
    if number[0] == '0':
        number = number[1:]
    if len(number) < 64:
        while len(number) != 64:
            number = '0' + number
    return number


def insert_numbers():
    print("Bin(1) ot Hex(2)?")
    ans = input()
    if ans == '1':
        print("Insert bin A:")
        A = bin_str_to_arr(input())
        print("Insert bin B:")
        B = bin_str_to_arr(input())
        print("Insert bin N:")
        N = bin_str_to_arr(input())
    elif ans == '2':
        print("Insert hex A:")
        A = hex_str_to_arr(input())
        print("Insert hex B:")
        B = hex_str_to_arr(input())
        print("Insert hex N:")
        N = hex_str_to_arr(input())
    else:
        print("WRONG INPUT. TRY AGAIN")
        insert_numbers()
    return A, B, N

def addition_nb(x, y):
    if len(x) != len(y):
        lb.equalize(x, y)
    n = len(x)
    z = arr.array('I', [])
    for i in reversed(range(n)):
        temp = x[i] + y[i]
        z.insert(0, temp & 1)
    if len(z) <251:
        while len(z) != 251:
            z.insert(0, 0)
    return z

def square_nb(x):
    y = x[:]
    z = y[-1:len(y):] + y[0:-1:]
    return z

check_existance(m)
zero = generate_constant_0_1(0)
one = generate_constant_0_1(1)

inserted_values = insert_numbers()
a = inserted_values[0]
b = inserted_values[1]
n = inserted_values[2]

addition = addition_nb(a, b)
square = square_nb(a)

addition_str = ''.join(map(str, addition))
square_str = ''.join(map(str, square))

# print("A+B=", addition_str)
# print("A^2=", square_str)

print("A+B hex=", bin_str_to_hex_str(addition_str))
print("A^2 hex=", bin_str_to_hex_str(square_str))