import array as arr

# Initialising system base
print("insert power of 2 for system base:")
w = int(input())
b = 2 ** w
print("b=", b)

# Initialising hex string
print("insert hex string:")
ini_string = input()

# Initial string
print("Initial string", ini_string)

# Converting hex to 2^w
n = int(ini_string, 16)
print("n=", n)
number = arr.array('I', [])
while n > 0:
    number.insert(0, n % b)   #take remainder of division and add it leftmost of the array
    n = n // b

res = number  #result as an array
# Print the result as a string
str_res = "".join(map(str, number))
print("string result:", str_res)

