#include <bits/stdc++.h>

using namespace std;

void showBoard(char *a)
{
    for (int j = 0; j < 3; j++)
    {
        cout << " __ ";
    }

    cout << "\n";

    for (int i = 0; i < 3; i++)
    {
        cout << "\n";
        for (int j = 0; j < 3; j++)
        {
            cout << "| " << a[i * 3 + j] << " ";
        }

        cout << "|\n";

        for (int j = 0; j < 3; j++)
        {
            cout << " __ ";
        }

        cout << "\n";
    }
}

bool isLegalMove(char *a, int pos)
{
    if (pos < 0 || pos >= 9)
    {
        return false;
    }

    if (a[pos] == 'O' || a[pos] == 'X')
    {
        return false;
    }

    return true;
}

bool checkWin(char *a)
{
    for (int i = 0; i < 3; i++)
    {
        if (a[i * 3 + 0] == a[i * 3 + 1] && a[i * 3 + 1] == a[i * 3 + 2])
        {
            return true;
        }

        if (a[i] == a[3 + i] && a[3 + i] == a[6 + i])
        {
            return true;
        }
    }

    if (a[0] == a[4] && a[4] == a[8])
    {
        return true;
    }

    if (a[2] == a[4] && a[4] == a[6])
    {
        return true;
    }

    return false;
}

int main()
{
    char a[9];

    for (int i = 0; i < 9; i++)
    {
        a[i] = '1' + i;
    }

    showBoard(a);

    bool flag = 0;
    bool isPlaying = true;
    while (isPlaying)
    {
        cout << "\n";

        if (flag == 0)
        {
            cout << "It is player 1 turn...\n";
        }
        else
        {
            cout << "It is player 2 turn...\n";
        }

        int pos = -1;
        cout << "Possition between 1 to 9 : ";
        cin >> pos;

        pos--;

        if (!isLegalMove(a, pos))
        {
            cout << "Move is illegal. Try another position...\n";
            continue;
        }

        a[pos] = flag == 0 ? 'O' : 'X';

        showBoard(a);

        if (checkWin(a))
        {
            cout << "Player " << (flag == 0 ? "1" : "2") << " won!\n";
            break;
        }

        flag = !flag;
    }
}