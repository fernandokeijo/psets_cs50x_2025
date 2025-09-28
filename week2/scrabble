#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    int teste;
    string player1, player2;

    char alphabet[] = {'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                       'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'}; // alphabets
    char alphabet2[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'};
    int points[] = {1, 3, 3, 2,  1, 4, 2, 4, 1, 8, 5, 1, 3,
                    1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10}; // point counters

    int score1 = 0, score2 = 0;

    player1 = get_string("Player1: "); // get those words

    player2 = get_string("Player2: ");

    for (int j = 0; j < strlen(player1); j++)
    {

        for (int i = 0; i < 26; i++) // calculate the scores
        {
            if (player1[j] == alphabet[i] || player1[j] == alphabet2[i])
            {
                score1 += points[i];
                break;
            }
        }
    }

    for (int j = 0; j < strlen(player2); j++)
    {

        for (int i = 0; i < 26; i++)
        {
            if (player2[j] == alphabet[i] || player2[j] == alphabet2[i])
            {
                score2 += points[i];
                break;
            }
        }
    }

    if (score1 > score2)
    {
        printf("Player 1 wins!\n"); // results
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
