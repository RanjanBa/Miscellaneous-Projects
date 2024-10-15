#ifndef LIBRARIAN_H
#define LIBRARIAN_H

#include <string>
#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "ui_page.cpp"
#include "all_page_names.cpp"

class LibrarianPage : public UIPage {
private:
    int chosen_page_idx;
public:
    LibrarianPage(string _page_name) : UIPage(_page_name) {
        chosen_page_idx = -1;
    }

    string getNextPageName() {
        if(chosen_page_idx == 1) {
            return AllPageNames::searchBookPageName;
        } else if(chosen_page_idx == 2) {
            return AllPageNames::addBookPageName;
        } else if(chosen_page_idx == 3) {
            return AllPageNames::mainMenuPageName;
        }
        return "";
    }

    void showPage(LibraryManagement *lb_management) {
        User* user = lb_management->getLoggedUser();
        cout << "Hi, " << user->getFullName() << endl;
        while(true) {
            cout << "\t1. Search Book!" << endl;
            cout << "\t2. Add Book!" << endl;
            cout << "\t3. Logout!" << endl;
            
            cout << "Please select Your Option (1-3) : ";
            if (!HandleInputUtility::getNumber(chosen_page_idx)) {
                cout << "Invalid input. Please enter a number between 1 and 3." << endl;
                continue;
            }

            if(chosen_page_idx <= 0 || chosen_page_idx > 3) {
                cout << "Please select valid option." << endl;
            } else {
                if(chosen_page_idx == 3) {
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