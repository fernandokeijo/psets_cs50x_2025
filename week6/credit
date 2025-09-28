from cs50 import get_string

def main():

    checksum()


def checksum():

    number = get_string("Number: ")
    count = len(number)
    twotimes = 0
    onetime = 0

    for i in range(count - 2, -1, -2):
        digit = int(number[i]) * 2
        if digit < 10:
            twotimes += digit
        else:
            twotimes += (digit // 10) + (digit % 10)

    count = len(number)

    while count >= 1:
        count = count - 1
        onetime = onetime + int(number[count])
        count = count - 1

    sum1 = onetime + twotimes
    count = len(number)

    if (sum1 % 10 != 0):
        print("INVALID")
        return

    if number.startswith("4") and count in [13, 16]:
        print("VISA")
    elif number[:2] in ["34", "37"] and count == 15:
        print("AMEX")
    elif number[0] == "5" and number[1] in "12345" and count == 16:
        print("MASTERCARD")
    else:
        print("INVALID")


main()
