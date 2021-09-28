# write a power function

def calculate_power(base, exponent):
    result = 1
    for i in range(exponent):
        result = result * base
    return result


print(calculate_power(2, 4))
print(calculate_power(5, 2))
