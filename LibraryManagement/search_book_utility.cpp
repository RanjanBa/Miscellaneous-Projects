#ifndef SEARCH_BOOK_UTILITY_H
#define SEARCH_BOOK_UTILITY_H

#include<vector>
#include<algorithm>

#include "book.cpp"

class SearchBookUtility {
public:
    static vector<Book*> seacrhByTitle(string search_title, const vector<Book*> books) {
        vector<Book*> results;
        transform(search_title.begin(), search_title.end(), search_title.begin(), ::tolower);
        for(Book* book : books) {
            string title = book->getTitle();
            transform(title.begin(), title.end(), title.begin(), ::tolower);
            if(search_title == title) {
                results.push_back(book);
            }
        }

        return results;
    }

    static vector<Book*> seacrhByAuthor(string author_name, const vector<Book*> books) {
        vector<Book*> results;
        transform(author_name.begin(), author_name.end(), author_name.begin(), ::tolower);
        for(Book* book : books) {
            for(string author : book->getAuthors()) {
                transform(author.begin(), author.end(), author.begin(), ::tolower);
                if(author_name == author) {
                    results.push_back(book);
                }
            }
        }

        return results;
    }

    static vector<Book*> seacrhByPublisher(string publisher_name, const vector<Book*> books) {
        vector<Book*> results;
        transform(publisher_name.begin(), publisher_name.end(), publisher_name.begin(), ::tolower);
        for(Book* book : books) {
            string publisher = book->getPublisher();
            transform(publisher.begin(), publisher.end(), publisher.begin(), ::tolower);
            if(publisher_name == publisher) {
                results.push_back(book);
            }
        }

        return results;
    }
};

#endif