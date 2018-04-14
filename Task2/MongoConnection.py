import pymongo
from pymongo import MongoClient

conn = MongoClient()
db = conn['Task2']
user_db = db.user
book_db = db.book
user_db.create_index([('Username', pymongo.ASCENDING)],unique=True)
book_db.create_index([('ISBN', pymongo.ASCENDING)],unique=True)


def clear_db(name):
    conn.drop_database(name)

##Adding
def add_book(Title, ISBN, Page, Author):
    new_entry = {'ISBN': ISBN,
                 'Title': Title,
                 'Page': Page,
                 'Author': Author,
                 'Copies': 1,
                 'CheckedOut': 0,
                 'Borrowers': []}
    if check_if_book_exist(ISBN):
        ls = book_db.insert_one(new_entry)
        return True
    elif book_db.find({'ISBN': ISBN,
                       'Title': Title,
                       'Page': Page,
                        'Author': Author,}).count() ==1:
        book_db.update_one({'ISBN': ISBN},
                           {'$inc': {'Copies': 1}})
        return True
    else:
        return False


def check_if_book_exist(ISBN):
    '''

    :param ISBN:
    :return: True if the book does not exist
            False if the book does exist
    '''
    return book_db.find({'ISBN':ISBN}).count() == 0


def add_user(name,username,phone):
    new_entry = {'Username': username,
                 'Name': name,
                 'Phone': phone,
                 'Checkout': []}
    if check_if_username_exist(username):
        ls = user_db.insert_one(new_entry)
        return True
    else:
        return False


def check_if_username_exist(username):
    '''

    :param username:
    :return: True if the book does not exist
            False if the book does exist
    '''
    return user_db.find({'Username':username}).count() == 0

##Deleting
def delete_book(ISBN):
    if not check_if_book_exist(ISBN):
        bk_data = retrieve_book_by_ISBN(ISBN)
        for users in bk_data.get('Borrowers'):
            return_book(ISBN, users)
        result = book_db.delete_many({'ISBN':ISBN})
        return result.deleted_count() == 1
    return False


def delete_username(username):
    if not check_if_username_exist(username):
        user_data = retrieve_user_by_username(username)
        for bk in user_data.get('Checkout'):
            return_book(bk, username)
        result = user_db.delete_many({'Username':username})
        return result.deleted_count() == 1
    return False

##Editing
def edit_book_title(ISBN,title):
    result = book_db.update_one({'ISBN': ISBN},
                                {'$set': {'Title' : title}})
    return result is not None


def edit_book_page_count(ISBN,page_count):
    result = book_db.update_one({'ISBN': ISBN},
                                {'$set': {'Page': page_count}})
    return result is not None


def edit_book_author(ISBN,author):
    result = book_db.update_one({'ISBN': ISBN},
                                {'$set': {'Author': author}})
    return result is not None


def edit_user_name(username, name):
    result = user_db.update_one({'Username': username},
                                {'$set': {'Name': name}})
    return result is not None


def edit_user_phone(username, phone):
    result = user_db.update_one({'Username': username},
                                {'$set': {'Phone': phone}})
    return result is not None


##Searching
def retrieve_book_by_title(title):
    return book_db.find({'Title': title})


def retrieve_book_by_ISBN(ISBN):
    return book_db.find_one({'ISBN': ISBN})


def retrieve_book_by_author(author):
    return book_db.find({'Author': author})


def retrieve_user_by_username(username):
    return user_db.find_one({'Username': username})


def retrieve_user_by_name(name):
    return user_db.find({'Name': name})


##Display
def retrieve_all_books():
    return book_db.find()


def retrieve_all_users():
    return user_db.find()


def retrieve_books_sorted_by_pages():
    return book_db.find().sort("Page", pymongo.ASCENDING)


def retrieve_books_sorted_by_ISBN():
    return book_db.find().sort("ISBN", pymongo.ASCENDING)


def retrieve_books_sorted_by_title():
    return book_db.find().sort("Title", pymongo.ASCENDING)


def retrieve_books_sorted_by_authors():
    pass


def retrieve_users_by_active_checkout():
    pass


def retrieve_users_by_checkouts():
    pass


##Checkout and Return
def checkout_book(ISBN,username):
    if not check_if_book_exist(ISBN) and not check_if_username_exist(username):
        bk_data = retrieve_book_by_ISBN(ISBN)
        if bk_data.get('CheckedOut')<bk_data.get('Copies'):
            result1 = user_db.update_one({'Username': username},
                                        {'$push': {'Checkout': ISBN}})

            result2 = book_db.update_one({'ISBN':ISBN},
                                        {'$inc': {'CheckedOut': 1}})
            result3 = book_db.update_one({'ISBN': ISBN},
                                        {'$push': {'Borrowers': username}})
            return result1 is not None and \
                   result2 is not None and \
                   result3 is not None
    return False


def return_book(ISBN,username):
    if not check_if_book_exist(ISBN) and not check_if_username_exist(username):
        user_data = retrieve_user_by_username(username)
        if ISBN in user_data.get('Checkout'):
            result1 = user_db.update_one({'Username': username},
                                         {'$pull': {'Checkout': ISBN}})
            result2 = book_db.update_one({'ISBN': ISBN},
                                         {'$inc': {'CheckedOut': -1}})
            result3 = book_db.update_one({'ISBN': ISBN},
                                         {'$pull': {'Borrowers': username}})
            return result1 is not None and \
                   result2 is not None and \
                   result3 is not None
    return False