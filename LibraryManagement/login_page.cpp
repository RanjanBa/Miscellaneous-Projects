#ifndef LOGIN_H
#define LOGIN_H

#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "all_page_names.cpp"
#include "user.cpp"
#include "ui_page.cpp"


class LogInPage : public UIPage {
private:
    UserType logged_user_type;
    bool is_failed;
public:
    LogInPage(string _page_name) : UIPage(_page_name) {
        is_failed = false;
    }

    string getNextPageName() {
        if(is_failed) return AllPageNames::mainMenuPageName;

        if(logged_user_type == UserType::LIBRARIAN_TYPE) {
            return AllPageNames::librarianPageName;
        } else if(logged_user_type == UserType::MEMBER_TYPE) {
            return AllPageNames::memberPageName;
        }

        throw runtime_error("Different user type is not allowed!");
    }

    void showPage(LibraryManagement *lb_management) {
        is_failed = false;
        string user_name, password;
        while (true) {
            cout << "Enter user name : ";
            if(!HandleInputUtility::getStringWithoutSpace(user_name)) {
                cout << "Invalid input. Please enter valid user name." << endl;
            } else {
                break;
            }
        }

        while (true) {
            cout << "Enter password : ";
            if(!HandleInputUtility::getStringWithoutSpace(password)) {
                cout << "Invalid input. Please enter valid password." << endl;
            } else {
                break;
            }
        }

        if(lb_management->login(user_name, password)) {
            logged_user_type = lb_management->getLoggedUser()->getUserType();
        } else {
            cout << "Username and Password doesn't match. Please try again..." << endl;
            is_failed = true;
        }
    }
};

#endif