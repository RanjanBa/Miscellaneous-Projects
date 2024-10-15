#ifndef REGISTER_H
#define REGISTER_H

#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "all_page_names.cpp"
#include "ui_page.cpp"
#include "user.cpp"

// string user_name;
// string password;
// string title;
// string address;
// string email_address;
// UserType user_type;

class RegistrationPage : public UIPage {
private:
    UserType logged_user_type;
    bool is_failed;
public:
    RegistrationPage(string _page_name) : UIPage(_page_name) {
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
        string user_name, password, full_name, address, email_address;
        is_failed = false;
        while (true) {
            cout << "Enter user_name : ";
            if(!HandleInputUtility::getStringWithoutSpace(user_name)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }

        while (true) {
            cout << "Enter password : ";
            if(!HandleInputUtility::getStringWithoutSpace(password)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }

        while (true) {
            cout << "Enter Full Name : ";
            if(!HandleInputUtility::getStringWithSpace(full_name)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }

        while (true) {
            cout << "Enter address : ";
            if(!HandleInputUtility::getStringWithSpace(address)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }
        
        while (true) {
            cout << "Enter email id : ";
            if(!HandleInputUtility::getStringWithSpace(email_address)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }

        UserType user_type;
        while(true) {
            cout << "Press (A) for Librarian or (B) for Member : ";
            char ch;
            if(!HandleInputUtility::getChar(ch)) {
                cout << "Invalid input. Please enter valid character." << endl;
                continue;
            }

            if(ch == 'A') {
                user_type = UserType::LIBRARIAN_TYPE;
                break;
            } else if(ch == 'B') {
                user_type = UserType::MEMBER_TYPE;
                break;
            } else {
                cout << "Please enter valid option." << endl;
            }
        }
        
        if(lb_management->registerNewUser(user_name, password, full_name, address, email_address, user_type)) {
            logged_user_type = user_type;
        } else {
            cout << "Can't register new user. Please try again..." << endl;
            is_failed = true;
        }
    }
};

#endif