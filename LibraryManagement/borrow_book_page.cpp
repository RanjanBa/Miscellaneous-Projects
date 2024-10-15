#ifndef BORROW_BOOK_H
#define BORROW_BOOK_H

#include <string>
#include "library_management.cpp"
#include "all_page_names.cpp"
#include "handle_input_utility.cpp"
#include "ui_page.cpp"
#include "search_book_utility.cpp"
#include "books_view_utility.cpp"

class BorrowBookPage : public UIPage {
public:
    BorrowBookPage(string _page_name) : UIPage(_page_name) {}

    string getNextPageName() {
        return AllPageNames::memberPageName;
    }

    void showPage(LibraryManagement* lb_management) {
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
            if(search_results.size() > 0) {
                while (true) {
                    int option;
                    cout << "Please enter number between 1 - " << search_results.size() << " to select book : ";
                    if(!HandleInputUtility::getNumber(option)) {
                        cout << "Invalid input. Please enter a number between 1 and 3." << endl;
                        continue;
                    }

                    if(option <= 0 || option > search_results.size()) {
                        cout << "Number is out of range. Please enter valid number." << endl;
                        continue;
                    }

                    Book* selected_book = search_results[option - 1];
                    if(lb_management->getLoggedUser()->addBorrowedBook(selected_book)) {
                        cout << "You are borrowing book with title : " << selected_book->getTitle() << endl;
                    } else {
                        cout << "You can't borrow book with title : " << selected_book->getTitle() << endl;
                    }
                    return;
                }
            }
        }
    }
};

#endif