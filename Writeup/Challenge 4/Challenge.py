import serial

def A008336(n):
    a008336_list = [1]
    for i in range(1, n):
        a008336_list.append(a008336_list[i-1] // i if a008336_list[i-1] % i == 0 else a008336_list[i-1] * i)
    return a008336_list[n-1]

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

while True:
    while True:
        result = ser.readline()
        if(len(result) > 0):
            print(result.decode())

        if("over serial" in result.decode()):
            break

    ser.write(str(A008336(25)).encode("ascii"))
    ser.flush()