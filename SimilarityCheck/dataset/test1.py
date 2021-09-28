# write a power function

def power(x, e):
    res = 1

    for i in range(e):
        res = res * x

    return res


print(power(2, 4))
print(power(5, 2))
