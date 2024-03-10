#include <iostream>
using namespace std;
char board[3][3];

void showbrd()
{
    cout << endl
         << endl;
    cout << "    " << board[0][0] << "  "
         << "|"
         << "  " << board[0][1] << " "
         << "|"
         << "  " << board[0][2] << endl;
    cout << "   ____"
         << "|"
         << "____"
         << "|"
         << "____" << endl;
    cout << "    " << board[1][0] << "  "
         << "|"
         << "  " << board[1][1] << " "
         << "|"
         << "  " << board[1][2] << endl;
    cout << "   ____"
         << "|"
         << "____"
         << "|"
         << "____" << endl;
    cout << "    " << board[2][0] << "  "
         << "|"
         << "  " << board[2][1] << " "
         << "|"
         << "  " << board[2][2] << endl;
    cout << "       "
         << "|"
         << "    "
         << "|"
         << "    " << endl;
}

bool checkbrd(int i, int j)
{
    if (board[i][j] == 'O' || board[i][j] == 'X')
    {
        return false;
    }

    return true;
}

bool checkWin()
{
    for (int i = 0; i < 3; i++)
    {
        if (board[i][0] == board[i][1] && board[i][1] == board[i][2])
        {
            return true;
        }
    }

    for (int i = 0; i < 3; i++)
    {
        if (board[0][i] == board[1][i] && board[1][i] == board[2][i])
        {
            return true;
        }
    }

    if (board[0][0] == board[1][1] && board[1][1] == board[2][2])
    {
        return true;
    }

    if (board[0][2] == board[1][1] && board[1][1] == board[2][0])
    {
        return true;
    }

    return false;
}

int main()
{
    char O, X;

    for (int k = 0; k < 3; k++)
    {
        for (int j = 0; j < 3; j++)
        {
            board[k][j] = '1' + (k * 3 + j);
        }
    }

    showbrd();

    bool flag = true;

    for (int i = 0; i < 9; i++)
    {
        char ch;
        if (flag == true)
        {
            ch = 'O';
            cout << "Player 1's turn...\n";
        }
        else
        {
            ch = 'X';
            cout << "Player 2's turn...\n";
        }

        cout << "where do you want to put : ";
        int a;
        cin >> a;

        a--;

        int r = a / 3;
        int c = a % 3;

        if (checkbrd(r, c) == false)
        {
            cout << "Your position is not valid.\n";
            continue;
        }

        board[r][c] = ch;

        showbrd();

        if (checkWin())
        {
            if (flag)
            {
                cout << "Player 1 win!\n";
            }
            else
            {
                cout << "Player 2 win!\n";
            }

            break;
        }

        flag = !flag;
    }
}
