def substraction_with_decimals(minuend, subtrahend):
    if len(str(minuend).split(".")[1]) > len(str(subtrahend).split(".")[1]):
        largest_decimal = minuend
    else:
        largest_decimal = subtrahend
 
    return round(minuend - subtrahend, len(str(largest_decimal).split(".")[1]))