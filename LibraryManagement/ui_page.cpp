#ifndef UIPAGE_H
#define UIPAGE_H

#include <string>

#include "library_management.cpp"

class UIPage {
protected:
    string page_name;
    UIPage* prev_page;
public:
    UIPage(string _page_name) {
        page_name = _page_name;
        prev_page = nullptr;
    }

    void setPrevPage(UIPage* page) {
        prev_page = page;
    }

    string getPageName() {
        return page_name;
    }

    virtual string getNextPageName() = 0;

    virtual void showPage(LibraryManagement *lb_management) = 0;
};

#endif // UIPAGE_H