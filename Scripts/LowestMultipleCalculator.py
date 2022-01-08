"""
Prints a list of numbers (except 1) that the given number is a multiple of.
"""

import sys
if __name__ == "__main__":
    num = int(sys.argv[1]) * -1
    for x in range(2, num):
        if num % x == 0:
            print(x)

