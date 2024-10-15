#ifndef HANDLE_INPUT_H
#define HANDLE_INPUT_H

#include <iostream>
#include <sstream>
#include <string>
#include <limits>

using namespace std;

class HandleInputUtility {
public:
    static bool getNumber(int &res) {
        string input;
        getline(cin, input);

        if(input.empty()) {
            return false;
        }

        stringstream ss(input);

        if(ss >> res) {
            return true;
        }

        return false;
    }
    
    static bool getChar(char &res) {
        string input;
        getline(cin, input);

        if(input.empty()) {
            return false;
        }

        stringstream ss(input);

        if(ss >> res) {
            return true;
        }

        return false;
    }

    static bool getStringWithoutSpace(string &res) {
        string input;
        getline(cin, input);

        if (cin.fail()) {
            cin.clear();
            return false;
        }

        int pos = input.find(' ');

        if(pos != string::npos) {
            res = input.substr(0, pos);
        } else {
            res = input;
        }

        if(res.empty()) return false;

        return true;
    }

    static bool getStringWithSpace(string &res) {
        getline(cin, res);

        if (cin.fail()) {
            cin.clear();
            return false;
        }

        if(res.empty()) return false;
        
        return true;
    }
};

#endif