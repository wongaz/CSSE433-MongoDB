import MongoConnection as mc

prompt = "(a)dd, (d)elete, (e)dit, (s)earch, (l)ookup, (c)heckout, (r)eturn, (h)elp"


def pretty_print_users(user_info):
    print('Name\t\t', user_info.get('Name'))
    print('Username\t', user_info.get('Username'))
    print('Phone\t\t', user_info.get('Phone'))
    print('Checkouts\t', user_info.get('Checkout'))
    print("----------------------------------------------------------------------------")


def pretty_print_books(bk_info):
    print("Title\t\t\t", bk_info.get('Title'))
    print("Authors\t\t\t", bk_info.get('Author'))
    print("ISBN\t\t\t", bk_info.get('ISBN'))
    print("Page\t\t\t", bk_info.get('Page'))
    print("Copies\t\t\t", bk_info.get('Copies'))
    print("Checked Out \t", bk_info.get('CheckedOut'))
    print("Borrowers \t\t", bk_info.get('Borrowers'))
    print("----------------------------------------------------------------------------")


def add_new():
    def add_new_book():
        title = str(input(">>>>(title):")).strip()
        try:
            number_of_authors = int(input(">>>>(number of authors):"))
        except ValueError:
            print("ERROR")
            return

        author = []

        for _ in range(number_of_authors):
            new_author = str(input(">>>>(author):")).strip()
            if len(new_author) != 0:
                author.append(new_author)
            else:
                print("ERROR")
                return

        ISBN = str(input(">>>>(ISBN):")).strip()
        try:
            page_count = str(input(">>>>(page count):")).strip()

        except ValueError:
            print("ERROR")
            return

        if len(title) != 0 and \
                len(author) != 0 and \
                len(ISBN) != 0 and \
                len(page_count) != 0 and \
                mc.add_book(title, ISBN, page_count, author):

            print("OK")
        else:
            print("ERROR")

    def add_new_borrow():
        name = str(input(">>>>(name):")).strip()
        username = str(input(">>>>(username):")).strip()
        phone = str(input(">>>>(phone):")).strip()
        if len(name) != 0 and \
                len(username) != 0 and \
                len(phone)!=0 and \
                mc.add_user(name, username, phone):

            print("OK")
        else:
            print("ERROR")

    print("options to (1)book or (2)borrower:")
    select = str(input(">>>>(select):")).strip()
    if select == '1':
        add_new_book()
    elif select == '2':
        add_new_borrow()


def edit_entry():
    def edit_user():
        print("Editing User Information by username. If you want to keep the information the same leave blank.")
        username = str(input(">>>>(username):")).strip()
        name = str(input(">>>>(name):")).strip()
        phone = str(input(">>>>(phone):")).strip()
        if not mc.check_if_username_exist(username):
            if len(name) != 0:
                mc.edit_user_name(username, name)
            if len(phone) != 0:
                mc.edit_user_phone(username, phone)
            print("OK")
        else:
            print("ERROR")

    def edit_book():
        print("Editing Book Information by ISBN. If you want to keep the information the same leave blank.")
        ISBN = str(input(">>>>(ISBN):")).strip()
        if not mc.check_if_book_exist(ISBN):
            title = str(input(">>>>(title):")).strip()

            try:
                number_of_authors = input(">>>>(number of authors):")
                author = []
                if len(number_of_authors) != 0:
                    number_of_authors = int(number_of_authors)
                    for _ in range(number_of_authors):
                        new_author = str(input(">>>>(author):")).strip()
                        if len(new_author) != 0:
                            author.append(new_author)

                page_count = input(">>>>(page count):")
                if type(page_count) is int or len(page_count) != 0:
                    page_count = int(page_count)

            except ValueError:
                print("ERROR")
                return

            if len(author) != 0:
                mc.edit_book_author(ISBN, author)
            if len(title) != 0:
                mc.edit_book_title(ISBN, title)
            if type(page_count) is int:
                mc.edit_book_page_count(ISBN, page_count)
            print("OK")
        else:
            print("ERROR")

    print("options to (1)book or (2)borrower:")
    select = str(input(">>>>(select):")).strip()
    if select == '1':
        edit_book()
    elif select == '2':
        edit_user()


def delete_from_mongo():
    def delete_book():
        ISBN = str(input(">>>>(ISBN):")).strip()
        res = mc.delete_book(ISBN)
        if res:
            print("OK")
        else:
            print("ERROR")

    def delete_borrower():
        username = str(input(">>>>(username):")).strip()
        res = mc.delete_username(username)
        if res:
            print("OK")
        else:
            print("ERROR")

    print("options to (1)book or (2)borrower:")
    select = str(input(">>>>(select):")).strip()
    if select == '1':
        delete_book()
    elif select == '2':
        delete_borrower()


def searching():
    def search_by_ISBN():
        print("ISBN to search for:")
        ISBN = str(input(">>>>(ISBN):")).strip()
        res = mc.retrieve_book_by_ISBN(ISBN)
        print(res)
        if res != 0:
            pretty_print_books(res)
        else:
            print("ERROR")

    def search_by_title():
        print("title to search for:")
        title = str(input(">>>>(title):")).strip()
        res = mc.retrieve_book_by_title(title)
        if res.count() != 0:
            for bk in res:
                pretty_print_books(bk)
        else:
            print("ERROR")

    def search_by_author():
        print("author to search for:")
        author = str(input(">>>>(author):")).strip()
        res = mc.retrieve_book_by_author(author)
        if res.count() != 0:
            for bk in res:
                pretty_print_books(bk)
        else:
            print("ERROR")

    def search_by_name():
        print("name to search for:")
        name = str(input(">>>>(name):")).strip()
        res = mc.retrieve_user_by_name(name)
        if res != 0:
            for keys in res:
                pretty_print_users(keys)
        else:
            print("ERROR")

    def search_by_username():
        print("name to search for:")
        name = str(input(">>>>(username):")).strip()
        res = mc.retrieve_user_by_username(name)
        if res != 0:
            pretty_print_users(res)
        else:
            print("ERROR")

    print("options to search: (t)itles, (a)uthors, (I)SBNs, (n)ames and (u)sername")
    select = str(input(">>>>(select):")).strip().lower()
    if select.startswith('a') or select == 'authors':
        search_by_author()
    elif select.startswith('t') or select == 'titles':
        search_by_title()
    elif select.startswith('i') or select == 'isbns':
        search_by_ISBN()
    elif select.startswith('n') or select == 'names':
        search_by_name()
    elif select.startswith('u') or select == 'username':
        search_by_username()
    else:
        print("nothing was selected")


def display_books():
    def display_books_by_title():
        for k in mc.retrieve_books_sorted_by_title():
            pretty_print_books(k)

    def display_books_by_author():
        for k in mc.retrieve_books_sorted_by_authors():
            pretty_print_books(k)

    def display_books_by_ISBN():
        for k in mc.retrieve_books_sorted_by_ISBN():
            pretty_print_books(k)

    def display_books_by_pages():
        for k in mc.retrieve_books_sorted_by_pages():
            pretty_print_books(k)

    def display_users_by_checkouts():
        for k in mc.retrieve_users_by_checkouts():
            pretty_print_users(k)

    def display_users_by_active_checkouts():
        for k in mc.retrieve_users_by_active_checkout():
            pretty_print_users(k)

    def display_all_books():
        for k in mc.retrieve_all_books():
            pretty_print_books(k)

    def display_all_users():
        for k in mc.retrieve_all_users():
            pretty_print_users(k)

    print("Display books by:"
          "(t)itle, (a)uthors, (I)SBN, (p)age#, "
          "(c)heckouts by user, (l)ive checkouts,(1)books, and (2)users")

    inpt = str(input(">>>>(selection):")).strip().lower()
    if inpt.startswith("t"):
        display_books_by_title()
    elif inpt.startswith("a"):
        display_books_by_author()
    elif inpt.startswith("i"):
        display_books_by_ISBN()
    elif inpt.startswith("p"):
        display_books_by_pages()
    elif inpt.startswith("c"):
        display_users_by_checkouts()
    elif inpt.startswith("l"):
        display_users_by_active_checkouts()
    elif inpt.startswith('1'):
        display_all_books()
    elif inpt.startswith('2'):
        display_all_users()
    else:
        print("ERROR")


def checkout_book():
    username = str(input(">>>>(username):")).strip()
    isbn = str(input(">>>>(isbn):")).strip()
    if mc.checkout_book(isbn, username):
        print("OK")
    else:
        print("ERROR")


def return_book():
    username = str(input(">>>>(username):")).strip()
    isbn = str(input(">>>>(isbn):")).strip()
    if mc.return_book(username, isbn):
        print("OK")
    else:
        print("ERROR")


def main():
    print("Welcome to the Library")
    print("commands include:", prompt)
    while True:
        inpt = str(input(">>>")).strip().lower()
        if inpt.startswith('a') or inpt == 'add':
            add_new()

        elif inpt.startswith('d') or inpt == 'del':
            delete_from_mongo()

        elif inpt.startswith('s') or inpt == 'search':
            searching()

        elif inpt.startswith('l') or inpt == 'lookup':
            display_books()

        elif inpt.startswith('e') or inpt == 'edit':
            edit_entry()

        elif inpt.startswith('c') or inpt == 'checkout':
            checkout_book()

        elif inpt.startswith('r') or inpt == 'returns':
            return_book()

        elif inpt.startswith('h'):
            print(prompt)
        else:
            print("Valid commands:", prompt)


if __name__ == '__main__': main()