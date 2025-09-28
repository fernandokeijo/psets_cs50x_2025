#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int calc = 0, calc2 = 0, calc3, credit3, credit4, sum = 0, op, op2, result, card2, card3;
    long card,credit2 ,credit = get_long("Number: "), count = 0, card4;

    card = credit;
    card4 = credit;

    do {
    credit2 = credit / 10;                      // count by the second to last number until the begining of the credit card number
    credit3 = credit % 10;


    credit = credit2 / 10;

    calc = ( credit2 % 10 ) * 2;

    if (calc < 10)
    calc2 += calc;                             // split the numbers that will be added first from the ones that i'll add after
    else
    {
    calc3 = calc / 10;
    calc2 += calc % 10;
    calc2 += calc3;
    }

    if (credit3 < 10)
    sum += credit3;
    else{
    op = credit3 / 10;                        // sum both groups of digits
    sum += op;
    sum += credit3 % 10;}

    } while (credit != 0);


    result = calc2 + sum;                       // put them together

    do{
        card = card / 10;    //extract the first 2 numbers of the creditcard id

    } while (card > 100);

    do{
        card4 = card4 / 10;    //AAAAAAAAAAAAAAAAAAA
        count++;
    } while (card4 > 0);


    card3 = card / 10;      //extract the first number of the creditcard id

    if(result > 10)
        result = result % 10;


    if (result != 0)
        printf("INVALID\n");
    else if (card3 == 4)
    {                                                   //determine which card is
        if (count == 13 || count == 16)
        printf("VISA\n");
        else
        printf("INVALID\n");
    }

    else if (card == 34 || card == 37)
    {
        if (count == 15)
        printf("AMEX\n");
        else
        printf("INVALID\n");
    }
    else if (card >= 51 && card <= 55 && count == 16)
        printf("MASTERCARD\n");
    else
        printf("INVALID\n");
}
