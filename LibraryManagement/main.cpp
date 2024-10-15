#include <iostream>

#include "library_management.cpp"
#include "all_page_names.cpp"
#include "ui_page.cpp"
#include "main_menu_page.cpp"
#include "login_page.cpp"
#include "registration_page.cpp"
#include "librarian_page.cpp"
#include "member_page.cpp"
#include "add_book_page.cpp"
#include "search_book_page.cpp"
#include "borrow_book_page.cpp"
#include "return_book_page.cpp"

using namespace std;

LibraryManagement* manager = new LibraryManagement();
AllPageNames* all_page_names = new AllPageNames();

void AddAllPages() {
    all_page_names->addNewPage(new MainMenuPage(AllPageNames::mainMenuPageName));
    all_page_names->addNewPage(new LogInPage(AllPageNames::loginPageName));
    all_page_names->addNewPage(new RegistrationPage(AllPageNames::registrationPageName));
    all_page_names->addNewPage(new LibrarianPage(AllPageNames::librarianPageName));
    all_page_names->addNewPage(new MemberPage(AllPageNames::memberPageName));
    all_page_names->addNewPage(new SearchBookPage(AllPageNames::searchBookPageName));
    all_page_names->addNewPage(new AddBookPage(AllPageNames::addBookPageName));
    all_page_names->addNewPage(new BorrowBookPage(AllPageNames::borrowBookPageName));
    all_page_names->addNewPage(new ReturnBookPage(AllPageNames::returnBookPageName));
}

int main() {
    AddAllPages();

    UIPage* current_page = all_page_names->getPage(AllPageNames::mainMenuPageName);
    while(current_page != nullptr) {
        cout << current_page->getPageName() << endl;
        current_page->showPage(manager);
        string next_page = current_page->getNextPageName();
        current_page = all_page_names->getPage(next_page);
    }

    return 0;
}