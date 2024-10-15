#ifndef BOOKS_VIEW_UTILITY_H
#define BOOKS_VIEW_UTILITY_H

#include<iostream>
#include <vector>

#include "book.cpp"

class BooksViewUtility {
public:
    static void showBooks(const vector<Book*> &books) {
        cout << "\n\n";
        if(books.size() == 0) {
            cout << "No books is found!\n\n";
            return;
        }

        int idx = 1;
        for(Book* book : books) {
            cout << idx << "." << "\tTitle : " << book->getTitle() << endl;
            cout << "\tAuthors : " << endl;
            for(string author : book->getAuthors()) {
                cout << "\t\t" << author << endl;
            }
            cout << "\tPublisher : " << book->getPublisher() << endl;
            cout << "\tCategory : " << CategoryUtils::GetCategoryName(book->getCategory()) << endl;
            cout << "\tShelf Location -> floor number : " << book->getShelfLocation().floor_number << ", shelf number : " << book->getShelfLocation().shelf_number << endl;
            cout << "\tIs book available : " << (book->getAvailabilityStatus() ? "True" : "False") << endl;
            cout << "\n\n";
            idx++;
        }
    }
};

#endif