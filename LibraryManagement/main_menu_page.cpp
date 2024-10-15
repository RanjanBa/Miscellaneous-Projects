#ifndef MAINMENU_H
#define MAINMENU_H

#include<string>

#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "ui_page.cpp"
#include "all_page_names.cpp"

class MainMenuPage : public UIPage {
private:
    int chosen_page_idx;
public:
    MainMenuPage(string _page_name) : UIPage(_page_name) {
        chosen_page_idx = -1;
    }

    string getNextPageName() {
        if(chosen_page_idx == 1) {
            return AllPageNames::loginPageName;
        } else if(chosen_page_idx == 2) {
            return AllPageNames::registrationPageName;
        }

        return "";
    }

    void showPage(LibraryManagement *lb_management) {
        while(true) {
            cout << page_name << endl;
            cout << "\t1. Login Page" << endl;
            cout << "\t2. Registration Page" << endl;
            cout << "\t3. Exit" << endl;

            cout << "Please select Your Option (1-3) : ";
            if(!HandleInputUtility::getNumber(chosen_page_idx)) {
                cout << "Invalid input. Please enter a number between 1 and 3." << endl;
                continue;
            }

            if(chosen_page_idx < 0 || chosen_page_idx > 3) {
                cout << "Please select valid option." << endl;
            } else {
                break;
            }
        }
    }
};

#endif