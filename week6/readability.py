from cs50 import get_string

def main():

    text = get_string("Text: ")
    letters = 0
    words = 1
    sentences = 0

    for i in text:

        if i.isalpha():
            letters += 1

        elif i == " ":
            words += 1

        elif i in [".", "!", "?"]:
            sentences += 1

    letters = (letters / words) * 100
    sentences = (sentences / words) * 100

    formula = round((0.0588 * letters - 0.296 * sentences - 15.8))

    if formula < 1:
        print("Before Grade 1")
        return
    elif formula >= 16:
        print("Grade 16+")
        return
    else:
        print(f"Grade {formula}")


main()
