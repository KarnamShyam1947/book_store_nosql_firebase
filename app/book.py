from flask import Blueprint, flash, redirect, render_template, request, url_for, session
from FirebaseUtils import get_all_books, get_book_by_isbn, upload_file, insert_or_update_book, delete_book, delete_file
import json

book = Blueprint("book", __name__)

@book.route("/add-book", methods=['GET', 'POST'])
def add_book():
    if 'user' not in session:
        flash("Login to access this page", "warning")
        return redirect(url_for("auth.login"))
    
    if session['user']['role'] != 'admin':
        flash("only admin can access this", "danger")
        return redirect(url_for("book.all_books"))

    if request.method == 'POST':
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        pageCnt = request.form.get("pageCnt")
        desc = request.form.get("desc")
        thumbImage = request.files.get("coverPage")
        bookPdf = request.files.get("bookPdf")
        authors = request.form.getlist("author")
        categories = request.form.getlist("category")

        if get_book_by_isbn(isbn) is not None:
            flash("Book already exists with same isbn number", "danger")
            return redirect(url_for("book.add_book"))
        
        else:
            thumb_url = upload_file(thumbImage.read(), f"cover_pages/{isbn}.jpg")
            pdf_url = upload_file(bookPdf.read(), f"books/{isbn}.pdf")

            result = insert_or_update_book(
                title=title,
                isbn=isbn,
                page_count=pageCnt,
                thumb_url=thumb_url,
                file_url=pdf_url,
                description=desc,
                authors=authors,
                categories=categories,
                isUpdate=False
            )

            if result:
                flash("book added successfully", "success")

            else:
                flash("failed to add book", "danger")

            return redirect(url_for("book.add_book"))

    return render_template("book/add.html")

@book.route("/all-books")
def all_books():
    if 'user' not in session:
        flash("Login to access this page", "warning")
        return redirect(url_for("auth.login"))
    
    books = get_all_books()
    return render_template("book/all.html", books=books)

@book.route("/book/<isbn>")
def get_book(isbn):
    if 'user' not in session:
        flash("Login to access this page", "warning")
        return redirect(url_for("auth.login"))
    
    book = get_book_by_isbn(isbn)

    return render_template("book/details.html", book=book)

@book.route("/edit/<isbn>", methods=['GET', 'POST'])
def edit_book(isbn):
    if 'user' not in session:
        flash("Login to access this page", "warning")
        return redirect(url_for("auth.login"))
    
    if session['user']['role'] != 'admin':
        flash("only admin can access this", "danger")
        return redirect(url_for("book.all_books"))
    
    book = get_book_by_isbn(isbn)

    if request.method == 'POST':
        title = request.form.get("title")
        isbn = request.form.get("isbn")
        pageCnt = request.form.get("pageCnt")
        desc = request.form.get("desc")
        thumbImage = request.files.get("coverPage")
        bookPdf = request.files.get("bookPdf")
        authors = request.form.getlist("author")
        categories = request.form.getlist("category")

        thumb_url = request.form.get('oldThumbUrl')
        thumb_source = thumbImage.read()
        
        if len(thumb_source) > 0: 
            print("in thumb")       
            thumb_url = upload_file(thumb_source, f"cover_pages/{isbn}.jpg")

        pdf_url = request.form.get('oldBookPdf')
        pdf_src=bookPdf.read()

        if len(pdf_src) > 0:
            print("in book")
            pdf_url = upload_file(pdf_src, f"books/{isbn}.pdf")

        print(thumb_url)
        print(pdf_url)

        result = insert_or_update_book(
            title=title,
            isbn=isbn,
            page_count=pageCnt,
            thumb_url=thumb_url,
            file_url=pdf_url,
            description=desc,
            authors=authors,
            categories=categories,
            isUpdate=True
        )

        if result:
            flash("book updated successfully", "success")

        else:
            flash("failed to update book", "danger")

        return redirect(url_for("book.all_books"))
        

    return render_template("book/edit.html", book=book, authors=book['authors'], categories=book['categories'])

@book.route("/delete/<isbn>")
def process_delete_book(isbn):
    if 'user' not in session:
        flash("Login to access this page", "warning")
        return redirect(url_for("auth.login"))
    
    if session['user']['role'] != 'admin':
        flash("only admin can access this", "danger")
        return redirect(url_for("book.all_books"))
    

    delete_file(f"books/{isbn}.pdf")
    delete_file(f"cover_pages/{isbn}.jpg")
    delete_book(isbn)

    flash("book deleted successfully", "success")

    return redirect(url_for('book.all_books'))
