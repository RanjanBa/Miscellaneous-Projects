#ifndef USER_H
#define USER_H

#include <vector>
#include <string>
#include "book.cpp"

using namespace std;

enum class UserType {
    LIBRARIAN_TYPE,
    MEMBER_TYPE
};

class User {
protected:
    int user_id;
    string user_name;
    string password;
    string full_name;
    string address;
    string email_address;
    UserType user_type;
    vector<Book*> borrowed_books;
public:
    User(int _user_id, string _user_name, string _password, string _full_name, string _address, string _email_address, UserType _user_type) {
        user_id = _user_id;
        user_name = _user_name;
        password = _password;
        full_name = _full_name;
        address = _address;
        email_address = _email_address;
        user_type = _user_type;
    }

    int getUserId() { return user_id; }
    string getUserName() { return user_name; }
    string getPassword() { return password; }
    string getFullName() { return full_name; }
    UserType getUserType() { return user_type; }

    const vector<Book*> getAllBorrowedBooks() {
        return borrowed_books;
    }

    bool addBorrowedBook(Book* book) {
        if(!book->getAvailabilityStatus()) return false;
        borrowed_books.push_back(book);
        return true;
    }

    bool returnBook(Book* book) {
        book->makeAvailable();
        return true;
    }
};

#endif // USER_H