# write a power function

def power(base, exponent):
    result = 1
    for i in range(exponent):
        result = result * base
    return result


print(power(2, 4))
print(power(5, 2))
print(power(4, 3))
