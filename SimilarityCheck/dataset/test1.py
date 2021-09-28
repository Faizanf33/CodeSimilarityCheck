# write fibonacci series up to n

def fibnocci(n):
    x = 0
    y = 1

    fibs = []

    while y < n:
        fibs.append(y)
        x, y = y, x + y

    return fibs


print(fibnocci(5))
