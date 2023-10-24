def a008336(n):
    a008336_list = [1]
    for i in range(1, n):
        a008336_list.append(a008336_list[i-1] // i if a008336_list[i-1] % i == 0 else a008336_list[i-1] * i)
    return a008336_list[n-1]

test = []

for i in range (25):
    test.append(a008336(i))

print(test)