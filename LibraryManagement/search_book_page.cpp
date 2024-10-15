#ifndef SEARCH_BOOK_H
#define SEARCH_BOOK_H

#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "all_page_names.cpp"
#include "ui_page.cpp"
#include "book.cpp"
#include "books_view_utility.cpp"
#include "search_book_utility.cpp"

class SearchBookPage : public UIPage {
private:
    UserType user_type;
public:
    SearchBookPage(string _page_name) : UIPage(_page_name) { }

    string getNextPageName() {
        if(user_type == UserType::LIBRARIAN_TYPE) {
            return AllPageNames::librarianPageName;
        }
        return AllPageNames::memberPageName;
    }

    void showPage(LibraryManagement* lb_management) {
        cout << "Search Book Page" << endl;

        while (true) {
            cout << "\t1. Search By Title" << endl;
            cout << "\t2. Search By Authors" << endl;
            cout << "\t3. Search By Publisher" << endl;

            int option;
            cout << "Please select Your Option (1-3) : ";
            if(!HandleInputUtility::getNumber(option)) {
                cout << "Invalid input. Please enter a number between 1 and 3." << endl;
                continue;
            }

            const vector<Book*> books = lb_management->getBooks();
            vector<Book*> search_results;
            cin.sync();
            if(option == 1) {
                string search_title;
                while (true) {
                    cout << "Enter book's title to search : ";
                    if(!HandleInputUtility::getStringWithSpace(search_title)) {
                        cout << "Invalid input. Please enter valid string." << endl;
                    } else {
                        break;
                    }
                }

                search_results = SearchBookUtility::seacrhByTitle(search_title, books);
            } else if(option == 2) {
                string search_author;
                while (true) {
                    cout << "Enter book's author to search : ";
                    if(!HandleInputUtility::getStringWithSpace(search_author)) {
                        cout << "Invalid input. Please enter valid string." << endl;
                    } else {
                        break;
                    }
                }

                search_results = SearchBookUtility::seacrhByAuthor(search_author, books);
            } else if(option == 3) {
                string search_publisher;
                while (true) {
                    cout << "Enter book's publisher to search : ";
                    if(!HandleInputUtility::getStringWithSpace(search_publisher)) {
                        cout << "Invalid input. Please enter valid string." << endl;
                    } else {
                        break;
                    }
                }
                
                search_results = SearchBookUtility::seacrhByPublisher(search_publisher, books);
            } else {
                cout << "Please select valid option." << endl;
                continue;
            }

            BooksViewUtility::showBooks(search_results);
            break;
        }

        if(lb_management->getLoggedUser()->getUserType() == UserType::LIBRARIAN_TYPE) {
            user_type = UserType::LIBRARIAN_TYPE;
            return;
        }

        user_type = UserType::MEMBER_TYPE;
    }
};

#endif