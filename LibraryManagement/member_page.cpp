#ifndef MEMBER_H
#define MEMBER_H

#include <string>
#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "all_page_names.cpp"
#include "ui_page.cpp"

class MemberPage : public UIPage {
private:
    int chosen_page_idx;
public:
    MemberPage(string _page_name) : UIPage(_page_name) {
        chosen_page_idx = -1;
    }

    string getNextPageName() {
        if(chosen_page_idx == 1) {
            return AllPageNames::searchBookPageName;
        } else if(chosen_page_idx == 2) {
            return AllPageNames::borrowBookPageName;
        } else if(chosen_page_idx == 3) {
            return AllPageNames::returnBookPageName;
        } else if(chosen_page_idx == 4) {
            return AllPageNames::mainMenuPageName;
        } else {
            cout << "Please select valid option." << endl;
        }
        return "";
    }

    void showPage(LibraryManagement *lb_management) {
        User *user = lb_management->getLoggedUser();
        cout << "Hi, " << user->getFullName() << endl;
        while(true) {
            cout << "\t1. Search Book!" << endl;
            cout << "\t2. Borrow Book!" << endl;
            cout << "\t3. Return Book!" << endl;
            cout << "\t4. Logout!" << endl;

            cout << "Please select Your Option (1-4) : ";

            if(!HandleInputUtility::getNumber(chosen_page_idx)) {
                cout << "Invalid input. Please enter a number between 1 and 4." << endl;
                continue;
            }

            if(chosen_page_idx <= 0 || chosen_page_idx > 4) {
                cout << "Please select valid option." << endl;
            } else {
                if(chosen_page_idx == 4) {
                    if(lb_management->logout()) {
                        cout << "You are logged out of system." << endl;
                        break;
                    } else {
                        cout << "You can't logged out of system." << endl;
                    }
                } else {
                    break;
                }
            }
        }
    }
};

#endif