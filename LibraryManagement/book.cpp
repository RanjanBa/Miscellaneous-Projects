#ifndef BOOK_H
#define BOOK_H

#include<vector>
#include<string>

using namespace std;

enum class Category {
    ARTS,
    BIOGRAPHY,
    COMICS,
    COMPUTER_TECH,
    COOKING,
    ENTERTAINMENT,
    HEALTH_FITNESS,
    KIDS,
    LITERATURE,
    FICTION,
    MATH,
    SCIENCE,
    TRAVEL,
    OTHER
};

struct Location {
    int floor_number;
    int shelf_number;
};

class Book {
private:
    int book_id;
    string title;
    vector<string> authors;
    string publisher;
    Category category;
    bool availability_status;
    Location shelf_location;
public:
    Book(int _book_id, string _title, vector<string> _authors, string _publishers, Category _category, bool _availability_status, Location _shelf_location) {
        book_id = _book_id;
        title = _title;
        authors = _authors;
        publisher = _publishers;
        category = _category;
        availability_status = _availability_status;
        shelf_location = _shelf_location;
    }

    string getTitle() { return title; }
    vector<string> getAuthors() { return authors; }
    string getPublisher() { return publisher; }
    Category getCategory() { return category; }
    bool getAvailabilityStatus() { return availability_status; }
    Location getShelfLocation() { return shelf_location; }

    void makeAvailable() {
        availability_status = true;
    }
};

class CategoryUtils
{
public:
    static const vector<string>& GetAllCategoryNames() {
        static const vector<string> categories = {
            "ARTS",
            "BIOGRAPHY",
            "COMICS",
            "COMPUTER_TECH",
            "COOKING",
            "ENTERTAINMENT",
            "HEALTH_FITNESS",
            "KIDS",
            "LITERATURE",
            "FICTION",
            "MATH",
            "SCIENCE",
            "TRAVEL",
            "OTHER"
        };

        return categories;
    }

    static Category GetCategory(string name) {
        if("ARTS" == name) {
            return Category::ARTS;
        } else if("BIOGRAPHY" == name) {
            return Category::BIOGRAPHY;
        } else if("COMICS" == name) {
            return Category::COMICS;
        } else if("COMPUTER_TECH" == name) {
            return Category::COMPUTER_TECH;
        } else if("COOKING" == name) {
            return Category::COOKING;
        } else if("ENTERTAINMENT" == name) {
            return Category::ENTERTAINMENT;
        } else if("HEALTH_FITNESS" == name) {
            return Category::HEALTH_FITNESS;
        } else if("KIDS" == name) {
            return Category::KIDS;
        } else if("LITERATURE" == name) {
            return Category::LITERATURE;
        } else if("FICTION" == name) {
            return Category::FICTION;
        } else if("MATH" == name) {
            return Category::MATH;
        } else if("SCIENCE" == name) {
            return Category::SCIENCE;
        } else if("TRAVEL" == name) {
            return Category::TRAVEL;
        }

        return Category::OTHER;
    }

    static string GetCategoryName(Category category) {
        switch (category)
        {
            case Category::ARTS:
                return "Arts";
            case Category::BIOGRAPHY:
                return "Biography";
            case Category::COMICS:
                return "Comics";
            case Category::COMPUTER_TECH:
                return "Computer_tech";
            case Category::COOKING:
                return "Cooking";
            case Category::ENTERTAINMENT:
                return "Entertainment";
            case Category::HEALTH_FITNESS:
                return "Health_Fitness";
            case Category::KIDS:
                return "Kids";
            case Category::LITERATURE:
                return "Literature";
            case Category::FICTION:
                return "Fiction";
            case Category::MATH:
                return "Math";
            case Category::SCIENCE:
                return "Science";
            case Category::TRAVEL:
                return "Travel";
            default:
                return "Other";
        }
    }
};

#endif