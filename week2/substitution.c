#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

string convertion (string script1, string plaintext1);

int main (int arg,string script[])
{
    if (arg != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    if (strlen(script[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    // Verifica se todos os caracteres são letras
    for (int i = 0; i < 26; i++)
    {
        if (!isalpha(script[1][i]))
        {
            printf("Key must only contain alphabetic characters.\n");
            return 1;
        }
    }

    // Verifica se há caracteres repetidos (ignora maiúscula/minúscula)
    for (int i = 0; i < 26; i++)
    {
        for (int j = i + 1; j < 26; j++)
        {
            if (tolower(script[1][i]) == tolower(script[1][j]))
            {
                printf("Key must not contain repeated characters.\n");
                return 1;
            }
        }
    }

    string plaintext = get_string("plaintext: ");
    string script2 = script[1];

    printf("ciphertext: %s\n",convertion(script2, plaintext));
}

string convertion (string script1, string plaintext1)
{
    char alphabet[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", alphabet2[] = "abcdefghijklmnopqrstuvwxyz";

    for (int aux = 0; aux < strlen(plaintext1); aux++)
    {
        for (int i = 0; i < 26; i++)
        {
            if (plaintext1[aux] == alphabet[i])   //upper
            {
                plaintext1[aux] = script1[i];
                plaintext1[aux] = toupper(plaintext1[aux]);
                break;
            }
            if  (plaintext1[aux] == alphabet2[i])  //lower
            {
                plaintext1[aux] = script1[i];
                plaintext1[aux] = tolower(plaintext1[aux]);
                break;
            }
        }
    }

    return plaintext1;
}
