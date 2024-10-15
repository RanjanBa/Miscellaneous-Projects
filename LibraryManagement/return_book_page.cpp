#ifndef RETURN_BOOK_H
#define RETURN_BOOK_H

#include "library_management.cpp"
#include "handle_input_utility.cpp"
#include "all_page_names.cpp"
#include "ui_page.cpp"
#include "books_view_utility.cpp"

class ReturnBookPage : public UIPage 
{
public:
    ReturnBookPage(string _page_name) : UIPage(_page_name) { }

    string getNextPageName() {
        return AllPageNames::memberPageName;
    }

    void showPage(LibraryManagement *lb_management) {
        const vector<Book*> borrowed_books = lb_management->getLoggedUser()->getAllBorrowedBooks();
        BooksViewUtility::showBooks(borrowed_books);

        if(borrowed_books.size() > 0) {
            while (true) {
                int option;
                cout << "Please enter number between 1 - " << borrowed_books.size() << " to select book : ";
                if(!HandleInputUtility::getNumber(option)) {
                    cout << "Invalid input. Please enter a number between 1 and 3." << endl;
                    continue;
                }

                if(option <= 0 || option > borrowed_books.size()) {
                    cout << "Number is out of range. Please enter valid number." << endl;
                    continue;
                }

                Book* selected_book = borrowed_books[option - 1];
                if(lb_management->getLoggedUser()->returnBook(selected_book)) {
                    cout << "You return book with title : " << selected_book->getTitle() << endl;
                } else {
                    cout << "You can't return book with title : " << selected_book->getTitle() << endl;
                }
                return;
            }
        }
    }
};

#endif