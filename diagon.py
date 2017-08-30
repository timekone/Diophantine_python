input_arr = [
       [0, 2, 4, 0, -9],
    [0, 2, -3, -2, -1],
       [2, -1, -4, 1, 5],]

print(range(len(input_arr[0])))

for i in range(len(input_arr)):
    if input_arr[i][i] == 0:
        t = 1
        while input_arr[i+t][i] == 0 and i+t < len(input_arr):
            t += 1
        c = input_arr[i]
        input_arr[i] = input_arr[i + t]
        input_arr[i + t] = c
        if input_arr[i][i] == 0:
            break
    for j in range(0, i):
        if input_arr[j][i] != 0:
            input_arr[j] = list(map(lambda x, y: x * input_arr[i][i] - y * input_arr[j][i], input_arr[j], input_arr[i]))
    for j in range(i+1, len(input_arr)):
        if input_arr[j][i] != 0:
            input_arr[j] = list(map(lambda x, y: x * input_arr[i][i] - y * input_arr[j][i], input_arr[j], input_arr[i]))

#arr[1] = list(map(lambda x, y: x*arr[0][0]-y*arr[1][0], arr[1], arr[0]))
for v in input_arr:
    print(v)
