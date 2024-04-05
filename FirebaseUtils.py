import uuid
import pyrebase
import firebase_admin
from firebase_admin import credentials, auth, firestore

firebaseConfig = {
    "apiKey": "AIzaSyCtuLuWLmU7KS2QZyi0VjLmj8K31vV1WoE",
    "authDomain": "bookstore-309b7.firebaseapp.com",
    "projectId": "bookstore-309b7",
    "storageBucket": "bookstore-309b7.appspot.com",
    "messagingSenderId": "555840721336",
    "appId": "1:555840721336:web:ba3983b7e3e3229c2aff4d",
    "measurementId": "G-PYJGKNHZWP",
    "databaseURL": "https://bookstore-309b7-default-rtdb.asia-southeast1.firebasedatabase.app/"
}

cred = credentials.Certificate("bookstore-firebase-admin-sdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

firebase = pyrebase.initialize_app(firebaseConfig)
firebase_auth = firebase.auth()
firebase_storage = firebase.storage()

def create_user(display_name, email, password, photo_url):
    try:
        res = auth.create_user(
            display_name=display_name,
            photo_url=photo_url,
            password=password,
            email=email,
        )

        print(res.uid)
        user = {
            "display_name" : display_name,
            "photo_url" : photo_url,
            "email" : email,
            "role" : "user",
            "id" : res.uid
        }

        r = db.collection("users").document(res.uid).set(user)
        print(r)

        return True, r
    
    except Exception as e:
        print(e)
        return False, str(e)

def get_user(uid):
    user = db.collection("users").document(uid).get().to_dict()
    print(user)

    return user

def get_user_using_email(email):
    try:
        auth.get_user_by_email(email)
        return True
    
    except Exception:
        return False

def delete_user(uid):
    auth.delete_user(uid)

    db.collection("users").document(uid).delete()

    return True

def get_all_users():
    user_docs = db.collection("users").get()
    user_list = [user.to_dict() for user in user_docs]
    
    return user_list

def user_login(email, password):
    try:
        user = firebase_auth.sign_in_with_email_and_password(email, password)
        return True, get_user(user['localId'])

    except Exception as e:
        print("Login failed")
        return False, "Invalid user details"

def send_password_reset_mail(email):
    try:
        user = auth.get_user_by_email(email)
    
        firebase_auth.send_password_reset_email(email)
        return True, "mail sent"

    except Exception as e:
        return False, str(e)

def upload_file(image_src, name=str(uuid.uuid4())):
    firebase_storage.child(name).put(image_src)
    url = firebase_storage.child(name).get_url(None)
    return str(url)

def delete_file(name):
    try:
        firebase_storage.delete(name, None)

        return True, "success"
    
    except Exception as e:
        return False, "file not found"

def insert_or_update_book(title, isbn, page_count, thumb_url, file_url, description, authors, categories, isUpdate=False):
    if not isUpdate and get_book_by_isbn(isbn) is not None:
        return False
    
    book = dict()

    book['isbn'] = isbn
    book['title'] = title
    book['authors'] = authors
    book['file_url'] = file_url
    book['thumb_url'] = thumb_url
    book['categories'] = categories
    book['page_count'] = page_count
    book['description'] = description

    if not isUpdate:
        db.collection("books").document(isbn).set(book)

    else:
        db.collection("books").document(isbn).update(book)

    return True

def get_all_books():
    book_docs = db.collection("books").get()
    book_list = [book.to_dict() for book in book_docs]
    
    return book_list

def delete_book(isbn):
    db.collection("books").document(isbn).delete()

    return True

def get_book_by_isbn(isbn):
    return db.collection("books").document(isbn).get().to_dict()

if __name__ == "__main__":
    # r = insert_or_update_book(
    #     "book01",
    #     "123456789",
    #     148,
    #     "https://shyam.com/projects/bookstore/storage/thumbs/123456789.jpg",
    #     "https://shyam.com/projects/bookstore/storage/files/123456789.jpg",
    #     "some about the book will go here..... i changed description ",
    #     ['author01', "author02"],
    #     ['cat02', "cat05"],
    #     True
    # )

    # print(r)

    # r = get_book_by_isbn("123456")
    # print(r)

    delete_file("books/1884777902.pdf")
