#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

double countLetters(string text);
double countSentences(string text);
double finalFormula(double avgL, double avgS);

int main(void)
{
    string texts;
    texts = get_string("Text: ");

    double result, answer;
    answer = round(result = finalFormula(countLetters(texts), countSentences(texts))); 
    if (answer < 1)
    {
        printf("Grade: Before Grade 1\n");                                       // the whole line of thought was right but pay attention to some declaration issues
    }                                                                           // to get the most accurate results u must put the numbers as double remember that shi bro
    else if (answer >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", (int) answer);
    }
}

double countLetters(string text) // determine the avg letters every 100 words
{
    int words = 1, letters = 0;
    double avgletters;

    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }

        if (isalpha(text[i]))
        {
            letters++;
        }
    }

    return avgletters = ((double) letters / words) * 100;
}

double countSentences(string text) // determine the avg sentences every 100 words
{
    double sentences = 0, words = 1;
    double avgsentences;

    for (int i = 0; i <= strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }

        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            sentences++;
        }
    }
    return avgsentences = ((double) sentences / words) * 100;
}

double finalFormula(double avgL, double avgS)
{
    double formula;
    return formula = (0.0588 * avgL) - (0.296 * avgS) - 15.8; // final result lesgo
}
