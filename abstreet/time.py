def conv_time(i):
    return str(int(i)) + ':' + str(int((i % 1) * 60))

print(conv_time(17.05))