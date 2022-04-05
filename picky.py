"""picky.py by srciaga"""

import pyinputplus as pyip
import random
import os


def main():
    """Starts the program."""
    ask_for_category()


def ask_for_category():
    """Asks user for list category, which will temporarily change the
    text and filenames for the program."""

    global CATEGORY
    CATEGORY = input(
        "What category do you want to work with?"
        + "\nPlease enter a single word. (examples: books, movies)\n"
    )

    # Create file paths.
    global LIST_PATH
    LIST_PATH = f"{CATEGORY}list.txt"
    global TEMP_FILE
    TEMP_FILE = "temp.txt"

    # Create menu options.
    global MENU_OPTIONS
    MENU_OPTIONS = (
        "Quit",
        f"Get random {CATEGORY}",
        f"See list of {CATEGORY}",
        f"Add {CATEGORY} to list",
        f"Remove {CATEGORY} from list",
        f"Switch to a different category."
    )

    print("\n")
    start_up()


def start_up():
    """Calls check_list_txt() then main_menu(). Only used at the end of
    the ask_for_category() function."""

    check_list_txt()
    main_menu()


def check_list_txt():
    """Checks if {CATEGORY}list.txt exists. If not, it's created."""

    try:
        with open(LIST_PATH, "r") as f:
            f.readline()
    except FileNotFoundError:
        with open(LIST_PATH, "a") as f:
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
        get_rand_item()
    elif selection == MENU_OPTIONS[2]:
        see_list()
    elif selection == MENU_OPTIONS[3]:
        add_item()
    elif selection == MENU_OPTIONS[4]:
        remove_item()
    elif selection == MENU_OPTIONS[5]:
        ask_for_category()


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


def print_items():
    """Prints the contents of {CATEGORY}list.txt"""

    with open(LIST_PATH, "r") as f:

        # Check if the first line is empty. If not, move on.
        item_id = f.readline()
        if item_id == "":
            print("\nThe list is empty.")
        else:
            print(f"\nCurrent list of {CATEGORY}:")
            while item_id != "":
                item = f.readline()
                # Strip \n
                item_id = item_id.rstrip("\n")
                item = item.rstrip("\n")
                # Print, then continue reading.
                print(f"{item_id} {item}")
                item_id = f.readline()


def see_list():
    """Prints {CATEGORY}list.txt and waits for user to continue."""

    print_items()
    wait_menu()


def get_rand_item():
    """Picks a random item from {CATEGORY}list.txt."""

    with open(LIST_PATH, "r") as f:
        # Check if the list is empty, if not, continue.
        item_id = f.readline()
        if item_id == "":
            print("Sorry, the list is empty.")
        else:
            # Add items to a list.
            items = []
            while item_id != "":
                item_title = f.readline()
                items.append(item_title)
                item_id = f.readline()

            # Pick a random item.
            print("\nHere's a random item:")
            print(random.choice(items))
    # Display menu when done.
    wait_menu()


def add_item():
    """Adds item(s) to {CATEGORY}list.txt."""

    print("\nEnter 0 when you're done.")
    item_entry = None  # Prepare for loop
    item_id = 0  # Prepare for loop
    while item_entry != "0":
        with open(LIST_PATH, "a") as f:
            item_entry = input("Add item: ")
            # If done, don't write anything.
            if item_entry == "0":
                pass
            else:
                item_id += 1
                f.write(f"{item_id}.\n")
                f.write(f"{item_entry}\n")

    renumber_list()

    # Display menu when done.
    print("Done!\n")
    wait_menu()


def remove_item():
    """Removes item(s) from {CATEGORY}list.txt."""

    found = False  # bool flag

    # Print item list.
    print_items()

    with open(LIST_PATH, "r") as original_list:
        # Check if the file is empty, if not, continue reading.
        item_id = original_list.readline()
        if item_id == "":
            print("You can't delete items from an empty list.")
        else:
            # Ask user what item to delete.
            search = input("Enter the number of the item you want to delete: ")

            while item_id != "":
                # Read the item title field.
                item_title = original_list.readline()

                # Strip the ID for the search.
                item_id = item_id.rstrip(".\n")
                with open(TEMP_FILE, "a") as temp_list:
                    # If this is not the item to delete, write it to
                    # the temporary file.
                    if item_id != search:
                        temp_list.write(f"{item_id}.\n")
                        temp_list.write(f"{item_title}")
                    else:
                        # Set the found flag to True.
                        found = True

                # Continue reading.
                item_id = original_list.readline()

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
    """Delete the original {CATEGORY}list.txt and rename temp.txt."""

    os.remove(LIST_PATH)
    os.rename(TEMP_FILE, LIST_PATH)


def renumber_list():
    """Properly numbers the list after adding or removing items."""

    with open(LIST_PATH, "r") as original_list, open(TEMP_FILE, "w") as temp_list:
        item_id = original_list.readline()
        count = 0
        while len(item_id) == 3:
            count += 1
            temp_list.write(f"{count}.\n")
            item_title = original_list.readline()
            temp_list.write(f"{item_title}")
            item_id = original_list.readline()

        delete_rename_files()


# Call the main function.
if __name__ == "__main__":
    main()
