from __future__ import print_function


def string_height_to_inches(height_str):
    """
    Given the NBA API style returned height return same height in integer inches.
    Example:
    string_height_to_inches("6-7")  ->  79
    """
    if len(height_str.split("-")) == 2:
        feet, inches = height_str.split("-")
        return 12 * int(feet) + int(inches)
    else:
        f = open('tools.log','w')
        print("string_height_to_inches error:" + height_str, file=f)
        return ""
    
