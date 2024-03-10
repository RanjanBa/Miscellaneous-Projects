#include <stdio.h>

void showBoard(char *a)
{
    for (int j = 0; j < 3; j++)
    {
        printf(" ___");
    }

    printf("\n");

    for (int i = 0; i < 3; i++)
    {
        printf("\n");
        for (int j = 0; j < 3; j++)
        {
            printf("| %c ", a[i * 3 + j]);
        }

        printf("|\n");

        for (int j = 0; j < 3; j++)
        {
            printf(" ___");
        }

        printf("\n");
    }
}

int isLegalMove(char *a, int pos)
{
    if (pos < 0 || pos >= 9)
    {
        return 0;
    }

    if (a[pos] == 'O' || a[pos] == 'X')
    {
        return 0;
    }

    return 1;
}

int checkWin(char *a)
{
    for (int i = 0; i < 3; i++)
    {
        if (a[i * 3 + 0] == a[i * 3 + 1] && a[i * 3 + 1] == a[i * 3 + 2])
        {
            return 1;
        }

        if (a[i] == a[3 + i] && a[3 + i] == a[6 + i])
        {
            return 1;
        }
    }

    if (a[0] == a[4] && a[4] == a[8])
    {
        return 1;
    }

    if (a[2] == a[4] && a[4] == a[6])
    {
        return 1;
    }

    return 0;
}

int main()
{
    char a[9];

    for (int i = 0; i < 9; i++)
    {
        a[i] = '1' + i;
    }

    showBoard(a);

    int flag = 0;
    int isPlaying = 1;
    while (isPlaying)
    {
        printf("\n");

        if (flag == 0)
        {
            printf("It is player 1 turn...\n");
        }
        else
        {
            printf("It is player 2 turn...\n");
        }

        int pos = -1;
        printf("Possition between 1 to 9 : ");
        scanf("%d", &pos);

        pos--;

        while (getchar() != '\n')
            ;

        printf("Pos: ", pos);

        if (!isLegalMove(a, pos))
        {
            printf("Move is illegal. Try another position...\n");
            continue;
        }

        a[pos] = flag == 0 ? 'O' : 'X';

        showBoard(a);

        if (checkWin(a))
        {
            printf("Player %c won!\n", (flag == 0 ? '1' : '2'));
            break;
        }

        flag = (flag == 1 ? 0 : 1);
    }

    return 0;
}