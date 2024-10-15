#ifndef ADD_BOOK_H
#define ADD_BOOK_H

#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "all_page_names.cpp"
#include "ui_page.cpp"
#include "book.cpp"

// int book_id;
// string title;
// vector<string> authors;
// string publisher;
// Category category;
// bool availability_status;
// Location shelf_location;

class AddBookPage : public UIPage {
private:
    string getNumberString(int number) {
        if(number == 1) {
            return "1st";
        } else if(number == 2) {
            return "2nd";
        } else if(number == 3) {
            return "3rd";
        }

        return to_string(number) + "th";
    }
public:
    AddBookPage(string _page_name) : UIPage(_page_name) { }

    string getNextPageName() {
        return AllPageNames::librarianPageName;
    }

    void showPage(LibraryManagement* lb_management) {
        string title;
        vector<string> authors;
        string publisher;
        Category category;
        Location shelf_location;
        cin.sync();

        while (true) {
            cout << "Enter book title : ";
            if(!HandleInputUtility::getStringWithSpace(title)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }
        
        int authors_count = 0;
        while(true) {
            cout << "Enter number of authors : ";

            if(!HandleInputUtility::getNumber(authors_count)) {
                cout << "Invalid input. Please enter valid number." << endl;
                continue;
            }

            if(authors_count <= 0) {
                cout << "Pleas enter valid number of authors." << endl;
            } else {
                break;
            }
        }

        for(int i = 1; i <= authors_count; i++) {
            string author;
            while (true) {
                cout << "Enter " << getNumberString(i) << " author name : ";
                
                if(!HandleInputUtility::getStringWithSpace(author)) {
                    cout << "Invalid input. Please enter valid string." << endl;
                } else {
                    break;
                }
            }
            
            authors.push_back(author);
        }

        while (true) {
            cout << "Enter publisher name : ";
            if(!HandleInputUtility::getStringWithSpace(publisher)) {
                cout << "Invalid input. Please enter valid string." << endl;
            } else {
                break;
            }
        }
        
        const vector<string> &categories = CategoryUtils::GetAllCategoryNames();
        string instruction;
        for (int i = 0; i < categories.size(); i++)
        {
            string str(1, char('A' + i));
            instruction += "Press (" + str + ") for " + categories[i];
            if(i < categories.size() - 1) {
                instruction += ", ";
            }
        }

        char option;
        while (true) {
            cout << instruction << " : ";
            if(!HandleInputUtility::getChar(option)) {
                cout << "Invalid input. Please enter valid character." << endl;
                continue;
            }

            if('A' <= option && option <= 'A' + (categories.size()-1)) {
                break;
            } else {
                cout << "Please enter valid option." << endl;
            }
        }

        int index = option - 'A';
        category = CategoryUtils::GetCategory(categories[index]);

        while (true)
        {
            cout << "Enter floor number : ";
            if(!HandleInputUtility::getNumber(shelf_location.floor_number)) {
                cout << "Invalid input. Please enter valid number." << endl;
                continue;
            }

            if(shelf_location.floor_number < 0) {
                cout << "Please enter valid floor number." << endl;
            } else {
                break;
            }
        }

        while (true)
        {
            cout << "Enter shelf number : ";
            if(!HandleInputUtility::getNumber(shelf_location.shelf_number)) {
                cout << "Invalid input. Please enter valid number." << endl;
                continue;
            }
            if(shelf_location.shelf_number < 0) {
                cout << "Please enter valid shelf number." << endl;
            } else {
                break;
            }
        }

        if(lb_management->addBook(title, authors, publisher, category, true, shelf_location)) {
            return;
        } else {
            cout << "Please enter valid book's info." << endl;
        }
    }
};

#endif