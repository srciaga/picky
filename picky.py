"""picky.py by srciaga"""

import pyinputplus as pyip
import random
import os

BOOK_LIST = "booklist.txt"
TEMP_FILE = "temp.txt"
MENU_OPTIONS = (
    "Quit",
    "Get random book",
    "See list of books",
    "Add book to list",
    "Remove book from list",
)


def main():
    """Starts the program."""

    check_booklist_txt()
    main_menu()


def check_booklist_txt():
    """Checks if booklist.txt exists. If not, it's created."""

    try:
        with open(BOOK_LIST, "r") as f:
            f.readline()
    except FileNotFoundError:
        with open(BOOK_LIST, "a") as f:
            f.write("")


def main_menu():
    """Prints the menu, accepts input, and calls the
    corresponding function."""

    selection = pyip.inputMenu(
        MENU_OPTIONS,
        numbered=True,
    )

    # Menu selection.
    if selection == MENU_OPTIONS[0]:
        exit()
    elif selection == MENU_OPTIONS[1]:
        get_rand_book()
    elif selection == MENU_OPTIONS[2]:
        see_list()
    elif selection == MENU_OPTIONS[3]:
        add_book()
    elif selection == MENU_OPTIONS[4]:
        remove_book()


def wait_menu():
    """Allows user to:
    - Exit the program with q.
    - Wait until user hits enter to show the menu."""

    WAIT_OPTIONS = ("q", "")

    status = pyip.inputChoice(
        WAIT_OPTIONS,
        prompt="Hit enter to continue or q to quit.\n",
        blank=True,
    )
    if status == WAIT_OPTIONS[0]:
        exit()
    elif status == WAIT_OPTIONS[1]:
        main_menu()


def print_list():
    """Prints the contents of booklist.txt"""

    with open(BOOK_LIST, "r") as f:

        # Check if the first line is empty. If not, move on.
        book_id = f.readline()
        if book_id == "":
            print("\nThe list is empty.")
        else:
            print("\nCurrent list of books:")
            while book_id != "":
                book = f.readline()
                # Strip \n
                book_id = book_id.rstrip("\n")
                book = book.rstrip("\n")
                # Print, then continue reading.
                print(f"{book_id} {book}")
                book_id = f.readline()


def see_list():
    """Prints booklist.txt and waits for user to continue."""

    print_list()
    wait_menu()


def get_rand_book():
    """Picks a random book from booklist.txt."""

    with open(BOOK_LIST, "r") as f:
        # Check if the list is empty, if not, continue.
        book_id = f.readline()
        if book_id == "":
            print("Sorry, the list is empty.")
        else:
            # Add books to a list.
            books = []
            while book_id != "":
                book_title = f.readline()
                books.append(book_title)
                book_id = f.readline()

            # Pick a random book.
            print("\nHere's a random book:")
            print(random.choice(books))
    # Display menu when done.
    wait_menu()


def add_book():
    """Adds book(s) to booklist.txt."""

    print("\nEnter 0 when you're done.")
    book_entry = None  # Prepare for loop
    book_id = 0  # Prepare for loop
    while book_entry != "0":
        with open(BOOK_LIST, "a") as f:
            book_entry = input("Add book: ")
            # If done, don't write anything.
            if book_entry == "0":
                pass
            else:
                book_id += 1
                f.write(f"{book_id}.\n")
                f.write(f"{book_entry}\n")

    renumber_list()

    # Display menu when done.
    print("Done!\n")
    wait_menu()


def remove_book():
    """Removes book(s) from booklist.txt."""

    found = False  # bool flag

    # Print book list.
    print_list()

    with open(BOOK_LIST, "r") as original_list:
        # Check if the file is empty, if not, continue reading.
        book_id = original_list.readline()
        if book_id == "":
            print("You can't delete books from an empty list.")
        else:
            # Ask user what book to delete.
            search = input("Enter the number of the book you want to delete: ")

            while book_id != "":
                # Read the book title field.
                book_title = original_list.readline()

                # Strip the ID for the search.
                book_id = book_id.rstrip(".\n")
                with open(TEMP_FILE, "a") as temp_list:
                    # If this is not the book to delete, write it to
                    # the temporary file.
                    if book_id != search:
                        temp_list.write(f"{book_id}.\n")
                        temp_list.write(f"{book_title}")
                    else:
                        # Set the found flag to True.
                        found = True

                # Continue reading.
                book_id = original_list.readline()

            delete_rename_files()

            renumber_list()

    # If the search value was not found in the file
    # display a message.
    if found:
        print("The list has been updated.")
        wait_menu()
    else:
        wait_menu()


def delete_rename_files():
    """Delete the original booklist.txt and rename temp.txt."""

    os.remove(BOOK_LIST)
    os.rename(TEMP_FILE, BOOK_LIST)


def renumber_list():
    """Properly numbers the list after adding or removing books."""

    with open(BOOK_LIST, "r") as original_list, open(TEMP_FILE, "w") as temp_list:
        book_id = original_list.readline()
        count = 0
        while len(book_id) == 3:
            count += 1
            temp_list.write(f"{count}.\n")
            book_title = original_list.readline()
            temp_list.write(f"{book_title}")
            book_id = original_list.readline()

        delete_rename_files()


# Call the main function.
if __name__ == "__main__":
    main()
