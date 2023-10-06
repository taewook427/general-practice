def make_pattern():
    global pattern
    global length
    global valid_pattern
    valid_pattern = 0
    layer_1(pattern)
    print(valid_pattern)
def layer_1(input_pattern):
    global length
    if length >= 1:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_2(temp)
    else:
        check_pattern(input_pattern)
def layer_2(input_pattern):
    global length
    if length >= 2:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_3(temp)
    else:
        check_pattern(input_pattern)
def layer_3(input_pattern):
    global length
    if length >= 3:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_4(temp)
    else:
        check_pattern(input_pattern)
def layer_4(input_pattern):
    global length
    if length >= 4:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_5(temp)
    else:
        check_pattern(input_pattern)
def layer_5(input_pattern):
    global length
    if length >= 5:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_6(temp)
    else:
        check_pattern(input_pattern)
def layer_6(input_pattern):
    global length
    if length >= 6:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_7(temp)
    else:
        check_pattern(input_pattern)
def layer_7(input_pattern):
    global length
    if length >= 7:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_8(temp)
    else:
        check_pattern(input_pattern)
def layer_8(input_pattern):
    global length
    if length >= 8:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            layer_9(temp)
    else:
        check_pattern(input_pattern)
def layer_9(input_pattern):
    global length
    if length >= 9:
        for x in range(1,10):
            x = str(x)
            temp = input_pattern
            temp = temp + x
            check_pattern(temp)
    else:
        check_pattern(input_pattern)
def check_pattern(input_pattern):
    global valid_pattern
    global valid_check
    valid_check = 0
    if len(input_pattern) > 1:
        check_overlap(input_pattern)
        if valid_check == 0:
            check_latitude(input_pattern)
        if valid_check == 0:
            check_longitude(input_pattern)
        if valid_check == 0:
            check_diagonal(input_pattern)
    if valid_check == 0:
        valid_pattern = valid_pattern + 1
def check_overlap(input_pattern):
    check_1 = 0
    check_2 = 0
    check_3 = 0
    check_4 = 0
    check_5 = 0
    check_6 = 0
    check_7 = 0
    check_8 = 0
    check_9 = 0
    global valid_check
    long = len(input_pattern)
    for i in range(0,long):
        if input_pattern[i] == '1':
            if check_1 == 0:
                check_1 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '2':
            if check_2 == 0:
                check_2 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '3':
            if check_3 == 0:
                check_3 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '4':
            if check_4 == 0:
                check_4 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '5':
            if check_5 == 0:
                check_5 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '6':
            if check_6 == 0:
                check_6 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '7':
            if check_7 == 0:
                check_7 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '8':
            if check_8 == 0:
                check_8 = 1
            else:
                valid_check = 1
        elif input_pattern[i] == '9':
            if check_9 == 0:
                check_9 = 1
            else:
                valid_check = 1
def check_latitude(input_pattern):
    long = len(input_pattern)
    global valid_check
    check_2 = 0
    check_5 = 0
    check_8 = 0
    for i in range(0,long-1):
        if input_pattern[i] == '2':
            check_2 = 1
        elif input_pattern[i] == '5':
            check_5 = 1
        elif input_pattern[i] == '8':
            check_8 = 1
        elif input_pattern[i] == '1' and input_pattern[i+1] == '3' and check_2 == 0:
            valid_check = 1
        elif input_pattern[i] == '3' and input_pattern[i+1] == '1' and check_2 == 0:
            valid_check = 1
        elif input_pattern[i] == '4' and input_pattern[i+1] == '6' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '6' and input_pattern[i+1] == '4' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '7' and input_pattern[i+1] == '9' and check_8 == 0:
            valid_check = 1
        elif input_pattern[i] == '9' and input_pattern[i+1] == '7' and check_8 == 0:
            valid_check = 1
def check_longitude(input_pattern):
    long = len(input_pattern)
    global valid_check
    check_4 = 0
    check_5 = 0
    check_6 = 0
    for i in range(0,long-1):
        if input_pattern[i] == '4':
            check_4 = 1
        elif input_pattern[i] == '5':
            check_5 = 1
        elif input_pattern[i] == '6':
            check_6 = 1
        elif input_pattern[i] == '1' and input_pattern[i+1] == '7' and check_4 == 0:
            valid_check = 1
        elif input_pattern[i] == '7' and input_pattern[i+1] == '1' and check_4 == 0:
            valid_check = 1
        elif input_pattern[i] == '2' and input_pattern[i+1] == '8' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '8' and input_pattern[i+1] == '2' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '3' and input_pattern[i+1] == '9' and check_6 == 0:
            valid_check = 1
        elif input_pattern[i] == '9' and input_pattern[i+1] == '3' and check_6 == 0:
            valid_check = 1
def check_diagonal(input_pattern):
    long = len(input_pattern)
    global valid_check
    check_5 = 0
    for i in range(0,long-1):
        if input_pattern[i] == '5':
            check_5 = 1
        elif input_pattern[i] == '1' and input_pattern[i+1] == '9' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '9' and input_pattern[i+1] == '1' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '3' and input_pattern[i+1] == '7' and check_5 == 0:
            valid_check = 1
        elif input_pattern[i] == '7' and input_pattern[i+1] == '3' and check_5 == 0:
            valid_check = 1
def work():
    global valid_pattern
    global pattern
    global length
    valid_pattern = 0
    pattern = ''
    x = input('length?(1~9)\n')
    x = int(x)
    length = x
    make_pattern()
work()
