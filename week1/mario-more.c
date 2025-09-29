#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int count = 0;
    int k;
    int m;

    do
    {
        int i = get_int("say the number\n");
        k = i;
        m = i;
    }
    while (k < 1 || k > 8);

    for (int j = 0; j < k; j++)
    {
        count++;
        m--;
        for (int o = 0; o < m; o++)
        {
            printf(" ");
        }

        if (count == 1)
            printf("#  #\n");

        if (count == 2)
            printf("##  ##\n");

        if (count == 3)
            printf("###  ###\n");

        if (count == 4)
            printf("####  ####\n");

        if (count == 5)
            printf("#####  #####\n");

        if (count == 6)
            printf("######  ######\n");

        if (count == 7)
            printf("#######  #######\n");

        if (count == 8)
            printf("########  ########\n");
    }
}
