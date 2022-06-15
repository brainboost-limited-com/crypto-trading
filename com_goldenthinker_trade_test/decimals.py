

def val_to_str(val, precision=14):
    if (precision == None):
        print("!!! precision is None, setting to 14")
        precision = 14
    if(val == None) : return None
    print("val_to_str value:")
    print(val)
    if(precision < 0):
        print("val_to_str output:")
        print(None)
        return None
    string = ""
    if(val < 0): 
        string += "-"
        val *= -1
    whole = float(val) - float(val) % float(1.0)
    print("whole: " + str(whole))
    decimal = val - whole
    print("decimal: " + str(decimal))
    if(whole == 0.0 and decimal == 0.0):
        print("val_to_str output:")
        print("0")
        return "0"
    string += str(int(whole)) +"."
    for i in range (1, precision+1):
        w = int(decimal * 10)
        decimal = decimal * 10.0 - w
        string += str(int(w))

    string = string.rstrip("0").rstrip(".")
    print("val_to_str output:")
    print(string)
    return string

val_to_str(2.464336,8)