#ifndef ALL_PAGE_NAMES_H
#define ALL_PAGE_NAMES_H

#include <string>
#include <vector>

#include "ui_page.cpp"

using namespace std;

class AllPageNames {
private:
    vector<UIPage*> all_pages;
public:
    static const string mainMenuPageName;
    static const string loginPageName;
    static const string registrationPageName;
    static const string librarianPageName;
    static const string memberPageName;
    static const string searchBookPageName;
    static const string addBookPageName;
    static const string borrowBookPageName;
    static const string returnBookPageName;
    
    UIPage* getPage(string page_name) {
        for(auto page : all_pages) {
            if(page->getPageName() == page_name) return page;
        }

        return nullptr;
    }

    void addNewPage(UIPage* page) {
        all_pages.push_back(page);
    }
};

const string AllPageNames::mainMenuPageName = "Main Menu Page";
const string AllPageNames::loginPageName = "Login Page";
const string AllPageNames::registrationPageName = "Registration Page";
const string AllPageNames::librarianPageName = "Librarian Page";
const string AllPageNames::memberPageName = "Member Page";
const string AllPageNames::addBookPageName = "Add Book Page";
const string AllPageNames::searchBookPageName = "Search Book Page";
const string AllPageNames::borrowBookPageName = "Borrow Book Page";
const string AllPageNames::returnBookPageName = "Return Book Page";

#endif