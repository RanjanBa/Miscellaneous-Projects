#ifndef LIBRARY_H
#define LIBRARY_H

#include <iostream>
#include <vector>
#include <string>

#include "user.cpp"
#include "book.cpp"

using namespace std;

class LibraryManagement {
private:
    vector<User*> users;
    vector<Book*> books;
    User* logged_user;
public:
    LibraryManagement() {
        logged_user = NULL;
    }

    bool registerNewUser(string user_name, string password, string title, string address, string email_address, UserType user_type) {
        User *user = new User(users.size(), user_name, password, title, address, email_address, user_type);
        users.push_back(user);
        logged_user = user;
        return true;
    }

    bool login(string user_name, string password) {
        for(User *user : users) {
            if(user->getUserName() == user_name && user->getPassword() == password) {
                logged_user = user;
                return true;
            }
        }

        return false;
    }

    bool logout() {
        logged_user = NULL;
        return true;
    }

    User* getLoggedUser() {
        return logged_user;
    }

    bool addBook(string title, vector<string> authors, string publisher, Category category, bool availability_status, Location shelf_location) {
        Book *book = new Book(books.size(), title, authors, publisher, category, availability_status, shelf_location);
        books.push_back(book);
        return true;
    }

    const vector<Book*> &getBooks() {
        return books;
    }
};

#endif // LIBRARY_H