import array as arr
import long_modular as lm
import long_basic as lb
import polynomial_bas as pb
import time
import numpy as np

m = 251


def check_existence(num):
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
    for i in range(len(num)):
        number.append(int(num[i], 2))
    if len(number) < 251:
        number.insert(0, 0)
    return number


def hex_str_to_arr(num):
    n = int(num, 16)
    number = arr.array('I', [])
    while n > 0:
        number.insert(0, n % 2)  # take remainder of division and add it leftmost of the array
        n = n // 2
    if len(number) < 251:
        number.insert(0, 0)
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
        A = 0
        B = 0
        N = 0
        insert_numbers()
    return A, B, N, ans


def addition_nb(x, y):
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


def square_nb(x):
    y = x[:]
    z = y[-1:len(y):] + y[0:-1:]
    return z


def trace_nb(x):
    tr = 0
    for i in range(len(x)):
        tr = (tr + x[i]) % 2
    return tr


def mult_matrix(m):
    p = 2 * m + 1
    matr = [[0] * m for i in range(m)]
    for i in range(m):
        for j in range(m):
            k = 2 ** i
            t = 2 ** j
            q1 = k % p + t % p
            q2 = k % p - t % p
            if q1 > 0 and (q1 % p == 1 or p - q1 % p == 1):
                matr[i][j] = 1
            elif q2 > 0 and (q2 % p == 1 or p - q2 % p == 1):
                matr[i][j] = 1
            elif q2 < 0 and (p + q2 == 1 or p + q2 == -1 or q2 == -1):
                matr[i][j] = 1
            else:
                matr[i][j] = 0
    return matr


def mul_matrices(p, q):
    data_p = np.asarray(p)
    if len(data_p.shape) == 1:
        p = [[i for i in p]]
    data_q = np.asarray(q)
    if len(data_q.shape) == 1:
        q = [[i for i in q]]
        q = np.transpose(q)
    res = arr.array('I', [])
    t = 0
    for i in range(len(p)):
        for j in range(len(q[0])):
            for k in range(len(q)):
                h1 = p[i][k]
                h2 = q[k][j]
                t = (t + h1 * h2) % 2
            res.append(t)
            t = 0
    return res


def shift_r(x, n):
    y = x[:]
    z = y[-n:len(y):] + y[0:-n:]
    return z


def shift_l(x, n):
    y = x[:]
    z = y[n:len(y):] + y[0:n:]
    return z


def mul_nb(x, y):
    res = arr.array('I', [])
    for i in range(len(x)):
        mult_1 = (mul_matrices(shift_l(x, i), lambda_matr))
        mult_2 = (mul_matrices(mult_1, shift_l(y, i)))
        res.append(mult_2[0])
    return res


def degree_of_long_nb(x, n):
    l = len(n)
    z = one
    for i in reversed(range(l)):
        if n[i] == 1:
            print("a")
            z = mul_nb(x, z)
            print("b")
        x = square_nb(x)
    return z

def inv_by_mul(x):
    d = x[:]
    k = 1
    h = bin(m-1)[2:]
    t = len(h)
    for i in (range(1, t)):
        d_k = d[:]
        for j in range(k):
            d_k = square_nb(d_k)
        d = mul_nb(d_k, d)
        k = k * 2
        if h[i] == '1':
            d1 = square_nb(d)
            d = mul_nb(d1, a)
            k = k + 1
    res = square_nb(d)
    return res


check_existence(m)
zero = generate_constant_0_1(0)
one = generate_constant_0_1(1)

lambda_matr = mult_matrix(m)
# for row in lambda_matr:
#     print(row)


inserted_values = insert_numbers()
a = inserted_values[0]
b = inserted_values[1]
n = inserted_values[2]
sys = inserted_values[3]

start = time.time()
addition = addition_nb(a, b)
end = time.time()
print("A+B time (sec):", end - start)

start = time.time()
multiplication = mul_nb(a, b)
end = time.time()
print("A*B time (sec):", end - start)

start = time.time()
square = square_nb(a)
end = time.time()
print("A^2 time (sec):", end - start)

start = time.time()
trace = trace_nb(a)
end = time.time()
print("Tr(A) time (sec):", end - start)

start = time.time()
inv = inv_by_mul(a)
end = time.time()
print("A^(-1) time (sec):", end - start)

start = time.time()
degree = degree_of_long_nb(a, n)
end = time.time()
print("A^N time (sec):", end - start)


addition_str = ''.join(map(str, addition))
square_str = ''.join(map(str, square))
multiplication_str = ''.join(map(str, multiplication))
degr_str = ''.join(map(str, degree))
inv_str = ''.join(map(str, inv))

if sys == '1':
    print("A+B=", addition_str)
    print("A*B=", multiplication_str)
    print("A^2=", square_str)
    print("Tr(A)=", trace)
    print("A^(-1)=", inv_str)
    print("A^N=", degr_str)

else:
    print("A+B hex=", bin_str_to_hex_str(addition_str))
    print("A*B hex =", bin_str_to_hex_str(multiplication_str))
    print("A^2 hex=", bin_str_to_hex_str(square_str))
    print("Tr(A)=", trace)
    print("A^(-1) hex =", bin_str_to_hex_str(inv_str))
    print("A^N hex =", bin_str_to_hex_str(degr_str))


def test_func():
    test1 = lb.comparison(mul_nb(addition, n), addition_nb(mul_nb(a, n), mul_nb(b, n)))
    print("(A+B)*N=?=A*N+B*N:", test1)
    n_m = arr.array('I', [1 for i in range(m)])  # n_m = 2^m - 1
    n1 = arr.array('I', [0, 1])
    while len(n1) != 251:
        n1.insert(0, 0)
    start = time.time()
    test2 = degree_of_long_nb(n1, n_m)
    end = time.time()
    print("c^(2^m - 1)  time (sec):", end - start)
    test3 = lb.comparison(test2, one)
    print("c^(2^m - 1) =?= 1 :", test3)



test_func()

#N= 32ABCD (len=6)